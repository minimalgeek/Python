import logging
from queue import Queue

from ibweb import config as cfg, bat_executor, mongo_queries
from flask import Flask, request, render_template, redirect, url_for, g

from ibweb.log.dblogger import error_logging_decorator
from ibweb.strategies import strategy_runner, dataloader
from ibweb.strategies.ib_manager import IBManager, Buy, Sell, SignalFactory
from ibweb.strategies.strategy import Strategy
from ibweb.strategies.strategy_01 import Strategy01

logger = logging.getLogger(__name__)

app = Flask(__name__)
manager = None
strategy = None


def get_manager() -> IBManager:
    global manager
    if manager is None:
        logger.info("Connecting to IB...")
        manager = IBManager("127.0.0.1", 7497, 1)
        logger.info("Server version: %s, connection time: %s",
                    manager.serverVersion(),
                    manager.twsConnectionTime())
    return manager


@error_logging_decorator
@app.route('/', methods=['GET', 'POST'])
def index():
    logger.info('Index route entry')
    ret_code = None

    if request.method == 'POST':
        logger.info('Request to execute [%s]', request.form['func'])
        bat_code = int(request.form['func'])
        ret_code = bat_executor.run_bat(bat_code)

    list_of_transcripts = mongo_queries.latest_zacks_report_dates_and_transcripts()
    list_of_positions = get_manager().load_portfolio()
    merge_transcripts_and_positions(list_of_positions, list_of_transcripts)

    return render_template('home.html',
                           ret_code=ret_code,
                           executor=bat_executor,
                           trs=list_of_transcripts,
                           positions=list_of_positions,
                           nav='home')


@error_logging_decorator
@app.route('/strategy', methods=['GET', 'POST'])
def strategy():
    global strategy
    logger.info('Strategy route entry')
    signals = []
    tickers_to_filter_by = [row['ticker']
                            for row in
                            list(cfg.tickers_collection.find({'group': cfg.options['ticker_filter_group']}))]
    dates_and_transcripts = dataloader.load_transcripts_and_zacks_list(filter_list=tickers_to_filter_by)
    if request.method == 'GET':
        strategy = strategy_runner.run_strategy(get_manager())
        # strat = Strategy01()
        # strat.signals.put(Buy('NVDA', 20))
        # strat.signals.put(Sell('ATK', 40))
        signals = list(strategy.signals.queue)
    else:
        data = request.form.to_dict()
        accepted_signals = Queue()
        for key, value in data.items():
            if value == 'on':
                for old_signal in list(strategy.signals.queue):
                    if old_signal.id == int(key):
                        accepted_signals.put(old_signal)

        get_manager().process_signals(accepted_signals)
    return render_template('strategy.html',
                           signals=signals,
                           dates=dates_and_transcripts,
                           nav='strategy')


@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        logger.error('Not running with the Werkzeug Server')
    func()
    return 'shutdown'


def merge_transcripts_and_positions(list_of_positions, list_of_transcripts):
    for tr in list_of_transcripts:
        tr['pos_totalQuantity'] = 0
        for pos in list_of_positions:
            if pos[0].symbol == tr['ticker']:
                tr['pos_orderId'] = pos[1].orderId
                tr['pos_totalQuantity'] += pos[1].totalQuantity
                tr['pos_action'] = pos[1].action


def main() -> Flask:
    logger.debug('Enter main')
    app.run()
    return app


if __name__ == '__main__':
    main()

import logging
from queue import Queue

from flask import Flask, request, render_template

from ibweb import config as cfg, service_caller, mongo_queries
from ibweb.strategies import strategy_runner, dataloader
from ibweb.strategies.ib_manager import IBManager
from mongolog.dblogger import error_logging_decorator

logger = logging.getLogger(__name__)

app = Flask(__name__)
manager = None
strategy = None


def get_manager() -> IBManager:
    global manager
    if manager is None:
        logger.info("Connecting to IB...")
        manager = IBManager('ibgw', 4003, 1)  # Docker
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
        ret_code = service_caller.run(bat_code)

    list_of_transcripts = mongo_queries.latest_zacks_report_dates_and_transcripts()
    list_of_positions = get_manager().load_portfolio()
    merge_transcripts_and_positions(list_of_positions, list_of_transcripts)

    return render_template('home.html',
                           ret_code=ret_code,
                           executor=service_caller,
                           trs=list_of_transcripts,
                           positions=list_of_positions,
                           nav='home')


@error_logging_decorator
@app.route('/strategy', methods=['GET', 'POST'])
def strategy():
    global strategy
    logger.info('Strategy route entry')
    signals = []
    tickers_to_filter_by = cfg.options['used_tickers']
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
    app.run(host='0.0.0.0', port=80)
    return app


if __name__ == '__main__':
    main()

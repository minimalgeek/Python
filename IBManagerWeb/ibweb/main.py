import logging
from queue import Queue

from flask import Flask, request, render_template, redirect, url_for, g
from ibweb import config as cfg, bat_executor, mongo_queries
from strategies import strategies_main
from strategies.ib_manager import IBManager, Buy, Sell, SignalFactory
from strategies.strategy import Strategy
from strategies.strategy_01 import Strategy01

logger = logging.getLogger(__name__)

app = Flask(__name__)


def get_manager() -> IBManager:
    if not hasattr(g, 'manager'):
        g.manager = IBManager("127.0.0.1", 7497, 1)
    return g.manager


def get_strategy() -> Strategy:
    if hasattr(g, 'strategy'):
        return g.strategy
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    logger.info('Index route entry')
    template = 'home.html'
    ret_code = None
    signals = None

    if request.method == 'POST':
        logger.info('Request to execute [%s]', request.form['func'])
        bat_code = int(request.form['func'])
        if bat_code == bat_executor.STRATEGY:
            template = 'strategy.html'
            g.strategy = strategies_main.run_strategy(get_manager())
            # strat = Strategy01()
            # strat.signals.put(Buy('NVDA', 20))
            # strat.signals.put(Sell('ATK', 40))
            signals = list(get_strategy().signals.queue)
        else:
            ret_code = bat_executor.run_bat(bat_code)

    list_of_transcripts = mongo_queries.latest_zacks_report_dates_and_transcripts()
    list_of_positions = get_manager().load_portfolio()
    merge_transcripts_and_positions(list_of_positions, list_of_transcripts)

    return render_template(template,
                           ret_code=ret_code,
                           executor=bat_executor,
                           trs=list_of_transcripts,
                           positions=list_of_positions,
                           signals=signals)


@app.route('/strategy', methods=['GET', 'POST'])
def strategy():
    logger.info('Strategy route entry')
    data = request.form.to_dict()
    signals = Queue()

    for key, value in data.items():
        if value == 'on':
            for old_signal in list(get_strategy().signals.queue):
                if old_signal.id == int(key):
                    signals.put(old_signal)

    get_manager().process_signals(signals)
    return redirect(url_for('index'))


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
    cfg.say_hello()
    app.run()
    return app


if __name__ == '__main__':
    main()

import logging
from flask import Flask, request, render_template
from ibweb import config as cfg, bat_executor, mongo_queries
from strategies.ib_manager import IBManager

logger = logging.getLogger(__name__)

app = Flask(__name__)
manager = IBManager("127.0.0.1", 7497, 1)

@app.route('/', methods=['GET', 'POST'])
def hello():
    ret_code = None
    if request.method == 'POST':
        logger.info('Request to execute [%s]', request.form['func'])
        ret_code = bat_executor.run_bat(int(request.form['func']))

    list_of_transcripts = mongo_queries.latest_zacks_report_dates_and_transcripts()
    list_of_positions = manager.load_portfolio()

    for tr in list_of_transcripts:
        for pos in list_of_positions:
            if pos[0].symbol == tr['ticker']:
                tr['pos_orderId'] = pos[1].orderId
                tr['pos_totalQuantity'] = pos[1].totalQuantity
                tr['pos_action'] = pos[1].action

    return render_template('home.html',
                           ret_code=ret_code,
                           executor=bat_executor,
                           trs=list_of_transcripts,
                           positions=list_of_positions)


@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        logger.error('Not running with the Werkzeug Server')
    func()
    return 'shutdown'


def main() -> Flask:
    logger.debug('Enter main')
    cfg.say_hello()
    app.run(debug=False)
    return app


if __name__ == '__main__':
    main()

import logging
from flask import Flask, request, render_template
from ibweb import config as cfg, bat_executor

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    ret_code = None
    if request.method == 'POST':
        logger.info('Request to execute [%s]', request.form['func'])
        ret_code = bat_executor.run_bat(int(request.form['func']))

    return render_template('home.html', ret_code=ret_code, executor=bat_executor)


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
    app.run(debug=True)
    return app


if __name__ == '__main__':
    main()

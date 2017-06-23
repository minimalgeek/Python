import logging
from flask import Flask, request, render_template
from ibweb import config as cfg

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('home.html')


@app.route('/zacks', methods=['POST'])
def zacks():
    return render_template('home.html')


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

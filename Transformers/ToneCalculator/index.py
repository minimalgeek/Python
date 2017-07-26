from flask import Flask
from tone_calc import ToneCalc

app = Flask(__name__)


@app.route('/calc')
def calc():
    tc = ToneCalc(host='db')
    tc.process_transcripts_and_save()
    return 'success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

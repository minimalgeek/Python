from flask import Flask, render_template
import requests, os

app = Flask(__name__)


@app.route('/')
def home():
    r = requests.get('http://product-service')
    items = r.json()['product']
    return render_template('index.html', items=items)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

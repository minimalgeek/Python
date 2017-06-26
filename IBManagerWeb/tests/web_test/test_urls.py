import pytest
from flask.testing import FlaskClient

from ibweb import main


@pytest.fixture
def client():
    app = main.app
    app.config['TESTING'] = True
    return app.test_client()


def test_home_page_header(client: FlaskClient):
    rsp = client.get('/')
    assert rsp.status == '200 OK'
    html = rsp.get_data(as_text=True)
    assert '<title>IB Manager</title>' in html
    assert '<h1>Execution steps</h1>' in html
    assert '<button' in html

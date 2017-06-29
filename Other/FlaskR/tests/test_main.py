import logging
import flaskr
import pytest
import os
import tempfile

logger = logging.getLogger(__name__)

@pytest.fixture(scope='session', autouse=True)
def before_after():
    # before
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.testing = True
    with flaskr.app.app_context():
        flaskr.main.init_db()
    yield before_after
    # after
    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])


@pytest.fixture(scope='module')
def app_client():
    return flaskr.app.test_client()

def test_home(app_client):
    rv = app_client.get('/')
    assert rv is not None
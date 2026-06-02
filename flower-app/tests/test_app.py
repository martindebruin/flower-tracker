import pytest
from unittest.mock import patch
import app as flower_app

@pytest.fixture
def client():
    flower_app.app.config['TESTING'] = True
    with flower_app.app.test_client() as c:
        yield c

def test_index_no_reading(client):
    with patch('app.db.get_latest', return_value=None):
        r = client.get('/')
        assert r.status_code == 200
        assert 'Ingen avläsning'.encode('utf-8') in r.data

def test_index_shows_reading(client):
    reading = {'timestamp': '2026-06-02T14:00:00', 'ettan': 'wet', 'spansk_timjan': 'dry'}
    with patch('app.db.get_latest', return_value=reading):
        r = client.get('/')
        body = r.data.decode('utf-8')
        assert 'Lilla Essingen Flower Tracker' in body
        assert 'Våt' in body
        assert 'Torr' in body

def test_read_now_triggers_read_and_redirects(client):
    with patch('app.do_read') as mock_read:
        r = client.post('/read-now')
        mock_read.assert_called_once()
        assert r.status_code == 302
        assert r.headers['Location'].endswith('/')

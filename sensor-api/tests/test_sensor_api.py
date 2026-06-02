import pytest
import sys
from unittest.mock import MagicMock, patch

@pytest.fixture
def client():
    mock_gpio = MagicMock()
    sys.modules['RPi'] = MagicMock()
    sys.modules['RPi.GPIO'] = mock_gpio
    import importlib
    import sensor_api
    importlib.reload(sensor_api)
    sensor_api.app.config['TESTING'] = True
    with patch('sensor_api.GPIO', mock_gpio):
        mock_gpio.input.return_value = 0
        with sensor_api.app.test_client() as c:
            yield c, mock_gpio

def test_read_wet(client):
    c, mock_gpio = client
    mock_gpio.input.return_value = 0
    r = c.get('/read')
    assert r.status_code == 200
    data = r.get_json()
    assert data['ettan'] == 'wet'
    assert data['spansk_timjan'] == 'wet'
    assert 'timestamp' in data

def test_read_dry(client):
    c, mock_gpio = client
    mock_gpio.input.return_value = 1
    r = c.get('/read')
    data = r.get_json()
    assert data['ettan'] == 'dry'
    assert data['spansk_timjan'] == 'dry'

def test_health(client):
    c, _ = client
    r = c.get('/health')
    assert r.get_json() == {'ok': True}

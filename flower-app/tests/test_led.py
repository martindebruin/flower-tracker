import pytest
from unittest.mock import patch
import led

def test_sends_default_when_both_wet():
    with patch('led.asyncio.run') as mock_run:
        led.notify_if_dry('wet', 'wet')
        mock_run.assert_called_once()

def test_calls_matrix_when_ettan_dry():
    with patch('led.asyncio.run') as mock_run:
        led.notify_if_dry('dry', 'wet')
        mock_run.assert_called_once()

def test_calls_matrix_when_spansk_dry():
    with patch('led.asyncio.run') as mock_run:
        led.notify_if_dry('wet', 'dry')
        mock_run.assert_called_once()

def test_calls_matrix_when_both_dry():
    with patch('led.asyncio.run') as mock_run:
        led.notify_if_dry('dry', 'dry')
        mock_run.assert_called_once()

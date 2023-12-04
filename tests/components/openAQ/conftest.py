"""Provide common fixtures for tests."""
from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def mock_aq_client():
    """Fixture to create a basic mock AQClient."""
    with patch("homeassistant.components.openAQ.aq_client.AQClient") as mock_client:
        yield mock_client.return_value


@pytest.fixture
def mock_aq_client_no_sensors():
    """Fixture to create a mock AQClient where get_device returns an empty sensors list."""
    with patch("homeassistant.components.openAQ.aq_client.AQClient") as mock_client:
        mock_client.return_value.get_device = Mock(return_value=Mock(sensors=[]))
        yield mock_client.return_value

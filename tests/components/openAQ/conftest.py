"""Provide common openAQ fixtures."""
from unittest.mock import AsyncMock, Mock, patch

import pytest


@pytest.fixture
def mock_aq_client():
    """Fixture to create a basic mock AQClient."""
    with patch("homeassistant.components.openAQ.aq_client.AQClient") as mock_client:
        yield mock_client.return_value


@pytest.fixture
def mock_aq_client_for_config_flow(mock_aq_client):
    """Fixture to provide mocked AQClient with predefined data for config flow tests."""
    # Define standard mocked responses
    mock_aq_client.get_device.side_effect = [
        # Successful data retrieval
        AsyncMock(
            return_value=Mock(
                sensors=[
                    {
                        "type": "pm25",
                        "value": 15,
                        "last_updated": "2023-12-04T08:00:00+00:00",
                    },
                    {
                        "type": "pm10",
                        "value": 20,
                        "last_updated": "2023-12-04T09:00:00+00:00",
                    },
                ],
                locality="Visby",
            )
        ),
        # Location not found (empty sensors list)
        AsyncMock(return_value=Mock(sensors=[], locality="")),
        # Response for invalid or empty API key: Simulate no sensor data and no locality info
        AsyncMock(return_value=Mock(sensors=[], locality="")),
    ]
    return mock_aq_client

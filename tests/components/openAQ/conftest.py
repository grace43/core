"""Provide common fixtures for tests."""
from unittest.mock import MagicMock, Mock, patch

import pytest

from homeassistant.components.openAQ import const
from homeassistant.components.openAQ.coordinator import OpenAQDataCoordinator


class MockAQClientSuccess:
    """Mock for AQClient that simulates a successful response."""

    def __init__(self, *args, **kwargs):
        """Initialize the mock AQClient."""
        pass

    def get_device(self):
        """Simulate getting device data from AQClient."""
        return Mock(sensors=["pm25", "o3"], locality="Valid Location")


@pytest.fixture
def mock_aq_client_no_sensors():
    """Fixture to create a mock AQClient where get_device returns an empty sensors list."""
    with patch("homeassistant.components.openAQ.config_flow.AQClient") as mock_client:
        mock_client.return_value.get_device = Mock(return_value=Mock(sensors=[]))
        yield mock_client.return_value


@pytest.fixture
def mock_aq_client_valid_data():
    """Fixture to create a mock AQClient with valid data."""
    with patch(
        "homeassistant.components.openAQ.config_flow.AQClient", new=MockAQClientSuccess
    ):
        yield


class MockAQClient:
    """Mock version of AQClient for testing purposes."""

    def __init__(self, sensor_data):
        """Initialize with mock sensor data."""
        self.sensor_data = sensor_data

    def get_device(self):
        """Simulate the structure of data returned by AQClient."""
        return {
            "datetime_last": {"utc": "2023-01-01T00:00:00Z"},
            "sensors": list(self.sensor_data.keys()),
        }

    def get_latest_metrics(self):
        """Simulate the structure of the latest metrics data."""
        metrics = [
            {"parameter": {"name": name}, "value": value}
            for name, value in self.sensor_data.items()
        ]
        return {"results": metrics}

    def setup_sensors(self):
        """Simulate sensor setup without making network calls."""


@pytest.fixture
def mock_openaq_client():
    """Fixture to patch AQClient.get_device with mock data."""

    def _mock_openaq_client(sensor_data):
        mock_client = MockAQClient(sensor_data)
        with patch(
            "homeassistant.components.openAQ.aq_client.AQClient.get_device",
            new=mock_client.get_device,
        ):
            yield

    return _mock_openaq_client


@pytest.fixture
async def setup_openaq(hass, mock_openaq_client):
    """Set up the OpenAQ integration for testing."""

    async def _setup(sensor_data):
        mock_openaq_client(sensor_data)
        mock_config_entry = MagicMock()
        mock_config_entry.entry_id = "test_entry_id"
        coordinator = OpenAQDataCoordinator(hass, "api_key", "location_id")

        # Use the mock client in the coordinator
        coordinator.client = MockAQClient(sensor_data)

        # Trigger data update in coordinator without real network calls
        await coordinator._async_update_data()

        hass.data.setdefault(const.DOMAIN, {})
        hass.data[const.DOMAIN][mock_config_entry.entry_id] = coordinator
        return mock_config_entry

    return _setup

<<<<<<< HEAD
<<<<<<< HEAD
"""Provide common fixtures for tests."""
from unittest.mock import MagicMock, Mock, patch

import pytest

from homeassistant.components.openAQ import const
from homeassistant.components.openAQ.coordinator import OpenAQDataCoordinator

=======
"""Provide common fixtures for tests."""
from collections.abc import Awaitable, Callable
from unittest.mock import Mock, patch

import pytest

<<<<<<< HEAD
>>>>>>> 0ef05b56a4 (mock api using client (#25))
=======
from homeassistant.components.openAQ.const import API_KEY_ID, DOMAIN, LOCATION_ID
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from tests.common import MockConfigEntry

ComponentSetup = Callable[[MockConfigEntry], Awaitable[None]]


@pytest.fixture(name="config_entry")
def mock_config_entry() -> MockConfigEntry:
    """Create openAQ entry in Home Assistant."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="openAQ",
        data={
            API_KEY_ID: 1234,
            LOCATION_ID: 1234,
        },
    )


@pytest.fixture(name="setup_integration")
async def mock_setup_integration(
    hass: HomeAssistant,
) -> Callable[[MockConfigEntry], Awaitable[None]]:
    """Fixture for setting up the component."""

    async def func(mock_config_entry: MockConfigEntry) -> None:
        mock_config_entry.add_to_hass(hass)
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()

    return func

>>>>>>> 4d38476d3a (Setup test. TODO make fixture for coordinator)

class MockAQClientSuccess:
    """Mock for AQClient that simulates a successful response."""

    def __init__(self, *args, **kwargs):
        """Initialize the mock AQClient."""
        pass

    def get_device(self):
        """Simulate getting device data from AQClient."""
        return Mock(sensors=["pm25", "o3"], locality="Valid Location")


@pytest.fixture
<<<<<<< HEAD
=======
def mock_aq_client():
    """Fixture to create a basic mock AQClient."""
    with patch("homeassistant.components.openAQ.config_flow.AQClient") as mock_client:
        yield mock_client.return_value


@pytest.fixture
>>>>>>> 0ef05b56a4 (mock api using client (#25))
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
<<<<<<< HEAD


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
=======
"""Define test fixtures for openAQ."""
>>>>>>> 0137d8c7a9 (create test folder)
=======
>>>>>>> 0ef05b56a4 (mock api using client (#25))

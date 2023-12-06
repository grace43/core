"""Provide common fixtures for tests."""
from collections.abc import Awaitable, Callable
from unittest.mock import Mock, patch

import pytest

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


class MockAQClientSuccess:
    """Mock for AQClient that simulates a successful response."""

    def __init__(self, *args, **kwargs):
        """Initialize the mock AQClient."""
        pass

    def get_device(self):
        """Simulate getting device data from AQClient."""
        return Mock(sensors=["pm25", "o3"], locality="Valid Location")


@pytest.fixture
def mock_aq_client():
    """Fixture to create a basic mock AQClient."""
    with patch("homeassistant.components.openAQ.config_flow.AQClient") as mock_client:
        yield mock_client.return_value


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

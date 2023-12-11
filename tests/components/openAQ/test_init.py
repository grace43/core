"""Test openAQ component setup process."""

import pytest

from homeassistant.components.openAQ.const import DOMAIN
from homeassistant.components.openAQ.coordinator import OpenAQDataCoordinator
from homeassistant.core import HomeAssistant

from .conftest import ComponentSetup

from tests.common import MockConfigEntry


@pytest.mark.asyncio
async def test_add_correct_devices(
    hass: HomeAssistant,
    setup_integration: ComponentSetup,
    config_entry: MockConfigEntry,
):
    """Test for successfully setting up the platform and entities."""
    await setup_integration(
        config_entry, "location_good.json", "measurements_good.json"
    )
    entities = hass.states.async_entity_ids("sensor")
    assert len(entities) == 5
    coordinator: OpenAQDataCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    assert coordinator.location_id == 10496


@pytest.mark.asyncio
async def test_add_correct_and_incorrect_devices(
    hass: HomeAssistant,
    setup_integration: ComponentSetup,
    config_entry: MockConfigEntry,
):
    """Test for successfully setting up the platform and entities where one entity is inorrect."""
    await setup_integration(config_entry, "location_bad.json", "measurements_good.json")
    entities = hass.states.async_entity_ids("sensor")
    assert len(entities) == 5


@pytest.mark.asyncio
async def test_no_devices(
    hass: HomeAssistant,
    setup_integration: ComponentSetup,
    config_entry: MockConfigEntry,
):
    """Test for successfully setting up the platform and entities where one entity is inorrect."""
    await setup_integration(
        config_entry, "location_no_devices.json", "measurements_good.json"
    )
    entities = hass.states.async_entity_ids("sensor")
    assert len(entities) == 1  # only last_updated should be here


@pytest.mark.asyncio
async def test_wrong_location_id(
    hass: HomeAssistant,
    setup_integration: ComponentSetup,
    config_entry: MockConfigEntry,
):
    """Test for unsuccessfully setting up the platform as the location entered does not exist."""
    await setup_integration(
        config_entry, "location_wrong_location_id.json", "measurements_good.json"
    )
    entities = hass.states.async_entity_ids("sensor")
    assert len(entities) == 0

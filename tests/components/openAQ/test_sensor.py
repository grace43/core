"""Test openAQ sensors."""

import pytest

from homeassistant.core import HomeAssistant

from .conftest import ComponentSetup

from tests.common import MockConfigEntry


@pytest.mark.asyncio
async def test_add_all_sensors_supported(
    hass: HomeAssistant,
    setup_integration: ComponentSetup,
    config_entry: MockConfigEntry,
):
    """Test for successfully setting up all sensors."""
    await setup_integration(
        config_entry, "location_all_good.json", "measurements_all_good.json"
    )
    assert hass.states.get("sensor.temperature").state == "43.0"
    assert hass.states.get("sensor.ozone").state
    assert hass.states.get("sensor.pm10").state == "17.0"
    assert hass.states.get("sensor.nitrogen_dioxide").state == "29.0"
    assert hass.states.get("sensor.sulphur_dioxide").state == "2.0"
    assert hass.states.get("sensor.co").state == "290.0"
    assert hass.states.get("sensor.atmospheric_pressure").state == "1000.0"
    assert hass.states.get("sensor.humidity").state == "70.0"
    assert hass.states.get("sensor.timestamp").state == "2023-12-08T11:00:00+00:00"
    assert hass.states.get("sensor.pm25").state == "8.2"


@pytest.mark.asyncio
async def test_negative_values_sensors(
    hass: HomeAssistant,
    setup_integration: ComponentSetup,
    config_entry: MockConfigEntry,
):
    """Test for negative sensor values."""
    await setup_integration(
        config_entry, "location_all_good.json", "measurements_negative.json"
    )
    assert hass.states.get("sensor.temperature").state == "-43.0"
    assert hass.states.get("sensor.ozone").state == "unknown"
    assert hass.states.get("sensor.pm10").state == "unknown"
    assert hass.states.get("sensor.nitrogen_dioxide").state == "unknown"
    assert hass.states.get("sensor.sulphur_dioxide").state == "unknown"
    assert hass.states.get("sensor.co").state == "unknown"
    assert hass.states.get("sensor.atmospheric_pressure").state == "unknown"
    assert hass.states.get("sensor.humidity").state == "unknown"
    assert hass.states.get("sensor.pm25").state == "unknown"

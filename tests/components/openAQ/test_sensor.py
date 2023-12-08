"""Test cases for sensor.py."""
from unittest.mock import MagicMock

import pytest

from homeassistant.components.openAQ.sensor import async_setup_entry


@pytest.mark.asyncio
async def test_sensor_exists(hass, setup_openaq):
    """Test if a sensor exists in the JSON object and the hardcoded values."""
    sensor_data = {"pm25": 10, "pm10": 20, "o3": 30, "co2": 40, "no2": 50}
    mock_config_entry = await setup_openaq(sensor_data)
    async_add_entities = MagicMock()
    await async_setup_entry(hass, mock_config_entry, async_add_entities)
    assert hass.states.get("sensor.openaq_pm25") is not None
    assert hass.states.get("sensor.openaq_pm25").state == "10"


@pytest.mark.asyncio
async def test_adding_non_hardcoded_sensor(hass, setup_openaq):
    """Test what happens when you add a sensor that isn't hardcoded."""
    sensor_data = {"pm25": 10, "unexpected_sensor": 100}
    mock_config_entry = await setup_openaq(sensor_data)
    async_add_entities = MagicMock()
    await async_setup_entry(hass, mock_config_entry, async_add_entities)
    assert hass.states.get("sensor.openaq_unexpected_sensor") is None


@pytest.mark.asyncio
async def test_add_all_sensors(hass, setup_openaq):
    """Test adding all sensors and check if everything is added."""
    sensor_data = {"pm25": 10, "pm10": 20, "o3": 30, "co2": 40, "no2": 50}
    mock_config_entry = await setup_openaq(sensor_data)
    async_add_entities = MagicMock()
    await async_setup_entry(hass, mock_config_entry, async_add_entities)
    for sensor_name in sensor_data:
        assert hass.states.get(f"sensor.openaq_{sensor_name}") is not None


@pytest.mark.asyncio
async def test_values_get_updated(hass, setup_openaq):
    """Test that values get updated (both in the object and hardcoded)."""
    initial_data = {"pm25": 10}
    mock_config_entry = await setup_openaq(initial_data)
    async_add_entities = MagicMock()
    await async_setup_entry(hass, mock_config_entry, async_add_entities)

    updated_data = {"pm25": 15}
    await setup_openaq(updated_data)  # Update the setup with new data
    await hass.data["openAQ"][mock_config_entry.entry_id].async_refresh()
    assert hass.states.get("sensor.openaq_pm25").state == "15"


@pytest.mark.asyncio
async def test_no_negative_values_air_quality(hass, setup_openaq):
    """Test that the API does not return negative values for air quality sensors."""
    sensor_data = {"pm25": -10, "pm10": -20}
    mock_config_entry = await setup_openaq(sensor_data)
    async_add_entities = MagicMock()
    await async_setup_entry(hass, mock_config_entry, async_add_entities)
    assert int(hass.states.get("sensor.openaq_pm25").state) >= 0
    assert int(hass.states.get("sensor.openaq_pm10").state) >= 0


@pytest.mark.asyncio
async def test_handling_negative_values_other_sensors(hass, setup_openaq):
    """Test that negative values are returned correctly for sensors where it's acceptable."""
    sensor_data = {"co2": -40, "no2": -50}
    mock_config_entry = await setup_openaq(sensor_data)
    async_add_entities = MagicMock()
    await async_setup_entry(hass, mock_config_entry, async_add_entities)
    assert int(hass.states.get("sensor.openaq_co2").state) < 0
    assert int(hass.states.get("sensor.openaq_no2").state) < 0

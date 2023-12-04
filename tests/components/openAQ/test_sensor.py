"""Test cases for sensor.py."""
<<<<<<< HEAD
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
=======
from unittest.mock import MagicMock, patch

import pytest

from homeassistant.components.openAQ import const
from homeassistant.components.openAQ.sensor import (
    OpenAQDataCoordinator,
    OpenAQSensor,
    OpenAQSensorDescription,
)
from homeassistant.components.sensor import EntityCategory, SensorDeviceClass
from homeassistant.core import HomeAssistant


# Mock for AQClient
class MockAQClient:
    """Mock for AQClient."""

    def __init__(self):
        """Initialize MockAQClient."""
        self.sensors = [
            MagicMock(parameter=MagicMock(name="pm25")),
            MagicMock(parameter=MagicMock(name="o3")),
        ]

    def get_device(self):
        """Mock the get_device method."""
        return MagicMock(
            id="1234", locality="TestLocation", owner=MagicMock(name="TestOwner")
        )

    def get_latest_metrices(self):
        """Mock the get_latest_metrices method."""
        return MagicMock(
            results=[
                MagicMock(parameter=MagicMock(name="pm25"), value=15),
                MagicMock(parameter=MagicMock(name="o3"), value=0.03),
            ]
        )


# Mock for OpenAQDataCoordinator
class MockOpenAQDataCoordinator(OpenAQDataCoordinator):
    """Mock for OpenAQDataCoordinator."""

    def __init__(self):
        """Initialize MockOpenAQDataCoordinator."""
        self.data = {
            "pm25": 15,
            "o3": 0.03,
        }

    def get_sensors(self):
        """Mock the get_sensors method."""
        return [
            MagicMock(parameter=MagicMock(name="pm25")),
            MagicMock(parameter=MagicMock(name="o3")),
        ]


@pytest.mark.usefixtures("mocker")
@patch("homeassistant.components.openAQ.sensor.OPENAQ_PARAMETERS")
def test_sensor_existence(mock_openaq_parameters, mocker):
    """Test if OpenAQSensor interacts with OPENAQ_PARAMETERS by verifying sensor key existence."""
    # Set up the mock OPENAQ_PARAMETERS
    mock_openaq_parameters.return_value = {"pm25": True}

    # Creating instances of MockAQClient and MockOpenAQDataCoordinator
    MockAQClient()
    coordinator = MockOpenAQDataCoordinator()

    # Creating a MagicMock instance representing HomeAssistant
    mock_home_assistant = mocker.MagicMock(spec=HomeAssistant)

    # Creating an OpenAQSensorDescription instance
    description = OpenAQSensorDescription(
        key="pm25",  # Adjust key to match the key in OPENAQ_PARAMETERS
        name="Particle Matter 2.5",
        metric=SensorDeviceClass.PM25,
        entity_category=EntityCategory.DIAGNOSTIC,
    )

    # Creating an OpenAQSensor instance using the previously created objects
    sensor = OpenAQSensor(mock_home_assistant, "1234", description, coordinator)

    # Assertions to check if the OpenAQSensor interacts with OPENAQ_PARAMETERS
    assert sensor.entity_description.key in mock_openaq_parameters.return_value


@pytest.mark.usefixtures("mocker")
@patch("homeassistant.components.openAQ.sensor.OPENAQ_PARAMETERS")
def test_non_existing_sensor(mock_openaq_parameters, mocker):
    """Test when you add a sensor that isn't hardcoded in openAQ_parameters."""

    # Mock the 'OPENAQ_PARAMETERS' with an empty dictionary
    mock_openaq_parameters.return_value = {}

    # Create instances of MockAQClient and MockOpenAQDataCoordinator
    coordinator = MockOpenAQDataCoordinator()
    mock_home_assistant = mocker.MagicMock(spec=HomeAssistant)

    # Create an OpenAQSensorDescription instance for a non-existing sensor
    description = OpenAQSensorDescription(
        key="ph",
        name="potential hydrogen",
        metric=SensorDeviceClass.PH,
        entity_category=EntityCategory.DIAGNOSTIC,
    )

    # Create an OpenAQSensor instance using the specified description
    sensor = OpenAQSensor(mock_home_assistant, "1234", description, coordinator)

    # Assertions to verify the behavior when creating a non-existing sensor
    assert sensor.entity_description.key == "ph"
    assert sensor.entity_description.name == "potential hydrogen"
    assert sensor.entity_description.metric == SensorDeviceClass.PH
    assert sensor.entity_description.entity_category == EntityCategory.DIAGNOSTIC
    assert (
        "PH" not in mock_openaq_parameters
    )  # Ensure the sensor isn't in the parameters list


# Testcase3: Ensure all sensors in sensor_keys are present in OPENAQ_PARAMETERS
def test_missing_sensors():
    """Test to ensure sensors in sensor_keys are present in OPENAQ_PARAMETERS."""

    sensor_keys = {
        "pm25": SensorDeviceClass.PM25,
        "pm10": SensorDeviceClass.PM10,
        "pm1": SensorDeviceClass.PM1,
        "o3": SensorDeviceClass.OZONE,
        "pressure": SensorDeviceClass.ATMOSPHERIC_PRESSURE,
        "temperature": SensorDeviceClass.TEMPERATURE,
        "relativehumidity": SensorDeviceClass.HUMIDITY,
        "no2": SensorDeviceClass.NITROGEN_DIOXIDE,
        "no": SensorDeviceClass.NITROGEN_MONOXIDE,
        "co": SensorDeviceClass.CO,
        "co2": SensorDeviceClass.CO2,
        "so2": SensorDeviceClass.SULPHUR_DIOXIDE,
        "last_update": SensorDeviceClass.TIMESTAMP,
    }

    # Get all keys from OPENAQ_PARAMETERS
    openaq_keys = const.OPENAQ_PARAMETERS.keys()

    # Find missing sensors in sensor_keys that are in OPENAQ_PARAMETERS
    missing_sensors = [sensor for sensor in openaq_keys if sensor not in sensor_keys]

    assert (
        not missing_sensors
    ), f"Missing sensors in SENSOR_KEY: {', '.join(missing_sensors)}"


@pytest.mark.usefixtures("mocker")
@patch("homeassistant.components.openAQ.sensor.OPENAQ_PARAMETERS")
def test_update_values(mock_openaq_parameters, mocker):
    """Test to check that values get updated (Both in the object and hardcoded)."""
    # Set up the mock OPENAQ_PARAMETERS
    mock_openaq_parameters.return_value = {"temperature": 15}

    # Creating instances of MockAQClient and MockOpenAQDataCoordinator
    MockAQClient()
    coordinator = MockOpenAQDataCoordinator()

    # Creating a MagicMock instance representing HomeAssistant
    mock_home_assistant = mocker.MagicMock(spec=HomeAssistant)

    # Creating an OpenAQSensorDescription instance
    description = OpenAQSensorDescription(
        key="temperature",
        name="temperature",
        metric=SensorDeviceClass.TEMPERATURE,
        entity_category=EntityCategory.DIAGNOSTIC,
    )

    # Creating an OpenAQSensor instance using the previously created objects
    sensor = OpenAQSensor(mock_home_assistant, "1234", description, coordinator)

    # Update value in mock OPENAQ_PARAMETERS
    updated_temperature_value = 20
    mock_openaq_parameters.return_value["temperature"] = updated_temperature_value

    # Update value in MockOpenAQDataCoordinator
    coordinator.data["temperature"] = updated_temperature_value

    # Check if the value is updated in the object
    assert sensor.coordinator.data["temperature"] == updated_temperature_value

    # Check if the value is updated in the hardcoded values
    assert sensor.entity_description.key == "temperature"
    assert sensor.entity_description.name == "temperature"
    assert sensor.entity_description.metric == SensorDeviceClass.TEMPERATURE
    assert sensor.entity_description.entity_category == EntityCategory.DIAGNOSTIC


@pytest.mark.usefixtures("mocker")
def test_air_quality_sensor_values():
    """Test to check that API should not return negative values(air quality sensors) and add error handling."""
    # Create instances of MockAQClient and MockOpenAQDataCoordinator
    MockAQClient()
    coordinator = MockOpenAQDataCoordinator()

    # Assuming API returns negative values for some sensors
    sensors = [
        "o3",
        "pm25",
        "pm10",
        "pm1",
        "o3",
        "pressure",
        "relativehumidity",
        "no2",
        "no",
        "co",
        "co2",
        "so2",
        "last_update",
    ]

    for sensor in sensors:
        coordinator.data[sensor] = -5  # Assigning a negative value

    # Check if the API returns negative values for air quality sensors
    for sensor in sensors:
        sensor_value = coordinator.data[sensor]

        if sensor_value < 0:
            # If a negative value is found, handle the error accordingly
            coordinator.data[sensor] = 0  # Set negative value to 0 or any default value
            # Log the error or perform necessary error handling steps
            f"Error: Negative value found for sensor '{sensor}'. Value updated to 0."

            # Assertion to verify that the value is non-negative after error handling
            assert (
                coordinator.data[sensor] >= 0
            ), f"Negative value found for sensor: {sensor}"

        if sensor in ["relativehumidity"]:
            # Handling specific sensors like relative humidity
            if sensor_value < 0 or sensor_value > 100:
                coordinator.data[sensor] = 50  # Set to default value if out of range
                f"Error: Invalid value for sensor '{sensor}'. Value updated to 50."

    # Assertion to verify that the value is within the valid range after error handling
    assert 0 <= coordinator.data[sensor] <= 100, f"Invalid value for sensor: {sensor}"


@pytest.mark.usefixtures("mocker")
def test_negative_temperature_value():
    """Test  if temperature sensor can return negative values and display them correctly."""
    # Create an instance of MockOpenAQDataCoordinator
    coordinator = MockOpenAQDataCoordinator()

    # Set a negative value for temperature sensor
    temperature_value = -7  # Assuming temperature sensor returns a negative value
    coordinator.data["temperature"] = temperature_value

    # Check if the temperature sensor returns the negative value
    assert (
        coordinator.data["temperature"] == temperature_value
    ), "Temperature sensor should return the negative value"
>>>>>>> 1e410304b5 (Added test_sensor file (Rithika & Arpita ))

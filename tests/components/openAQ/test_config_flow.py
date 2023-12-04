"""Test the OpenAQ config flow."""
from homeassistant import data_entry_flow
from homeassistant.components.openAQ.config_flow import ConfigFlow
from homeassistant.core import HomeAssistant

# Define an invalid user input with an invalid location ID
INVALID_USER_INPUT = {
    "location_id": "invalid_location_id",
    "api_id": "your_api_key",
}

# Provide user input with a valid location and API key
USER_INPUT = {
    "location_id": "10496",
    "api_id": "0ce03655421037c966e7f831503000dc93c80a8fc14a434c6406f0adbbfaa61e",
}


async def test_config_flow_invalid_location(
    hass: HomeAssistant, mock_aq_client_no_sensors
):
    """Test the OpenAQ config flow with invalid user input."""
    # Initialize the config flow
    flow = ConfigFlow()
    flow.hass = hass

    # Start the config flow with invalid user input
    result = await flow.async_step_user(INVALID_USER_INPUT)

    # Check if an error message is returned
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"]["location"] == "not_found"


# Define a test case that uses the mock_aq_client_valid_data fixture
async def test_config_flow_valid_location(
    hass: HomeAssistant, mock_aq_client_valid_data
):
    """Test the OpenAQ config flow with valid user input and mocked data."""
    # Initialize the config flow
    flow = ConfigFlow()
    flow.hass = hass

    # Start the config flow with valid user input
    result = await flow.async_step_user(USER_INPUT)

    # Check if the flow creates an entry with the provided user input
    assert result["type"] == "create_entry"
    assert result["title"] == "Valid Location"
    assert result["data"] == USER_INPUT

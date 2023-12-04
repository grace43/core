"""Test the OpenAQ config flow."""


from homeassistant import data_entry_flow
from homeassistant.core import HomeAssistant

# Import the fixtures defined in conftest.py

# Define an invalid user input with an invalid location ID
INVALID_USER_INPUT = {
    "location_id": "invalid_location_id",
    "api_id": "your_api_key",  # Replace with your API key
}


async def test_config_flow_invalid_location(
    hass: HomeAssistant, mock_aq_client_no_sensors
):
    """Test the OpenAQ config flow with invalid location."""
    # Import the ConfigFlow class after applying the mock
    from homeassistant.components.openAQ.config_flow import ConfigFlow

    # Initialize the config flow
    flow = ConfigFlow()
    flow.hass = hass

    # Start the config flow with invalid user input
    result = await flow.async_step_user(INVALID_USER_INPUT)

    # Check if an error message is returned
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"]["location"] == "not_found"

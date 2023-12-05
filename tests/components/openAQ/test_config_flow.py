<<<<<<< HEAD
<<<<<<< HEAD
"""Test the OpenAQ config flow."""
from homeassistant import data_entry_flow
from homeassistant.components.openAQ.config_flow import ConfigFlow
from homeassistant.core import HomeAssistant

# Define an invalid user input with an invalid location ID
INVALID_USER_INPUT = {
    "location_id": "invalid_location_id",
    "api_id": "0ce03655421037c966e7f831503000dc93c80a8fc14a434c6406f0adbbfaa61e",
}

# Provide user input with a valid location and API key
USER_INPUT = {
    "location_id": "10496",
    "api_id": "0ce03655421037c966e7f831503000dc93c80a8fc14a434c6406f0adbbfaa61e",
}


# Define a test case that uses the mock_aq_client_no_sensors fixture
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
=======
"""Test the Open Exchange Rates config flow."""
import asyncio
from collections.abc import Generator
from typing import Any
from unittest.mock import AsyncMock, patch

from aioopenexchangerates import (
    OpenExchangeRatesAuthError,
    OpenExchangeRatesClientError,
)
import pytest

from homeassistant import config_entries
from homeassistant.components.openexchangerates.const import DOMAIN
=======
"""Test the OpenAQ config flow."""
from homeassistant import data_entry_flow
from homeassistant.components.openAQ.config_flow import ConfigFlow
>>>>>>> 0ef05b56a4 (mock api using client (#25))
from homeassistant.core import HomeAssistant

# Define an invalid user input with an invalid location ID
INVALID_USER_INPUT = {
    "location_id": "invalid_location_id",
    "api_id": "0ce03655421037c966e7f831503000dc93c80a8fc14a434c6406f0adbbfaa61e",
}

# Provide user input with a valid location and API key
USER_INPUT = {
    "location_id": "10496",
    "api_id": "0ce03655421037c966e7f831503000dc93c80a8fc14a434c6406f0adbbfaa61e",
}


# Define a test case that uses the mock_aq_client_no_sensors fixture
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

<<<<<<< HEAD
    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "USD"
    assert result["data"] == {
        "api_key": "test-api-key",
        "base": "USD",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_invalid_auth(
    hass: HomeAssistant,
    mock_latest_rates_config_flow: AsyncMock,
) -> None:
    """Test we handle invalid auth."""
    mock_latest_rates_config_flow.side_effect = OpenExchangeRatesAuthError()
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"api_key": "bad-api-key"},
    )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_auth"}


async def test_form_cannot_connect(
    hass: HomeAssistant,
    mock_latest_rates_config_flow: AsyncMock,
) -> None:
    """Test we handle cannot connect error."""
    mock_latest_rates_config_flow.side_effect = OpenExchangeRatesClientError()
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"api_key": "test-api-key"},
    )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}


async def test_form_unknown_error(
    hass: HomeAssistant,
    mock_latest_rates_config_flow: AsyncMock,
) -> None:
    """Test we handle unknown error."""
    mock_latest_rates_config_flow.side_effect = Exception()
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"api_key": "test-api-key"},
    )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "unknown"}


async def test_already_configured_service(
    hass: HomeAssistant,
    mock_latest_rates_config_flow: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test we abort if the service is already configured."""
    mock_config_entry.add_to_hass(hass)
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] is None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"api_key": "test-api-key"},
    )

    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_no_currencies(hass: HomeAssistant, currencies: AsyncMock) -> None:
    """Test we abort if the service fails to retrieve currencies."""
    currencies.side_effect = OpenExchangeRatesClientError()
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "cannot_connect"


async def test_currencies_timeout(hass: HomeAssistant, currencies: AsyncMock) -> None:
    """Test we abort if the service times out retrieving currencies."""

    async def currencies_side_effect():
        await asyncio.sleep(1)
        return {"USD": "United States Dollar", "EUR": "Euro"}

    currencies.side_effect = currencies_side_effect

    with patch(
        "homeassistant.components.openexchangerates.config_flow.CLIENT_TIMEOUT", 0
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "timeout_connect"


async def test_latest_rates_timeout(
    hass: HomeAssistant,
    mock_latest_rates_config_flow: AsyncMock,
) -> None:
    """Test we abort if the service times out retrieving latest rates."""

    async def latest_rates_side_effect(*args: Any, **kwargs: Any) -> dict[str, float]:
        await asyncio.sleep(1)
        return {"EUR": 1.0}

    mock_latest_rates_config_flow.side_effect = latest_rates_side_effect

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "homeassistant.components.openexchangerates.config_flow.CLIENT_TIMEOUT", 0
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"api_key": "test-api-key"},
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "timeout_connect"}


async def test_reauth(
    hass: HomeAssistant,
    mock_latest_rates_config_flow: AsyncMock,
    mock_setup_entry: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test we can reauthenticate the config entry."""
    mock_config_entry.add_to_hass(hass)
    flow_context = {
        "source": config_entries.SOURCE_REAUTH,
        "entry_id": mock_config_entry.entry_id,
        "title_placeholders": {"name": mock_config_entry.title},
        "unique_id": mock_config_entry.unique_id,
    }

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context=flow_context, data=mock_config_entry.data
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] is None

    mock_latest_rates_config_flow.side_effect = OpenExchangeRatesAuthError()

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            "api_key": "invalid-test-api-key",
        },
    )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_auth"}

    mock_latest_rates_config_flow.side_effect = None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            "api_key": "new-test-api-key",
        },
    )
    await hass.async_block_till_done()

    assert result["type"] == "abort"
    assert result["reason"] == "reauth_successful"
    assert len(mock_setup_entry.mock_calls) == 1
>>>>>>> 0137d8c7a9 (create test folder)
=======
    # Check if the flow creates an entry with the provided user input
    assert result["type"] == "create_entry"
    assert result["title"] == "Valid Location"
    assert result["data"] == USER_INPUT
>>>>>>> 0ef05b56a4 (mock api using client (#25))

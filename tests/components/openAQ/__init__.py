<<<<<<< HEAD
"""Tests for openAQ component."""
from unittest.mock import patch


def patch_setup_entry() -> bool:
    """Patch interface."""
    return patch("homeassistant.components.openAQ.async_setup_entry", return_value=True)
=======
"""Tests for OpenERZ component."""
>>>>>>> 0137d8c7a9 (create test folder)

"""Test to test the module binary_sensor.py."""

from homeassistant.components.roomba.binary_sensor import RoombaBinStatus

# Define some test data (you may need to adjust this according to your actual data)
test_data = {"bin": {"full": True}}


# Create a mock Roomba objecho
class MockRoomba:
    """Test for the MockRoobha."""

    def __init__(self, data):
        """Test for the __init__ method."""
        self.data = data
        self.master_state = {
            "state": {"reported": data}  # Set reported state based on your test_data
        }


def test_roomba_bin_status_on():
    """Test the RoombaBinStatus class when bin is full."""
    # Create a mock Roomba instance
    roomba = MockRoomba(test_data)

    # Create an instance of RoombaBinStatus
    bin_status = RoombaBinStatus(roomba, "12345")

    # Test the unique_id property
    assert bin_status.unique_id == "bin_12345"

    # Test the is_on property
    assert bin_status.is_on is True  # Updated assertion


def test_roomba_bin_status_off():
    """Test the RoombaBinStatus class when bin is not full."""
    # Create a mock Roomba instance with bin not full
    roomba = MockRoomba({"bin": {"full": False}})

    # Create an instance of RoombaBinStatus
    bin_status = RoombaBinStatus(roomba, "54321")

    # Test the is_on property
    assert bin_status.is_on is False  # Updated assertion

# We need to add this import to be able to find the `consumer` module
#import sys
#sys.path.insert(0, '.')

from consumer import calculate_moving_average

# A simple mock object to simulate a database price record
class MockPrice:
    def __init__(self, price):
        self.price = price

def test_calculate_moving_average():
    """
    Tests the moving average calculation with a simple list of mock prices.
    """
    # Arrange: Create a list of 5 mock price objects
    mock_prices = [
        MockPrice(10),
        MockPrice(12),
        MockPrice(11),
        MockPrice(13),
        MockPrice(14)
    ]

    # Act: Call the function we want to test
    result = calculate_moving_average(mock_prices)

    # Assert: Check if the result is what we expect ( (10+12+11+13+14) / 5 = 12 )
    assert result == 12.0
from unittest.mock import patch, Mock, mock_open
import pytest
from src.utils import read_transactions, transaction_sum

@pytest.fixture
def first_operation() -> dict:
    return {
        "operationAmount": {"amount": "8221.37", "currency": {"code": "USD"}},
    }

def test_read_transactions_and_transaction_sum(first_operation: dict) -> None:
    with patch("builtins.open", mock_open(read_data=json.dumps([first_operation]))):
        assert read_transactions(Path("valid_file.json")) == [first_operation]

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {"result": 9000.0}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        assert transaction_sum(first_operation) == 9000.0



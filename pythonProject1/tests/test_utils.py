from unittest.mock import patch, Mock
import pytest
from your_module import read_transactions, transaction_sum


@pytest.fixture
def first_operation() -> dict:
    return {
        "operationAmount": {"amount": "8221.37", "currency": {"code": "USD"}},
    }


def test_read_transactions_and_transaction_sum(first_operation: dict) -> None:
    """Тесты для чтения файла и вычисления суммы транзакции"""

    mock = Mock(return_value=[first_operation])
    with patch("builtins.open", mock_open(read_data=json.dumps([first_operation]))):
        assert read_transactions("valid_file.json") == [first_operation]

    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"result": 9000.0}
        assert transaction_sum(first_operation) == 9000.0


import pytest

from limit_order_book.limit_order_book import LimitOrderBook


@pytest.fixture
def limit_order_book():
    return LimitOrderBook()

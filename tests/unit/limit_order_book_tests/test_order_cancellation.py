from decimal import Decimal


def test_cancel_buy_order(limit_order_book):
    limit_order_book.place_order(
        order_id="O1", order_side="buy", order_price=1, order_quantity=1
    )
    assert "O1" in limit_order_book.active_orders

    order_cancel_result = limit_order_book.cancel_order(order_id="O1")

    assert order_cancel_result is True
    assert limit_order_book.buy_orders.search(-1) is None
    assert "O1" not in limit_order_book.active_orders


def test_cancel_sell_order(limit_order_book):
    limit_order_book.place_order(
        order_id="O1", order_side="sell", order_price=1, order_quantity=1
    )
    assert "O1" in limit_order_book.active_orders

    order_cancel_result = limit_order_book.cancel_order(order_id="O1")

    assert order_cancel_result is True
    assert limit_order_book.sell_orders.search(1) is None
    assert "O1" not in limit_order_book.active_orders


def test_cancel_a_cancelled_buy_order(limit_order_book):
    limit_order_book.place_order(
        order_id="O1", order_side="buy", order_price=1, order_quantity=1
    )
    first_order_cancel_result = limit_order_book.cancel_order(order_id="O1")
    second_order_cancel_result = limit_order_book.cancel_order(order_id="O1")
    assert first_order_cancel_result is True
    assert second_order_cancel_result is False


def test_cancel_a_cancelled_sell_order(limit_order_book):
    limit_order_book.place_order(
        order_id="O1", order_side="sell", order_price=1, order_quantity=1
    )
    first_order_cancel_result = limit_order_book.cancel_order(order_id="O1")
    second_order_cancel_result = limit_order_book.cancel_order(order_id="O1")
    assert first_order_cancel_result is True
    assert second_order_cancel_result is False


def test_cancel_order_not_found(limit_order_book):
    order_cancel_result = limit_order_book.cancel_order(order_id="O1")
    assert order_cancel_result is False


def test_cancel_partially_filled_buy_order(limit_order_book):
    place_buy_order_result = limit_order_book.place_order(
        order_id="O1", order_side="buy", order_price=1, order_quantity=2
    )

    place_sell_order_result = limit_order_book.place_order(
        order_id="O2", order_side="sell", order_price=1, order_quantity=1
    )

    sell_order_cancel_result = limit_order_book.cancel_order(order_id="O1")

    assert place_buy_order_result == []
    assert place_sell_order_result == [("O1", "O2", 1, Decimal("1"))]
    assert sell_order_cancel_result is True
    assert limit_order_book.buy_orders.search(-1) is None


def test_cancel_partially_filled_sell_order(limit_order_book):
    place_buy_order_result = limit_order_book.place_order(
        order_id="O1", order_side="buy", order_price=1, order_quantity=1
    )

    place_sell_order_result = limit_order_book.place_order(
        order_id="O2", order_side="sell", order_price=1, order_quantity=2
    )

    sell_order_cancel_result = limit_order_book.cancel_order(order_id="O2")

    assert place_buy_order_result == []
    assert place_sell_order_result == [("O1", "O2", 1, Decimal("1"))]
    assert sell_order_cancel_result is True
    assert limit_order_book.sell_orders.search(1) is None


def test_cancel_fully_filled_orders(limit_order_book):
    place_buy_order_result = limit_order_book.place_order(
        order_id="O1", order_side="buy", order_price=1, order_quantity=1
    )

    place_sell_order_result = limit_order_book.place_order(
        order_id="O2", order_side="sell", order_price=1, order_quantity=1
    )

    assert place_buy_order_result == []
    assert place_sell_order_result == [("O1", "O2", 1, Decimal("1"))]

    buy_order_cancel_result = limit_order_book.cancel_order(order_id="O1")
    assert buy_order_cancel_result is False

    sell_order_cancel_result = limit_order_book.cancel_order(order_id="O2")
    assert sell_order_cancel_result is False

    assert limit_order_book.buy_orders.search(-1) is None
    assert limit_order_book.sell_orders.search(1) is None

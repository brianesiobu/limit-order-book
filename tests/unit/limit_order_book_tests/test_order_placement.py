from decimal import Decimal


def test_place_buy_order(limit_order_book):
    place_order_result = limit_order_book.place_order(
        order_id="O1", order_side="buy", order_price=1, order_quantity=1
    )
    assert place_order_result == []

    buy_order = limit_order_book.buy_orders.search(
        -1
    ).value.queue.head.next.data
    assert buy_order.order_id == "O1"
    assert buy_order.order_side == "buy"
    assert buy_order.order_price == 1
    assert buy_order.order_quantity == 1

    assert len(limit_order_book.active_orders) == 1
    assert len(limit_order_book.filled_orders) == 0

    assert "O1" in limit_order_book.active_orders
    assert "O1" not in limit_order_book.filled_orders

    assert limit_order_book.active_orders["O1"][3].data == buy_order
    assert limit_order_book.active_orders["O1"][2].key == -1
    assert limit_order_book.active_orders["O1"][2].value.price == 1
    assert limit_order_book.active_orders["O1"][1] == -1
    assert limit_order_book.active_orders["O1"][0] == "buy"


def test_place_sell_order(limit_order_book):
    place_order_result = limit_order_book.place_order(
        order_id="O1", order_side="sell", order_price=1, order_quantity=1
    )
    assert place_order_result == []

    sell_order = limit_order_book.sell_orders.search(
        1
    ).value.queue.head.next.data
    assert sell_order.order_id == "O1"
    assert sell_order.order_side == "sell"
    assert sell_order.order_price == 1
    assert sell_order.order_quantity == 1

    assert len(limit_order_book.active_orders) == 1
    assert len(limit_order_book.filled_orders) == 0

    assert "O1" in limit_order_book.active_orders
    assert "O1" not in limit_order_book.filled_orders

    assert limit_order_book.active_orders["O1"][3].data == sell_order
    assert limit_order_book.active_orders["O1"][2].key == 1
    assert limit_order_book.active_orders["O1"][2].value.price == 1
    assert limit_order_book.active_orders["O1"][1] == 1
    assert limit_order_book.active_orders["O1"][0] == "sell"


def test_partial_match_with_buy_order(limit_order_book):
    limit_order_book.place_order(
        order_id="O1", order_side="buy", order_price=1, order_quantity=2
    )

    buy_order = limit_order_book.buy_orders.search(
        -1
    ).value.queue.head.next.data
    assert buy_order.order_id == "O1"
    assert buy_order.order_side == "buy"
    assert buy_order.order_price == 1
    assert buy_order.order_quantity == 2

    place_sell_order_result = limit_order_book.place_order(
        order_id="O2", order_side="sell", order_price=1, order_quantity=1
    )

    assert place_sell_order_result == [("O1", "O2", 1, Decimal("1"))]

    buy_order_after_match = limit_order_book.buy_orders.search(
        -1
    ).value.queue.head.next.data
    assert buy_order_after_match.order_id == "O1"
    assert buy_order_after_match.order_side == "buy"
    assert buy_order_after_match.order_price == 1
    assert buy_order_after_match.order_quantity == 1

    assert len(limit_order_book.active_orders) == 1
    assert len(limit_order_book.filled_orders) == 1

    assert "O2" in limit_order_book.filled_orders
    assert "O1" not in limit_order_book.filled_orders


def test_partial_match_with_sell_order(limit_order_book):
    limit_order_book.place_order(
        order_id="O1", order_side="sell", order_price=1, order_quantity=2
    )

    sell_order = limit_order_book.sell_orders.search(
        1
    ).value.queue.head.next.data
    assert sell_order.order_id == "O1"
    assert sell_order.order_side == "sell"
    assert sell_order.order_price == 1
    assert sell_order.order_quantity == 2

    place_buy_order_result = limit_order_book.place_order(
        order_id="O2", order_side="buy", order_price=1, order_quantity=1
    )

    assert place_buy_order_result == [("O2", "O1", 1, Decimal("1"))]

    sell_order_after_match = limit_order_book.sell_orders.search(
        1
    ).value.queue.head.next.data
    assert sell_order_after_match.order_id == "O1"
    assert sell_order_after_match.order_side == "sell"
    assert sell_order_after_match.order_price == 1
    assert sell_order_after_match.order_quantity == 1

    assert len(limit_order_book.active_orders) == 1
    assert len(limit_order_book.filled_orders) == 1

    assert "O2" in limit_order_book.filled_orders
    assert "O1" not in limit_order_book.filled_orders


def test_match_multiple_resting_buy_orders_with_sell_order_at_one_price(
    limit_order_book,
):
    for i in range(1, 11):
        limit_order_book.place_order(
            order_id=f"O{i}",
            order_side="buy",
            order_price=Decimal("1"),
            order_quantity=1,
        )
    matches = limit_order_book.place_order(
        order_id=f"O11",
        order_side="sell",
        order_price=Decimal("1"),
        order_quantity=10,
    )
    expected_matches = [
        ("O1", "O11", 1, Decimal("1")),
        ("O2", "O11", 1, Decimal("1")),
        ("O3", "O11", 1, Decimal("1")),
        ("O4", "O11", 1, Decimal("1")),
        ("O5", "O11", 1, Decimal("1")),
        ("O6", "O11", 1, Decimal("1")),
        ("O7", "O11", 1, Decimal("1")),
        ("O8", "O11", 1, Decimal("1")),
        ("O9", "O11", 1, Decimal("1")),
        ("O10", "O11", 1, Decimal("1")),
    ]
    assert matches == expected_matches
    assert len(limit_order_book.filled_orders) == len(expected_matches) + 1
    assert len(limit_order_book.active_orders) == 0


def test_match_multiple_resting_sell_orders_with_buy_order_at_one_price(
    limit_order_book,
):
    for i in range(1, 11):
        limit_order_book.place_order(
            order_id=f"O{i}",
            order_side="sell",
            order_price=Decimal("1"),
            order_quantity=1,
        )
    matches = limit_order_book.place_order(
        order_id=f"O11",
        order_side="buy",
        order_price=Decimal("1"),
        order_quantity=10,
    )
    expected_matches = [
        ("O11", "O1", 1, Decimal("1")),
        ("O11", "O2", 1, Decimal("1")),
        ("O11", "O3", 1, Decimal("1")),
        ("O11", "O4", 1, Decimal("1")),
        ("O11", "O5", 1, Decimal("1")),
        ("O11", "O6", 1, Decimal("1")),
        ("O11", "O7", 1, Decimal("1")),
        ("O11", "O8", 1, Decimal("1")),
        ("O11", "O9", 1, Decimal("1")),
        ("O11", "O10", 1, Decimal("1")),
    ]
    assert matches == expected_matches
    assert len(limit_order_book.filled_orders) == len(expected_matches) + 1
    assert len(limit_order_book.active_orders) == 0


def test_match_multiple_resting_buy_orders_with_sell_order(limit_order_book):
    for i in range(1, 11):
        limit_order_book.place_order(
            order_id=f"O{i}", order_side="buy", order_price=i, order_quantity=1
        )
    matches = limit_order_book.place_order(
        order_id=f"O11", order_side="sell", order_price=1, order_quantity=10
    )
    expected_matches = [
        ("O10", "O11", 1, Decimal("10")),
        ("O9", "O11", 1, Decimal("9")),
        ("O8", "O11", 1, Decimal("8")),
        ("O7", "O11", 1, Decimal("7")),
        ("O6", "O11", 1, Decimal("6")),
        ("O5", "O11", 1, Decimal("5")),
        ("O4", "O11", 1, Decimal("4")),
        ("O3", "O11", 1, Decimal("3")),
        ("O2", "O11", 1, Decimal("2")),
        ("O1", "O11", 1, Decimal("1")),
    ]
    assert matches == expected_matches
    assert len(limit_order_book.filled_orders) == len(expected_matches) + 1
    assert len(limit_order_book.active_orders) == 0


def test_match_multiple_resting_sell_orders_with_buy_order(limit_order_book):
    for i in range(1, 11):
        limit_order_book.place_order(
            order_id=f"O{i}",
            order_side="sell",
            order_price=Decimal(i),
            order_quantity=1,
        )
    matches = limit_order_book.place_order(
        order_id=f"O11", order_side="buy", order_price=10, order_quantity=10
    )
    expected_matches = [
        ("O11", "O1", 1, Decimal("1")),
        ("O11", "O2", 1, Decimal("2")),
        ("O11", "O3", 1, Decimal("3")),
        ("O11", "O4", 1, Decimal("4")),
        ("O11", "O5", 1, Decimal("5")),
        ("O11", "O6", 1, Decimal("6")),
        ("O11", "O7", 1, Decimal("7")),
        ("O11", "O8", 1, Decimal("8")),
        ("O11", "O9", 1, Decimal("9")),
        ("O11", "O10", 1, Decimal("10")),
    ]
    assert matches == expected_matches
    assert len(limit_order_book.filled_orders) == len(expected_matches) + 1
    assert len(limit_order_book.active_orders) == 0

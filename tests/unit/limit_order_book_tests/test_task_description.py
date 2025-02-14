from decimal import Decimal


def test_task_description(limit_order_book):
    # Input:  AAA Buy 10 @ 10
    # Output: OK
    output = limit_order_book.place_order(
        order_id=f"AAA",
        order_side="buy",
        order_price=Decimal("10"),
        order_quantity=10,
    )
    assert output == []

    # Input:  BBB Buy 12 @ 12
    # Output: OK
    output = limit_order_book.place_order(
        order_id=f"BBB",
        order_side="buy",
        order_price=12,
        order_quantity=12,
    )
    assert output == []

    # Input:  CCC Buy 14 @ 14
    # Output: OK
    output = limit_order_book.place_order(
        order_id=f"CCC",
        order_side="buy",
        order_price=14,
        order_quantity=14,
    )
    assert output == []

    # Input:  CCC Cancel
    # Output: OK
    output = limit_order_book.cancel_order(
        order_id=f"CCC",
    )
    assert output is True

    # Input:  DDD Sell 10 @ 15
    # Output: OK
    output = limit_order_book.place_order(
        order_id=f"DDD",
        order_side="sell",
        order_price=15,
        order_quantity=10,
    )
    assert output == []

    # Input:  EEE Sell 2 @ 12
    # Output: Fully matched with BBB (2 @ 12)
    output = limit_order_book.place_order(
        order_id=f"EEE",
        order_side="sell",
        order_price=12,
        order_quantity=2,
    )
    assert output == [("BBB", "EEE", 2, Decimal("12"))]

    # Input:  FFF Sell 4 @ 12
    # Output: Fully matched with BBB (4 @ 12)
    output = limit_order_book.place_order(
        order_id=f"EEE",
        order_side="sell",
        order_price=12,
        order_quantity=4,
    )
    assert output == [("BBB", "EEE", 4, Decimal("12"))]

    # Input:  GGG Sell 10 @ 12
    # Output: Partially matched with BBB (6 @ 12)
    output = limit_order_book.place_order(
        order_id=f"GGG",
        order_side="sell",
        order_price=12,
        order_quantity=10,
    )
    assert output == [("BBB", "GGG", 6, Decimal("12"))]

    # Input:  BBB Cancel
    # Output: Failed - already fully filled
    output = limit_order_book.cancel_order(
        order_id=f"BBB",
    )
    assert output is False

    # Input:  HHH Buy 14 @ 12
    # Output: Fully matched with GGG (4 @ 12)
    output = limit_order_book.place_order(
        order_id=f"HHH",
        order_side="buy",
        order_price=12,
        order_quantity=14,
    )
    assert output == [("HHH", "GGG", 4, Decimal("12"))]

    # Input:  KKK Sell 20 @ 10
    # Output: Fully matched with HHH (10 @ 12) and AAA (10 @ 10)
    output = limit_order_book.place_order(
        order_id=f"KKK",
        order_side="sell",
        order_price=10,
        order_quantity=20,
    )
    assert output == [
        ("HHH", "KKK", 10, Decimal("12")),
        ("AAA", "KKK", 10, Decimal("10")),
    ]

    # Input:  DDD Cancel
    # Output: OK
    output = limit_order_book.cancel_order(
        order_id=f"DDD",
    )
    assert output is True

    # Input:  DDD Cancel
    # Output: Failed – no such active order
    output = limit_order_book.cancel_order(
        order_id=f"DDD",
    )
    assert output is False

    # book is now empty on both sides
    assert limit_order_book.sell_orders.get_min() is None
    assert limit_order_book.buy_orders.get_min() is None

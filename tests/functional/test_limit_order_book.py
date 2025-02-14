import csv
from decimal import Decimal

import pytest


@pytest.mark.parametrize("test_case_id", ["00", "01", "02"])
def test_matches(limit_order_book, test_case_id):
    matches = []
    with open(
        f"tests/functional/testcase{test_case_id}/orders.csv", mode="r"
    ) as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            action, order_id, order_side, order_price, order_quantity = row

            if action == "place":
                place_order_result = limit_order_book.place_order(
                    order_id=order_id,
                    order_side=order_side,
                    order_price=Decimal(order_price),
                    order_quantity=int(order_quantity),
                )
                if place_order_result:
                    matches.extend(place_order_result)

            elif action == "cancel":
                limit_order_book.cancel_order(order_id)

    expected_matches = []
    with open(
        f"tests/functional/testcase{test_case_id}/matches.csv", mode="r"
    ) as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            buy_order_id, sell_order_id, order_price, order_quantity = row
            expected_matches.append(
                (
                    buy_order_id,
                    sell_order_id,
                    int(order_quantity),
                    Decimal(order_price),
                )
            )

    assert matches == expected_matches

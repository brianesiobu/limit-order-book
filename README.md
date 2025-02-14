# limit-order-book
A limit order book implementation in Python

## Usage
```
from decimal import Decimal
from limit_order_book.limit_order_book import LimitOrderBook

def main():
    limit_order_book = LimitOrderBook()

    limit_order_book.place_order(
        order_id="order1",
        order_side="buy",
        order_price=Decimal("99.99"),
        order_quantity=10,
    )

    matches = limit_order_book.place_order(
        order_id="order2",
        order_side="sell",
        order_price=Decimal("99.98"),
        order_quantity=5,
    )

    assert matches == [('order1', 'order2', 5, Decimal('99.99'))]

if __name__:
    main()
```

## Installation
Clone this repository, set up a new virtual environment, and install the requirements.
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt 
```

## Tests
The tests are conducted using pytest.
```
python3 -m pytest tests -vvv
```

There is a test based on the task's description.
```
tests/unit/limit_order_book_tests/test_task_description.py
```

## Benchmarks
There are 2 simple benchmarks in the repository.
```
export PYTHONPATH=src && python3 benchmarks/run_benchmark_ops.py
export PYTHONPATH=src && python3 benchmarks/run_benchmark_time.py
```

Based on these rudimentary benchmarks:

* placing an order takes approximately 4800 ns,
* cancelling an active order takes approximately 1200 ns.

The results are specific to my machine.

## Remarks
* The implementation uses two skip lists with prices as keys and FIFO queues of orders as values. This way, finding a price level can be done in `O(log P)` (on average), where `P` is the number of price levels.

* The implementation uses a doubly linked list as a FIFO queue. The benefit of this approach is that adding and removing orders at a price level can be done in `O(1)` time.

* Active orders are stored in a dictionary with pointers to linked list nodes, and filled order IDs are stored in a set. This allows cancellations to be done in `O(1)` time.

* The implementation assumes that orders are valid (i.e., order IDs are unique, prices are non-negative, and order quantities are valid, etc.).

* The implementation uses `Decimal` to store prices in order to avoid floating-point issues.

* The implementation assumes that order sizes are integers.

* Negative prices have not been tested.

* The set of filled orders will grow without bound.

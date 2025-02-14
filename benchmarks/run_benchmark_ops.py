import gc
import random
import time

from compute_statistics import compute_statistics

from limit_order_book.limit_order_book import LimitOrderBook


def benchmark_place_order(num_orders_to_place=10000):
    limit_order_book = LimitOrderBook()
    times = []

    for i in range(num_orders_to_place):
        order_id = f"O{i}"
        order_side = random.choice(["buy", "sell"])
        order_price = round(random.uniform(90, 110), 2)
        order_quantity = random.randint(1, 10)

        start = time.perf_counter_ns()
        limit_order_book.place_order(
            order_id, order_side, order_price, order_quantity
        )
        end = time.perf_counter_ns()

        times.append(end - start)

    stats = compute_statistics(times)
    print("Benchmark:          Place Order")
    print(f"Placed orders:      {stats['count']}")
    print(f"Mean Time:          {stats['mean_ns']:.2f} ns")
    print(f"Standard Deviation: {stats['stdev_ns']:.2f} ns")
    print(f"Median Time:        {stats['median_ns']:.2f} ns")
    print(f"99th Percentile:    {stats['p99_ns']:.2f} ns")


def benchmark_cancel_order(num_active_orders=10000):
    limit_order_book = LimitOrderBook()

    i = 0
    while len(limit_order_book.active_orders) < num_active_orders:
        order_id = f"O{i}"
        order_side = random.choice(["buy", "sell"])
        order_price = round(random.uniform(90, 110), 2)
        order_quantity = random.randint(1, 10)
        limit_order_book.place_order(
            order_id, order_side, order_price, order_quantity
        )
        i += 1

    orders_to_cancel = list(limit_order_book.active_orders.keys())
    random.shuffle(orders_to_cancel)

    times = []
    for order_id in orders_to_cancel:
        start = time.perf_counter_ns()
        limit_order_book.cancel_order(order_id)
        end = time.perf_counter_ns()
        times.append(end - start)

    stats = compute_statistics(times)
    print("\nBenchmark:          Cancel Order")
    print(f"Cancells:           {stats['count']}")
    print(f"Mean Time:          {stats['mean_ns']:.2f} ns")
    print(f"Standard Deviation: {stats['stdev_ns']:.2f} ns")
    print(f"Median Time:        {stats['median_ns']:.2f} ns")
    print(f"99th Percentile:    {stats['p99_ns']:.2f} ns")


def main():
    gc.disable()

    n = 100_000

    benchmark_place_order(num_orders_to_place=n)
    benchmark_cancel_order(num_active_orders=n)


if __name__ == "__main__":
    main()

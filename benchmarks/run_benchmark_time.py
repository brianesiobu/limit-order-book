import gc
import random
import time
from decimal import Decimal

from compute_statistics import compute_statistics

from limit_order_book.limit_order_book import LimitOrderBook


def main():
    gc.disable()

    benchmark_duration_seconds = 60
    print(f"Benchmark duration: {benchmark_duration_seconds} seconds")
    probability_of_placing = 1 / 3

    num_placed_orders = 0
    num_cancelled_orders = 0
    num_matched_orders = 0

    place_times = []
    cancel_times = []

    limit_order_book = LimitOrderBook()

    benchmark_start = time.time()
    while time.time() - benchmark_start < benchmark_duration_seconds:
        if random.random() < probability_of_placing:
            order_id = f"O{num_placed_orders}"
            order_side = random.choice(["buy", "sell"])
            order_price = Decimal(f"{random.uniform(90, 110):.2f}")
            order_quantity = random.randint(1, 10)
            place_start = time.perf_counter_ns()
            matches = limit_order_book.place_order(
                order_id, order_side, order_price, order_quantity
            )
            place_stop = time.perf_counter_ns()
            place_times.append(place_stop - place_start)
            # print(matches)
            # for match in matches:
            #     assert match[0] != match[1]
            num_matched_orders += len(matches)
            num_placed_orders += 1
        elif num_placed_orders > 1:
            order_id = f"O{random.randint(1, num_placed_orders)}"
            cancel_start = time.perf_counter_ns()
            cancelled = limit_order_book.cancel_order(order_id)
            cancel_stop = time.perf_counter_ns()
            cancel_times.append(cancel_stop - cancel_start)
            num_cancelled_orders += int(cancelled is True)

    place_stats = compute_statistics(place_times)
    cancel_stats = compute_statistics(cancel_times)

    print("Success!\n")
    print(f"Number of placed orders:    {num_placed_orders}")
    print(f"Number of cancelled orders: {num_cancelled_orders}")
    print(f"Number of matched orders:   {num_matched_orders}")
    print(f"Number of filled orders:    {len(limit_order_book.filled_orders)}")
    print(f"Number of active orders:    {len(limit_order_book.active_orders)}")

    print(f"\nMedian Place Time:          {place_stats['median_ns']:.2f} ns")
    print(f"Median Cancel Time:         {cancel_stats['median_ns']:.2f} ns")


if __name__ == "__main__":
    main()

import statistics


def compute_statistics(times):
    if not times:
        return None
    n = len(times)
    mean_val = statistics.mean(times)
    stdev_val = statistics.stdev(times) if n > 1 else 0
    median_val = statistics.median(times)

    sorted_times = sorted(times)
    p99_index = int(0.99 * n)
    if p99_index >= n:
        p99_index = n - 1
    p99_val = sorted_times[p99_index]

    return {
        "mean_ns": mean_val,
        "stdev_ns": stdev_val,
        "median_ns": median_val,
        "p99_ns": p99_val,
        "count": n,
    }

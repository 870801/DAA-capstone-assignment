"""Small reproducible runtime benchmark for the project's main algorithms."""
import random
import time
from .algorithms import prioritize_parcels, knapsack_select, dijkstra

def run_benchmarks(sizes=(20, 50, 100, 200), seed=7):
    rng = random.Random(seed)
    rows = []
    for n in sizes:
        parcels = [
            {"id": f"P{i:04d}", "deadline_hours": rng.randint(1, 72),
             "priority": rng.randint(1, 10), "weight": rng.randint(1, 12)}
            for i in range(n)
        ]
        t0 = time.perf_counter()
        prioritize_parcels(parcels)
        sort_ms = (time.perf_counter() - t0) * 1000

        # Keep capacity moderate so DP runtime remains practical and comparable.
        capacity = 60
        t0 = time.perf_counter()
        knapsack_select(parcels, capacity)
        knapsack_ms = (time.perf_counter() - t0) * 1000

        # Sparse connected line graph with occasional shortcuts.
        graph = {f"N{i}": {} for i in range(n)}
        for i in range(n - 1):
            a, b = f"N{i}", f"N{i+1}"
            w = rng.randint(1, 20)
            graph[a][b] = w
            graph[b][a] = w
        for i in range(0, n - 5, 5):
            a, b = f"N{i}", f"N{i+5}"
            w = rng.randint(2, 25)
            graph[a][b] = w
            graph[b][a] = w
        t0 = time.perf_counter()
        dijkstra(graph, "N0")
        dijkstra_ms = (time.perf_counter() - t0) * 1000
        rows.append({"input_size": n, "sorting_ms": sort_ms,
                     "knapsack_ms": knapsack_ms, "dijkstra_ms": dijkstra_ms})
    return rows

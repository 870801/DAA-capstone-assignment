# Mini-Courier Planner

A Python prototype that combines parcel sorting, 0/1 knapsack dynamic programming, Dijkstra shortest paths, nearest-neighbor TSP approximation, and runtime benchmarking.

## Features
- Sorts parcels by earliest deadline, then higher priority.
- Selects a high-value set of parcels within a vehicle weight capacity using 0/1 knapsack.
- Models delivery locations as a weighted, undirected graph.
- Computes shortest paths from the depot with Dijkstra's algorithm.
- Builds a delivery tour using the nearest-neighbor approximation.
- Benchmarks sorting, knapsack, and Dijkstra on increasing input sizes.

## Project structure
```text
Mini-Courier-Planner/
├── main.py
├── mini_courier_planner.ipynb
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── algorithms.py
│   └── benchmark.py
├── datasets/
│   ├── parcels.csv
│   └── routes.json
├── images/
│   ├── runtime_comparison.png
│   ├── route_graph.png
│   └── console_output.png
└── results/
    └── benchmark_results.json
```

## Requirements
- Python 3.9 or newer
- matplotlib (for charts)
- Jupyter (optional, to open the notebook)

## Setup
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
From the project root:
```bash
python main.py
```

To open the notebook:
```bash
jupyter notebook mini_courier_planner.ipynb
```

## Algorithms and complexity
- Parcel sorting: Python Timsort, O(n log n) time.
- 0/1 knapsack: O(nW) time and O(nW) table space, where W is capacity in kg.
- Dijkstra with a binary heap: O((V + E) log V) time for adjacency-list representation.
- Nearest-neighbor tour: repeatedly chooses the closest unvisited location using shortest-path calculations; this implementation is an approximation, not guaranteed optimal. Its repeated Dijkstra calls dominate runtime.

## Dataset formats
- `datasets/parcels.csv`: parcel ID, customer, deadline in hours, priority value, and weight in kg.
- `datasets/routes.json`: weighted graph and depot node. Edge weights represent illustrative distances in km.

## Notes and assumptions
- All sample values are synthetic and are for demonstration only.
- The knapsack objective maximizes the sum of parcel priority values subject to capacity. Deadline sorting determines the display/order of candidates; the knapsack objective itself is priority value.
- Dijkstra requires non-negative edge weights.
- The route graph is treated as an undirected graph because each listed road connection is represented in both directions.
- The nearest-neighbor route returns to the depot after visiting every location.

## Reproducibility
Benchmark input sizes and random seed are fixed in `src/benchmark.py`. Measured milliseconds vary by computer and current system load. The generated benchmark table is stored in `results/benchmark_results.json`.

## GitHub submission
Push the complete project folder to a private repository. Tag the final commit:
```bash
git tag v1.0-final-submission
git push origin v1.0-final-submission
```

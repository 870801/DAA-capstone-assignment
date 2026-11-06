"""Run the Mini-Courier Planner demonstration from the project root."""
import csv
import json
from pathlib import Path
from src.algorithms import (prioritize_parcels, knapsack_select, dijkstra,
                            reconstruct_path, nearest_neighbor_tour)
from src.benchmark import run_benchmarks

ROOT = Path(__file__).resolve().parent

def load_parcels():
    with (ROOT / "datasets" / "parcels.csv").open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_graph():
    raw = json.loads((ROOT / "datasets" / "routes.json").read_text(encoding="utf-8"))
    return raw["graph"], raw["depot"]

def main():
    parcels = load_parcels()
    graph, depot = load_graph()
    parcels = [{**p, "deadline_hours": int(p["deadline_hours"]),
                "priority": int(p["priority"]), "weight": int(p["weight"])}
               for p in parcels]

    ordered = prioritize_parcels(parcels)
    capacity = 18
    selected, value, _ = knapsack_select(ordered, capacity)
    tour, route_distance = nearest_neighbor_tour(graph, depot)
    distances, previous = dijkstra(graph, depot)

    print("=" * 62)
    print("                 MINI-COURIER PLANNER")
    print("=" * 62)
    print("\n1) PARCEL PRIORITIZATION (deadline, priority)")
    for p in ordered:
        print(f"  {p['id']:4} | deadline={p['deadline_hours']:2}h | "
              f"priority={p['priority']:2} | weight={p['weight']:2}kg")
    print(f"\n2) PACKING PLAN (vehicle capacity = {capacity} kg)")
    for p in selected:
        print(f"  SELECT {p['id']}  weight={p['weight']}kg  priority={p['priority']}")
    print(f"  Total weight: {sum(p['weight'] for p in selected)} kg")
    print(f"  Total priority value: {value}")
    print("\n3) SHORTEST PATHS FROM DEPOT")
    for node in graph:
        print(f"  {depot} -> {node}: {distances[node]:.1f} km")
    print("\n4) APPROXIMATE DELIVERY TOUR (nearest-neighbor)")
    print("  " + " -> ".join(tour))
    print(f"  Tour distance: {route_distance:.1f} km")
    print("\n5) SAMPLE SHORTEST PATH RECONSTRUCTION")
    target = next(node for node in graph if node != depot)
    print(f"  {depot} -> {target}: " + " -> ".join(reconstruct_path(previous, target)))
    print("\n6) RUNTIME BENCHMARKS")
    rows = run_benchmarks()
    for row in rows:
        print("  " + " | ".join(f"{k}={v:.4f}" if k.endswith("_ms")
                                else f"{k}={v}" for k, v in row.items()))
    (ROOT / "results" / "benchmark_results.json").write_text(
        json.dumps(rows, indent=2), encoding="utf-8")
    print("\nBenchmark data saved to results/benchmark_results.json")
    print("=" * 62)

if __name__ == "__main__":
    main()

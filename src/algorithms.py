"""Core algorithms for the Mini-Courier Planner."""
from __future__ import annotations
import heapq
import math
from typing import Dict, List, Tuple

def prioritize_parcels(parcels: List[dict]) -> List[dict]:
    """Stable sort: urgent deadline first, then higher priority, then smaller ID."""
    return sorted(parcels, key=lambda p: (p["deadline_hours"], -p["priority"], p["id"]))

def knapsack_select(parcels: List[dict], capacity: int):
    """0/1 knapsack DP. Returns selected parcels and maximum priority value."""
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, parcel in enumerate(parcels, start=1):
        weight, value = parcel["weight"], parcel["priority"]
        for cap in range(capacity + 1):
            dp[i][cap] = dp[i-1][cap]
            if weight <= cap:
                dp[i][cap] = max(dp[i][cap], value + dp[i-1][cap-weight])
    selected = []
    cap = capacity
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i-1][cap]:
            selected.append(parcels[i-1])
            cap -= parcels[i-1]["weight"]
    selected.reverse()
    return selected, dp[n][capacity], dp

def dijkstra(graph: Dict[str, Dict[str, float]], start: str):
    """Single-source shortest paths for a graph with non-negative edge weights."""
    distances = {node: math.inf for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    heap = [(0, start)]
    while heap:
        distance, node = heapq.heappop(heap)
        if distance != distances[node]:
            continue
        for neighbor, weight in graph[node].items():
            candidate = distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = node
                heapq.heappush(heap, (candidate, neighbor))
    return distances, previous

def reconstruct_path(previous: dict, target: str):
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous[current]
    return list(reversed(path))

def nearest_neighbor_tour(graph: dict, start: str):
    """Approximate TSP tour using nearest unvisited reachable neighbor."""
    route = [start]
    unvisited = set(graph) - {start}
    total = 0.0
    current = start
    while unvisited:
        distances, _ = dijkstra(graph, current)
        reachable = [(distances[node], node) for node in unvisited if distances[node] < math.inf]
        if not reachable:
            raise ValueError(f"Some locations are unreachable from {current}: {sorted(unvisited)}")
        distance, next_node = min(reachable)
        total += distance
        route.append(next_node)
        unvisited.remove(next_node)
        current = next_node
    distances, _ = dijkstra(graph, current)
    if distances[start] == math.inf:
        raise ValueError("Cannot return to the starting depot; graph is not strongly connected.")
    total += distances[start]
    route.append(start)
    return route, total

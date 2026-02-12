#!/usr/bin/env python3
"""
Test DLS visualization issue in detail.
"""

from grid import Grid
from algorithms import DepthLimitedSearch
from visualizer import GridVisualizer

# Smaller grid for debugging
grid = Grid(20, 20, (2, 2), (18, 18), 0.01)
grid.add_walls_randomly(50)

print("Grid: 20x20")
print("Start: (2,2), Target: (18,18)")
print("Walls:", len(grid.walls))

# Run DLS with larger depth limit
print("\nRunning DLS with depth_limit=60...")
dls = DepthLimitedSearch(grid, depth_limit=60)
result = dls.search()

print(f"\nResults:")
print(f"  Path Found: {result.found}")
print(f"  Path Length: {len(result.path)}")
print(f"  Explored: {len(result.explored)}")
print(f"  Frontier History Steps: {len(result.frontier_history)}")

if result.path:
    print(f"  Path: {result.path}")

print(f"\nFrontier history samples:")
if result.frontier_history:
    print(f"  Step 0: {len(result.frontier_history[0])} nodes")
    print(f"  Step 10: {len(result.frontier_history[10]) if len(result.frontier_history) > 10 else 'N/A'} nodes")
    print(f"  Step 50: {len(result.frontier_history[50]) if len(result.frontier_history) > 50 else 'N/A'} nodes")
    print(f"  Last step: {len(result.frontier_history[-1])} nodes")

print("\n" + "="*50)
print("Starting visualization...")
print("="*50)

visualizer = GridVisualizer(grid, animation_delay=0.02)
visualizer.visualize_algorithm("DLS Testing", result)

print("Visualization complete!")

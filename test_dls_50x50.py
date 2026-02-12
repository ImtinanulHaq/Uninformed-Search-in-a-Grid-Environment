#!/usr/bin/env python3
"""
Test DLS visualization on 50x50 grid (the default grid size).
"""

from grid import Grid
from algorithms import DepthLimitedSearch
from visualizer import GridVisualizer

# Full size grid (same as app.py default)
grid = Grid(50, 50, (5, 5), (45, 45), 0.02)
grid.add_walls_randomly(250)

print("Grid: 50x50 (default size from app.py)")
print("Start: (5,5), Target: (45,45)")
print("Walls:", len(grid.walls))
print("Dynamic obstacle probability: 0.02")

# Run DLS with depth_limit=150
print("\nRunning DLS with depth_limit=150...")
dls = DepthLimitedSearch(grid, depth_limit=150)
result = dls.search()

print(f"\nResults:")
print(f"  Path Found: {result.found}")
print(f"  Path Length: {len(result.path)}")
print(f"  Explored: {len(result.explored)}")
print(f"  Frontier History Steps: {len(result.frontier_history)}")

# Analyze frontier history
if result.frontier_history:
    frontier_sizes = [len(f) for f in result.frontier_history]
    print(f"\nFrontier Analysis:")
    print(f"  Min nodes: {min(frontier_sizes)}")
    print(f"  Max nodes: {max(frontier_sizes)}")
    print(f"  Avg nodes: {sum(frontier_sizes) / len(frontier_sizes):.1f}")
    print(f"  Total steps: {len(result.frontier_history)}")

# Check if path is valid
if result.path:
    print(f"\nPath Validation:")
    valid = True
    for i, pos in enumerate(result.path):
        if grid.is_blocked(pos):
            print(f"  ERROR at step {i}: {pos} is blocked!")
            valid = False
            break
    if valid:
        print(f"  ✓ Path is valid (all nodes unblocked)")

print("\n" + "="*50)
print("Starting visualization...")
print("Press SPACE or close window to continue")
print("="*50)

try:
    visualizer = GridVisualizer(grid, animation_delay=0.01)
    visualizer.visualize_algorithm("DLS (Depth-Limited Search)", result)
    print("\n✓ Visualization completed successfully!")
except Exception as e:
    print(f"\n✗ Visualization error: {e}")
    import traceback
    traceback.print_exc()

#!/usr/bin/env python3
"""
Test DLS on 50x50 grid without dynamic obstacles to isolate the issue.
"""

from grid import Grid
from algorithms import DepthLimitedSearch
from visualizer import GridVisualizer

# Full size grid WITHOUT dynamic obstacles
grid = Grid(50, 50, (5, 5), (45, 45), 0.0)  # No dynamic obstacles
grid.add_walls_randomly(250)

print("Grid: 50x50 (NO dynamic obstacles)")
print("Start: (5,5), Target: (45,45)")
print("Walls:", len(grid.walls))
print("Dynamic obstacle probability: 0.0 (disabled)")

# Run DLS with depth_limit=150
print("\nRunning DLS with depth_limit=150...")
dls = DepthLimitedSearch(grid, depth_limit=150)
result = dls.search()

print(f"\nResults:")
print(f"  Path Found: {result.found}")
print(f"  Path Length: {len(result.path)}")
print(f"  Explored: {len(result.explored)}")
print(f"  Frontier History Steps: {len(result.frontier_history)}")

# Check if path is valid
if result.path:
    print(f"\nPath Validation:")
    valid = True
    for i, pos in enumerate(result.path):
        if grid.is_blocked(pos):
            print(f"  ✗ ERROR at step {i}: {pos} is blocked!")
            print(f"    Walls: {pos in grid.walls}")
            valid = False
            break
    if valid:
        print(f"  ✓ Path is VALID (all {len(result.path)} nodes unblocked)")
else:
    print("  No path returned")

print("\n" + "="*50)
print("Starting visualization...")
print("="*50)

try:
    visualizer = GridVisualizer(grid, animation_delay=0.01)
    visualizer.visualize_algorithm("DLS (Depth-Limited Search)", result)
    print("\n✓ Visualization completed successfully!")
except Exception as e:
    print(f"\n✗ Visualization error: {e}")
    import traceback
    traceback.print_exc()

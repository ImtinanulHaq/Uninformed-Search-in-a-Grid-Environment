"""
Test IDDFS specifically without dynamic obstacles
"""

from grid import Grid
from algorithms import IterativeDeepeningDFS

print("\nTesting IDDFS with NO dynamic obstacles")
print("=" * 70)

# Create test grid with NO dynamic obstacles
grid = Grid(30, 30, (2, 2), (28, 28), dynamic_spawn_probability=0.0)
grid.add_walls_randomly(100)

print(f"Grid created: {len(grid.walls)} walls")
print(f"Start: {grid.start}, Target: {grid.target}")
print(f"Dynamic obstacles spawn probability: {grid.dynamic_spawn_probability}")

# Test IDDFS
algo = IterativeDeepeningDFS(grid)
result = algo.search()

print(f"\nResults:")
print(f"  Found: {result.found}")
if result.path:
    print(f"  Path length: {len(result.path)}")
    print(f"  Path: {result.path[:3]}...{result.path[-3:]}")
print(f"  Nodes explored: {result.total_nodes_explored}")
print(f"  Explored size: {len(result.explored)}")
print(f"  Frontier history length: {len(result.frontier_history)}")
print(f"  Dynamic obstacles: {len(result.dynamic_obstacles_encountered)}")

if result.found and result.path:
    # Verify path
    assert result.path[0] == grid.start, "Path start incorrect"
    assert result.path[-1] == grid.target, "Path end incorrect"
    print(f"  ✓ Path verified")
else:
    print(f"  ✗ Path NOT found even without dynamic obstacles!")
    print(f"  This suggests an issue with IDDFS logic")

print("=" * 70)

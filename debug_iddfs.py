"""
Debug IDDFS to find the issue
"""

from grid import Grid
from algorithms import IterativeDeepeningDFS

print("\nDEBUGGING IDDFS")
print("=" * 70)

# Create small test grid first
grid = Grid(10, 10, (1, 1), (8, 8), dynamic_spawn_probability=0.0)
grid.add_walls_randomly(15)

print(f"Small grid test: 10×10 with 15 walls")
print(f"Start: {grid.start}, Target: {grid.target}")

algo = IterativeDeepeningDFS(grid)

# Manually test _dls_recursive for small depths
print(f"\nManual testing _dls_recursive:")
print(f"  Manhattan distance to target: {grid.get_heuristic_distance(grid.start)}")

for test_limit in [2, 4, 6, 8]:
    algo.explored.clear()
    algo.parent_map.clear()
    algo.parent_map[grid.start] = None
    
    found, path = algo._dls_recursive(grid.start, test_limit, None)
    
    print(f"\n  Depth limit {test_limit}:")
    print(f"    Found: {found}")
    if found:
        print(f"    Path length: {len(path)}")
        print(f"    Path: {path[:3]}...{path[-3:] if len(path) > 6 else path}")
    print(f"    Nodes explored: {len(algo.explored)}")

# Now test full IDDFS
print(f"\nFull IDDFS run:")
algo = IterativeDeepeningDFS(grid)
result = algo.search()
print(f"  Found: {result.found}")
if result.path:
    print(f"  Path length: {len(result.path)}")
    print(f"  Path: {result.path}")
print(f"  Nodes explored: {len(result.explored)}")

print("=" * 70)

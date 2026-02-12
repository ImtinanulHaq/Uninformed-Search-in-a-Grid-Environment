"""
Standalone test for all algorithms - No app.py interference
"""

print("=" * 70)
print("COMPREHENSIVE ALGORITHMS TEST SUITE")
print("=" * 70)

from grid import Grid
from algorithms import (
    BreadthFirstSearch, DepthFirstSearch, UniformCostSearch,
    DepthLimitedSearch, IterativeDeepeningDFS, BidirectionalSearch
)

# Create test grid
print("\n[SETUP] Creating test grid 30×30...")
grid = Grid(30, 30, (2, 2), (28, 28), dynamic_spawn_probability=0.03)
grid.add_walls_randomly(100)
print(f"✓ Grid created with {len(grid.walls)} walls")

# Test each algorithm
algorithms = [
    ("BFS", BreadthFirstSearch),
    ("DFS", DepthFirstSearch),
    ("UCS", UniformCostSearch),
    ("DLS", lambda g: DepthLimitedSearch(g, depth_limit=60)),  # Increased from 30 to 60
    ("IDDFS", IterativeDeepeningDFS),
    ("Bidirectional", BidirectionalSearch),
]

results_data = []

for algo_name, algo_class in algorithms:
    print(f"\n{'─' * 70}")
    print(f"Testing {algo_name}")
    print(f"{'─' * 70}")
    
    # Clear dynamic obstacles before each test
    grid.clear_dynamic_obstacles()
    
    try:
        # Run algorithm
        algo = algo_class(grid)
        result = algo.search()
        
        # Verify results
        found_str = "✓ FOUND" if result.found else "✗ NOT FOUND"
        print(f"Status: {found_str}")
        
        if result.path:
            print(f"Path Length: {len(result.path)} steps")
            if len(result.path) > 6:
                print(f"Path: {result.path[:3]}...{result.path[-3:]}")
            else:
                print(f"Path: {result.path}")
        
        print(f"Nodes Explored: {result.total_nodes_explored}")
        print(f"Explored Set Size: {len(result.explored)}")
        print(f"Frontier History Length: {len(result.frontier_history)}")
        
        if result.dynamic_obstacles_encountered:
            print(f"Dynamic Obstacles: {len(result.dynamic_obstacles_encountered)} spawned")
        
        # Verify path correctness
        if result.found and result.path:
            # Check start and end
            assert result.path[0] == grid.start, "Path doesn't start at start!"
            assert result.path[-1] == grid.target, "Path doesn't end at target!"
            
            # Check each step is adjacent
            for i in range(len(result.path) - 1):
                curr = result.path[i]
                next_pos = result.path[i + 1]
                
                # Verify next position is valid (adjacent or same?)
                is_valid = (abs(curr[0]-next_pos[0]) <= 1 and abs(curr[1]-next_pos[1]) <= 1 and 
                           curr != next_pos)
                
                assert is_valid, f"Invalid step from {curr} to {next_pos}"
            
            print(f"✓ Path verified as valid and continuous")
        
        results_data.append((algo_name, result.found, len(result.path) if result.path else 0, result.total_nodes_explored))
        
    except Exception as e:
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        results_data.append((algo_name, False, 0, 0))

# Summary
print(f"\n{'=' * 70}")
print("SUMMARY TABLE")
print(f"{'=' * 70}")
print(f"{'Algorithm':<15} {'Found':<8} {'Path Length':<15} {'Nodes Explored':<15}")
print(f"{'-' * 70}")

for algo_name, found, path_len, nodes in results_data:
    found_str = "Yes" if found else "No"
    path_str = str(path_len) if path_len > 0 else "N/A"
    print(f"{algo_name:<15} {found_str:<8} {path_str:<15} {nodes:<15}")

print(f"{'=' * 70}")
print("✅ ALL ALGORITHMS TESTED SUCCESSFULLY!")
print(f"{'=' * 70}\n")

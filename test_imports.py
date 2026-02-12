"""
Test Script - Verify all modules load correctly
"""

print("Testing imports...\n")

try:
    print("✓ Importing grid module...")
    from grid import Grid, CellType
    
    print("✓ Importing algorithms...")
    from algorithms import (
        BreadthFirstSearch, DepthFirstSearch, UniformCostSearch,
        DepthLimitedSearch, IterativeDeepeningDFS, BidirectionalSearch,
        SearchResult, SearchAlgorithm
    )
    
    print("✓ Importing visualizer...")
    from visualizer import GridVisualizer, Colors
    
    print("✓ Importing app...")
    from app import GridPathfinder
    
    print("\n" + "="*60)
    print("✓ ALL IMPORTS SUCCESSFUL!")
    print("="*60)
    
    print("\nCreating test grid...")
    test_grid = Grid(20, 20, (2, 2), (18, 18), dynamic_spawn_probability=0.02)
    print(f"✓ Grid created: {test_grid.width}×{test_grid.height}")
    print(f"✓ Start: {test_grid.start}, Target: {test_grid.target}")
    
    print("\nAdding random walls...")
    test_grid.add_walls_randomly(50)
    print(f"✓ Added {len(test_grid.walls)} walls")
    
    print("\nTesting algorithms...")
    
    # Test BFS
    print("\n  Testing BFS...")
    bfs = BreadthFirstSearch(test_grid)
    result = bfs.search()
    print(f"  ✓ BFS completed - Path: {len(result.path) if result.path else 0}, Explored: {result.total_nodes_explored}")
    
    # Clear for next algorithm
    test_grid.dynamic_obstacles.clear()
    
    # Test DFS
    print("  Testing DFS...")
    dfs = DepthFirstSearch(test_grid)
    result = dfs.search()
    print(f"  ✓ DFS completed - Path: {len(result.path) if result.path else 0}, Explored: {result.total_nodes_explored}")
    
    # Clear for next algorithm
    test_grid.dynamic_obstacles.clear()
    
    # Test UCS
    print("  Testing UCS...")
    ucs = UniformCostSearch(test_grid)
    result = ucs.search()
    print(f"  ✓ UCS completed - Path: {len(result.path) if result.path else 0}, Explored: {result.total_nodes_explored}")
    
    print("\n" + "="*60)
    print("✓ ALL TESTS PASSED SUCCESSFULLY!")
    print("="*60)
    print("\nApplication is ready to run!")
    print("Run: python app.py")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

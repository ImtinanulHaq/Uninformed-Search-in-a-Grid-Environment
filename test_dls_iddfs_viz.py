#!/usr/bin/env python3
"""
Test DLS and IDDFS visualization.
This script tests if visualization is rendering correctly for DLS and IDDFS algorithms.
"""

import sys
sys.path.insert(0, '/home/muhammad-imtinan-ul-haq/Desktop/Uninformed Search in a Grid Environment')

from grid import Grid
from algorithms import DepthLimitedSearch, IterativeDeepeningDFS
from visualizer import GridVisualizer

def test_dls_visualization():
    """Test DLS visualization."""
    print("\n" + "="*60)
    print("TEST: DLS (Depth-Limited Search) Visualization")
    print("="*60)
    
    # Create grid
    grid = Grid(30, 30, (2, 2), (28, 28), 0.02)
    grid.add_walls_randomly(100)
    
    print(f"✓ Grid created: 30×30, Walls: {len(grid.walls)}")
    print(f"  Start: (2,2), Target: (28,28)")
    
    # Run DLS
    print("\nExecuting DLS search...")
    dls = DepthLimitedSearch(grid, depth_limit=60)  # Increased to find paths on 30x30 grids
    result = dls.search()
    
    # Print results
    print(f"\n📊 DLS Results:")
    print(f"  Path Found: {result.found}")
    if result.found:
        print(f"  Path Length: {len(result.path)}")
    print(f"  Nodes Explored: {len(result.explored)}")
    print(f"  Dynamic Obstacles Encountered: {len(result.dynamic_obstacles_encountered)}")
    
    # Print path details
    if result.path:
        print(f"\n  Path: {result.path[:5]} ... {result.path[-5:] if len(result.path) > 5 else result.path}")
        
        # Validate path
        valid = True
        for i, pos in enumerate(result.path):
            if grid.is_blocked(pos):
                print(f"  ✗ ERROR: Position {pos} at index {i} is blocked!")
                valid = False
                break
        if valid:
            print(f"  ✓ Path validation passed (no walls)")
    
    # Visualize
    print("\n" + "-"*60)
    print("Starting DLS visualization...")
    print("Press SPACE to close window when ready")
    print("-"*60)
    
    try:
        visualizer = GridVisualizer(grid, animation_delay=0.01)
        visualizer.visualize_algorithm("DLS (Depth-Limited Search)", result)
        print("✓ DLS visualization completed successfully")
    except Exception as e:
        print(f"✗ DLS Visualization Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_iddfs_visualization():
    """Test IDDFS visualization."""
    print("\n" + "="*60)
    print("TEST: IDDFS (Iterative Deepening DFS) Visualization")
    print("="*60)
    
    # Create grid
    grid = Grid(30, 30, (2, 2), (28, 28), 0.02)
    grid.add_walls_randomly(100)
    
    print(f"✓ Grid created: 30×30, Walls: {len(grid.walls)}")
    print(f"  Start: (2,2), Target: (28,28)")
    
    # Run IDDFS
    print("\nExecuting IDDFS search...")
    iddfs = IterativeDeepeningDFS(grid)
    result = iddfs.search()
    
    # Print results
    print(f"\n📊 IDDFS Results:")
    print(f"  Path Found: {result.found}")
    if result.found:
        print(f"  Path Length: {len(result.path)}")
    print(f"  Nodes Explored: {len(result.explored)}")
    print(f"  Dynamic Obstacles Encountered: {len(result.dynamic_obstacles_encountered)}")
    
    # Print path details
    if result.path:
        print(f"\n  Path: {result.path[:5]} ... {result.path[-5:] if len(result.path) > 5 else result.path}")
        
        # Validate path
        valid = True
        for i, pos in enumerate(result.path):
            if grid.is_blocked(pos):
                print(f"  ✗ ERROR: Position {pos} at index {i} is blocked!")
                valid = False
                break
        if valid:
            print(f"  ✓ Path validation passed (no walls)")
    
    # Visualize
    print("\n" + "-"*60)
    print("Starting IDDFS visualization...")
    print("Press SPACE to close window when ready")
    print("-"*60)
    
    try:
        visualizer = GridVisualizer(grid, animation_delay=0.01)
        visualizer.visualize_algorithm("IDDFS (Iterative Deepening DFS)", result)
        print("✓ IDDFS visualization completed successfully")
    except Exception as e:
        print(f"✗ IDDFS Visualization Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  DLS & IDDFS VISUALIZATION TEST".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    dls_ok = test_dls_visualization()
    iddfs_ok = test_iddfs_visualization()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"DLS Visualization:   {'✓ PASSED' if dls_ok else '✗ FAILED'}")
    print(f"IDDFS Visualization: {'✓ PASSED' if iddfs_ok else '✗ FAILED'}")
    print("="*60)

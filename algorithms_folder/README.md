# Algorithms Folder

Each algorithm is implemented as a separate file for easy understanding and learning.

## Files

- **bfs.py** - Breadth-First Search
- **dfs.py** - Depth-First Search  
- **ucs.py** - Uniform Cost Search
- **dls.py** - Depth-Limited Search
- **iddfs.py** - Iterative Deepening DFS
- **bidirectional.py** - Bidirectional Search

## How to Use

Each algorithm class has the same interface:

```python
from grid import Grid
from algorithms_folder.bfs import BFS

grid = Grid(50, 50, (5, 5), (45, 45), 0.0)
grid.add_walls_randomly(250)

algorithm = BFS(grid)
result = algorithm.search()

print(f"Path found: {result['found']}")
print(f"Path length: {len(result['path'])}")
print(f"Nodes explored: {len(result['explored'])}")
```

## Understanding the Code

Each algorithm file is kept simple and easy to understand:
- No complex comments
- Clear variable names
- Direct logic flow
- Standard search patterns

Read the code to understand how each algorithm works!

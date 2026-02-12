# Uninformed Search in a Grid Environment

**AI Pathfinder with Dynamic Obstacles and Real-time Visualization**

This project implements six fundamental uninformed search algorithms to navigate a grid from a Start Point (S) to a Target Point (T) while avoiding static walls and handling dynamic obstacles that may appear during the search.

## Table of Contents

- [Features](#features)
- [Algorithms Implemented](#algorithms-implemented)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Algorithm Overview](#algorithm-overview)
- [Results and Analysis](#results-and-analysis)

## Features

✅ **Six Uninformed Search Algorithms**
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Uniform Cost Search (UCS)
- Depth-Limited Search (DLS)
- Iterative Deepening DFS (IDDFS)
- Bidirectional Search

✅ **Professional GUI Visualization**
- Real-time step-by-step animation
- Color-coded visualization (walls, explored nodes, frontier, final path)
- Live performance metrics
- Progress tracking

✅ **Dynamic Obstacles**
- Random obstacles that may spawn during search
- Automatic re-planning when obstacles block the path
- Configurable spawn probability

✅ **Professional Codebase**
- Well-documented with detailed comments
- Modular architecture
- Object-oriented design
- Type hints throughout

## Algorithms Implemented

### 1. **Breadth-First Search (BFS)**
- **Explores:** Level by level (explores nodes closest to start first)
- **Guarantees:** Shortest path in unweighted graphs
- **Time Complexity:** O(V + E)
- **Space Complexity:** O(V)
- **Best for:** Finding shortest paths

### 2. **Depth-First Search (DFS)**
- **Explores:** As far as possible along each branch before backtracking
- **Guarantees:** Complete (will find solution if it exists)
- **Time Complexity:** O(V + E)
- **Space Complexity:** O(V)
- **Best for:** Topological sorting, detecting cycles
- **Note:** May not find shortest path

### 3. **Uniform Cost Search (UCS)**
- **Explores:** Nodes with lowest path cost first
- **Guarantees:** Optimal cost path
- **Time Complexity:** O((V + E) * log V)
- **Space Complexity:** O(V)
- **Best for:** Weighted graphs, minimum cost paths

### 4. **Depth-Limited Search (DLS)**
- **Explores:** DFS with maximum depth limit
- **Guarantees:** Complete if solution is within depth limit
- **Time Complexity:** O(b^l) where b=branching factor, l=depth limit
- **Space Complexity:** O(b * l)
- **Best for:** Preventing infinite loops, limiting search scope

### 5. **Iterative Deepening DFS (IDDFS)**
- **Explores:** Multiple DFS iterations with increasing depth limits
- **Guarantees:** Shortest path + DFS space efficiency
- **Time Complexity:** O(b^d) where d=solution depth
- **Space Complexity:** O(b * d)
- **Best for:** Unknown solution depth, memory-constrained systems

### 6. **Bidirectional Search**
- **Explores:** Simultaneously from start and target
- **Guarantees:** Optimal path, reduced search space
- **Time Complexity:** O(b^(d/2))
- **Space Complexity:** O(b^(d/2))
- **Best for:** Dense graphs, when both endpoints are known

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/ImtinanulHaq/Uninformed-Search-in-a-Grid-Environment.git
cd Uninformed-Search-in-a-Grid-Environment
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pygame
```

### Step 3: Verify Installation

```bash
python -c "import pygame; print('✓ Pygame installed successfully')"
```

## Usage

### Basic Usage (Interactive Menu)

Run the application with the interactive menu:

```bash
python app.py
```

This will present you with a menu to:
1. Run individual algorithms (BFS, DFS, UCS, DLS, IDDFS, Bidirectional)
2. Run all algorithms and compare results
3. Create a new grid with custom parameters
4. Exit

### Running a Specific Algorithm

You can also run a specific algorithm from Python:

```python
from app import GridPathfinder

# Create pathfinder with custom grid
pathfinder = GridPathfinder(
    width=50,
    height=50,
    start=(5, 5),
    target=(45, 45),
    num_walls=250,
    dynamic_obstacle_probability=0.02
)

# Run a specific algorithm
pathfinder.run_algorithm("BFS", show_visualization=True)
```

### Running All Algorithms (Comparison Mode)

```python
pathfinder.run_all_algorithms(show_visualization=True)
```

## Configuration

### Grid Parameters

You can modify the grid parameters in `app.py`:

```python
pathfinder = GridPathfinder(
    width=50,                              # Grid width in cells
    height=50,                             # Grid height in cells
    start=(5, 5),                          # Start position (x, y)
    target=(45, 45),                       # Target position (x, y)
    num_walls=250,                         # Number of static walls
    dynamic_obstacle_probability=0.02      # Probability of obstacle spawn (0.0-1.0)
)
```

### Visualization Parameters

In `visualizer.py`, you can adjust:

```python
visualizer = GridVisualizer(
    grid=grid,
    window_width=1200,                     # Display window width
    animation_delay=0.02,                  # Delay between animation frames (seconds)
    show_dynamic_obstacles=True            # Show dynamic obstacles during visualization
)
```

### Movement Order

The application follows this strict movement order when expanding nodes:

```
1. Up (0, -1)
2. Right (+1, 0)
3. Down (0, +1)
4. Bottom-Right (+1, +1) - Diagonal
5. Left (-1, 0)
6. Top-Left (-1, -1) - Diagonal
7. Top-Right (+1, -1) - Diagonal
8. Bottom-Left (-1, +1) - Diagonal
```

## Project Structure

```
Uninformed-Search-in-a-Grid-Environment/
├── app.py                 # Main application (entry point)
├── grid.py               # Grid management and obstacle handling
├── algorithms.py         # All 6 search algorithm implementations
├── visualizer.py         # GUI visualization using Pygame
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .gitignore           # Git ignore file
```

### File Descriptions

- **app.py**: Main application orchestrating grid creation, algorithm execution, and visualization
- **grid.py**: Defines Grid class with wall/obstacle management and neighbor calculation
- **algorithms.py**: Implements all 6 search algorithms with SearchResult class
- **visualizer.py**: Professional GUI using Pygame for real-time algorithm visualization

## Algorithm Overview

### How Each Algorithm Works

#### BFS (Breadth-First Search)
```
1. Add start node to queue
2. While queue is not empty:
   - Dequeue node from front
   - If node is target, return path
   - Add all unvisited neighbors to back of queue
3. If queue empties, no path exists
```

**Visualization:** Expands in concentric "waves" from start point

#### DFS (Depth-First Search)
```
1. Add start node to stack
2. While stack is not empty:
   - Pop node from top
   - If node is target, return path
   - Add all unvisited neighbors to top of stack
3. If stack empties, no path exists
```

**Visualization:** Explores deep into one branch before backtracking

#### UCS (Uniform Cost Search)
```
1. Add start node to priority queue with cost 0
2. While priority queue is not empty:
   - Pop node with minimum cost
   - If node is target, return path
   - For each neighbor:
     - Calculate new cost
     - If cost is better than known, add to queue
3. If queue empties, no path exists
```

**Visualization:** Expands nodes in order of total path cost

#### DLS (Depth-Limited Search)
```
1. Add (start node, depth 0) to stack
2. While stack is not empty:
   - Pop (node, depth) from stack
   - If node is target, return path
   - If depth < limit:
     - Add all unvisited neighbors with (depth + 1) to stack
3. If stack empties, no path exists (or exceeds depth limit)
```

**Visualization:** Similar to DFS but stops at max depth

#### IDDFS (Iterative Deepening DFS)
```
For depth_limit = 1, 2, 3, ...:
  1. Perform DFS with current depth limit
  2. If target found, return path
  3. If not found, increase depth limit
```

**Visualization:** Repeats DFS pattern with increasing depth

#### Bidirectional Search
```
1. Create two search frontiers: from start and from target
2. Alternate expanding each frontier level by level
3. When a frontier encounters a node from the other frontier:
   - Meeting point found
   - Reconstruct path from start → meeting point → target
```

**Visualization:** Shows expansion from both ends meeting in middle

## Visualization Guide

### Color Coding

- 🟢 **Green:** Start position (S)
- 🔴 **Red:** Target position (T)
- ⬜ **Dark Gray:** Static walls
- 🟦 **Light Blue:** Explored nodes (visited)
- 🟨 **Yellow:** Frontier nodes (waiting to be explored)
- 🟦 **Blue:** Final shortest path
- 🟠 **Orange:** Dynamic obstacles

### GUI Features

1. **Real-time Animation:** Watch the algorithm explore step-by-step
2. **Live Metrics:** See current statistics as search progresses
3. **Progress Bar:** Track overall progress
4. **Legend:** Color guide always visible
5. **Performance Display:** Shows path length, nodes explored, obstacles encountered

## Results and Analysis

### Performance Comparison

Typical results on a 50×50 grid with 250 walls:

| Algorithm | Path Found | Path Length | Nodes Explored | Memory Efficient |
|-----------|-----------|------------|-----------------|-----------------|
| BFS | Usually | Shortest | High | Yes |
| DFS | Usually | Not Shortest | Medium | Yes |
| UCS | Usually | Optimal | Medium | Yes |
| DLS | Usually* | Not Shortest | Low | Yes |
| IDDFS | Usually | Shortest | High | Yes |
| Bidirectional | Usually | Shortest | Very Low | Yes |

*Depends on depth limit setting

### Best/Worst Case Scenarios

**Best Case:** Target is close to start and easily reachable
- BFS and Bidirectional will find it quickly with fewest nodes explored

**Worst Case:** Target is blocked or very far away
- BFS/IDDFS will explore entire reachable grid
- DFS might explore deep branches inefficiently
- Bidirectional significantly reduces exploration

## Testing Scenarios

The application includes test modes:

1. **Small Grid Test** (10×10): Quick testing
2. **Medium Grid Test** (30×30): Balanced testing
3. **Large Grid Test** (50×50): Performance testing
4. **Dense Obstacles** (High wall count): Difficulty testing
5. **Dynamic Environment** (High obstacle spawn rate): Real-time adaptation testing

## Troubleshooting

### "ModuleNotFoundError: No module named 'pygame'"
Solution: Install pygame
```bash
pip install pygame
```

### "Invalid grid position"
Solution: Ensure start and target positions are different and not on walls

### Algorithm runs very slowly
Solution: Reduce grid size or number of walls, increase animation delay

### Window closes immediately
Solution: Run from command line to see error messages
```bash
python app.py
```

## Contributing

To improve this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided for educational purposes.

## Author

Created as part of an AI Pathfinding assignment demonstrating uninformed search algorithms.

## References

- Russell, S. J., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to Algorithms
- Pygame Documentation: https://www.pygame.org/

---

**Happy Pathfinding!** 🤖🗺️

For any issues or questions, please open an issue on the GitHub repository.

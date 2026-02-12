"""
Grid Management Module

This module handles the grid representation, obstacle management, and dynamic obstacle spawning.
It provides the foundation for all search algorithms to work on.
"""

import random
from typing import List, Tuple, Set
from dataclasses import dataclass
from enum import Enum


class CellType(Enum):
    """
    Enumeration for different cell types in the grid.
    
    Each cell type represents a different state or element in the pathfinding grid.
    This helps visualization and tracking of algorithm progression.
    """
    EMPTY = 0       # Unvisited, walkable cell
    WALL = 1        # Static obstacle that blocks movement
    START = 2       # Starting position of the pathfinder
    TARGET = 3      # Goal/destination position
    EXPLORED = 4    # Cell already visited by the algorithm
    FRONTIER = 5    # Cell waiting to be explored (in queue/stack)
    PATH = 6        # Cell that is part of the final solution path


@dataclass
class Cell:
    """
    Represents a single cell in the grid.
    
    Using @dataclass decorator for clean, minimal boilerplate.
    Provides automatic __init__, __repr__, and __eq__ methods.
    """
    x: int                                    # X-coordinate (column) of the cell
    y: int                                    # Y-coordinate (row) of the cell
    cell_type: CellType = CellType.EMPTY      # Type of cell (empty, wall, start, etc.)
    
    def __hash__(self):
        """Make cell hashable so it can be added to sets and used in dictionaries."""
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        """
        Compare two cells for equality.
        Cells are equal if their coordinates match, regardless of cell_type.
        """
        if not isinstance(other, Cell):
            return False
        return self.x == other.x and self.y == other.y


class Grid:
    """
    Manages the complete grid environment for pathfinding algorithms.
    
    This class handles:
    - Static walls (permanent obstacles)
    - Dynamic obstacles (appear randomly during search)
    - Valid position checking and neighbor calculation
    - Movement order according to specs (8-directional with diagonals)
    
    Attributes:
        width (int): Grid width in cells
        height (int): Grid height in cells
        start (Tuple[int, int]): Starting position (x, y)
        target (Tuple[int, int]): Target position (x, y)
        walls (Set[Tuple[int, int]]): Set of static wall positions
        dynamic_obstacles (Set[Tuple[int, int]]): Dynamic obstacles appearing during search
        dynamic_spawn_probability (float): Probability (0-1) of obstacle spawn per step
    """
    
    def __init__(self, width: int, height: int, start: Tuple[int, int], 
                 target: Tuple[int, int], dynamic_spawn_probability: float = 0.02):
        """
        Initialize the grid environment.
        
        Args:
            width (int): Grid width in cells
            height (int): Grid height in cells
            start (Tuple[int, int]): Starting position as (x, y) tuple
            target (Tuple[int, int]): Target position as (x, y) tuple
            dynamic_spawn_probability (float): Probability of obstacle spawn per step [0.0 to 1.0]
        
        Raises:
            ValueError: If start or target position is out of bounds
        """
        # Initialize basic grid parameters
        self.width = width
        self.height = height
        self.start = start
        self.target = target
        
        # Initialize obstacle collections
        self.walls: Set[Tuple[int, int]] = set()                    # Static permanent walls
        self.dynamic_obstacles: Set[Tuple[int, int]] = set()        # Temporary dynamic obstacles
        self.dynamic_spawn_probability = dynamic_spawn_probability  # Spawn chance per iteration
        
        # Validate that start and target are within grid bounds
        if not self._is_valid_position(start):
            raise ValueError(f"Start position {start} is out of grid bounds ({width}×{height})")
        if not self._is_valid_position(target):
            raise ValueError(f"Target position {target} is out of grid bounds ({width}×{height})")
    
    def _is_valid_position(self, pos: Tuple[int, int]) -> bool:
        """
        Check if a position is within grid boundaries.
        
        Args:
            pos (Tuple[int, int]): Position to validate as (x, y)
        
        Returns:
            bool: True if position is within bounds, False otherwise
        """
        x, y = pos
        # Check both x and y are within valid range [0, width) and [0, height)
        return 0 <= x < self.width and 0 <= y < self.height
    
    def add_wall(self, x: int, y: int) -> None:
        """
        Add a static wall at the given position.
        
        Walls cannot be placed at start or target positions.
        
        Args:
            x (int): X-coordinate of wall
            y (int): Y-coordinate of wall
        """
        pos = (x, y)
        # Only add wall if position is valid and not start/target
        if self._is_valid_position(pos) and pos != self.start and pos != self.target:
            self.walls.add(pos)
    
    def add_walls_randomly(self, count: int) -> None:
        """
        Add random static walls to the grid.
        
        Uses random placement with a maximum attempt limit to prevent
        infinite loops if grid is too saturated with walls.
        
        Args:
            count (int): Number of random walls to add
        """
        # Calculate max attempts to prevent infinite loop (10x the target count)
        max_attempts = count * 10
        added = 0
        attempts = 0
        
        # Keep trying to add walls until we reach target count or max attempts
        while added < count and attempts < max_attempts:
            # Generate random coordinates
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            pos = (x, y)
            
            # Check if position is available (not wall, not start, not target)
            if pos not in self.walls and pos != self.start and pos != self.target:
                self.add_wall(x, y)
                added += 1
            
            attempts += 1
    
    def spawn_dynamic_obstacle(self) -> Tuple[int, int] | None:
        """
        Randomly spawn a dynamic obstacle during search.
        
        Probability-based spawning mechanism. If spawn occurs, obstacle
        appears at random empty location (not wall, start, or target).
        
        Returns:
            Tuple[int, int] | None: Position of new obstacle or None if none spawned
        """
        # Check if dynamic obstacle should spawn based on probability
        if random.random() > self.dynamic_spawn_probability:
            return None
        
        # Collect all empty cells available for obstacle placement
        empty_cells = []
        for x in range(self.width):
            for y in range(self.height):
                pos = (x, y)
                # Cell is empty if: not wall, not dynamic obstacle, not start, not target
                if (pos not in self.walls and 
                    pos not in self.dynamic_obstacles and 
                    pos != self.start and 
                    pos != self.target):
                    empty_cells.append(pos)
        
        # Place obstacle at random empty location if available
        if empty_cells:
            new_obstacle = random.choice(empty_cells)
            self.dynamic_obstacles.add(new_obstacle)
            return new_obstacle
        
        # No empty space available
        return None
    
    def is_blocked(self, pos: Tuple[int, int]) -> bool:
        """
        Check if a position is blocked by static or dynamic obstacles.
        
        A position is blocked if:
        - It's outside grid boundaries
        - It contains a static wall
        - It contains a dynamic obstacle
        
        Args:
            pos (Tuple[int, int]): Position to check as (x, y)
        
        Returns:
            bool: True if position is blocked, False if walkable
        """
        x, y = pos
        # First check if position is within valid grid bounds
        if not self._is_valid_position(pos):
            return True  # Out of bounds is always blocked
        # Check for static walls or dynamic obstacles
        return pos in self.walls or pos in self.dynamic_obstacles
    
    def clear_dynamic_obstacles(self) -> None:
        """
        Clear all dynamic obstacles.
        
        Useful for resetting search state or preparing for a new algorithm run.
        Static walls are preserved and not cleared.
        """
        self.dynamic_obstacles.clear()
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Get valid neighbors in strict movement order.
        
        Expansion order (as specified in assignment):
        1. Up          (0, -1)
        2. Right       (+1, 0)
        3. Down        (0, +1)
        4. BottomRight (+1, +1) - Diagonal
        5. Left        (-1, 0)
        6. TopLeft     (-1, -1) - Diagonal
        7. TopRight    (+1, -1) - Diagonal
        8. BottomLeft  (-1, +1) - Diagonal
        
        Args:
            pos (Tuple[int, int]): Position (x, y) to find neighbors for
        
        Returns:
            List[Tuple[int, int]]: List of valid unblocked neighbor positions in specified order
        """
        x, y = pos
        
        # Define all possible movements in the required order
        # Each movement is defined as a displacement vector
        movements = [
            (x, y - 1),        # 1. Up
            (x + 1, y),        # 2. Right
            (x, y + 1),        # 3. Down
            (x + 1, y + 1),    # 4. BottomRight Diagonal
            (x - 1, y),        # 5. Left
            (x - 1, y - 1),    # 6. TopLeft Diagonal
            (x + 1, y - 1),    # 7. TopRight Diagonal
            (x - 1, y + 1),    # 8. BottomLeft Diagonal
        ]
        
        # Filter out invalid positions and blocked cells
        neighbors = []
        for neighbor_pos in movements:
            # Only add if within bounds AND not blocked by obstacle
            if (self._is_valid_position(neighbor_pos) and 
                not self.is_blocked(neighbor_pos)):
                neighbors.append(neighbor_pos)
        
        return neighbors
    
    def get_heuristic_distance(self, pos: Tuple[int, int]) -> float:
        """
        Calculate Manhattan distance heuristic to target.
        
        Manhattan distance = |x1 - x2| + |y1 - y2|
        This is useful for informed search algorithms (not required for this assignment,
        but included for future enhancements like A* search).
        
        Args:
            pos (Tuple[int, int]): Current position (x, y)
        
        Returns:
            float: Manhattan distance from pos to target
        """
        x, y = pos
        tx, ty = self.target
        # Calculate Manhattan distance: sum of absolute differences
        return abs(x - tx) + abs(y - ty)

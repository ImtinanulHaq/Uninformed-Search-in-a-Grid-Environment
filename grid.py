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
    """Enumeration for different cell types in the grid."""
    EMPTY = 0
    WALL = 1
    START = 2
    TARGET = 3
    EXPLORED = 4
    FRONTIER = 5
    PATH = 6


@dataclass
class Cell:
    """Represents a single cell in the grid."""
    x: int
    y: int
    cell_type: CellType = CellType.EMPTY
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return self.x == other.x and self.y == other.y


class Grid:
    """
    Manages the grid environment including static walls and dynamic obstacles.
    
    Attributes:
        width (int): Grid width in cells
        height (int): Grid height in cells
        start (Tuple[int, int]): Starting position (x, y)
        target (Tuple[int, int]): Target position (x, y)
        walls (Set[Tuple[int, int]]): Set of static wall positions
        dynamic_obstacles (Set[Tuple[int, int]]): Dynamic obstacles that appear during search
        dynamic_spawn_probability (float): Probability of spawning a dynamic obstacle per step
    """
    
    def __init__(self, width: int, height: int, start: Tuple[int, int], 
                 target: Tuple[int, int], dynamic_spawn_probability: float = 0.02):
        """
        Initialize the grid.
        
        Args:
            width: Grid width
            height: Grid height
            start: Starting position (x, y)
            target: Target position (x, y)
            dynamic_spawn_probability: Probability of dynamic obstacle spawn (0.0-1.0)
        """
        self.width = width
        self.height = height
        self.start = start
        self.target = target
        self.walls: Set[Tuple[int, int]] = set()
        self.dynamic_obstacles: Set[Tuple[int, int]] = set()
        self.dynamic_spawn_probability = dynamic_spawn_probability
        
        # Validate positions
        if not self._is_valid_position(start):
            raise ValueError("Start position is out of bounds")
        if not self._is_valid_position(target):
            raise ValueError("Target position is out of bounds")
    
    def _is_valid_position(self, pos: Tuple[int, int]) -> bool:
        """Check if a position is within grid boundaries."""
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height
    
    def add_wall(self, x: int, y: int) -> None:
        """Add a static wall at the given position."""
        if self._is_valid_position((x, y)) and (x, y) != self.start and (x, y) != self.target:
            self.walls.add((x, y))
    
    def add_walls_randomly(self, count: int) -> None:
        """
        Add random static walls to the grid.
        
        Args:
            count: Number of random walls to add
        """
        attempts = 0
        max_attempts = count * 10
        added = 0
        
        while added < count and attempts < max_attempts:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            if (x, y) not in self.walls and (x, y) != self.start and (x, y) != self.target:
                self.add_wall(x, y)
                added += 1
            
            attempts += 1
    
    def spawn_dynamic_obstacle(self) -> Tuple[int, int] | None:
        """
        Randomly spawn a dynamic obstacle during search.
        
        Returns:
            Position of new obstacle or None if none spawned
        """
        if random.random() > self.dynamic_spawn_probability:
            return None
        
        # Find empty cells that are not start or target
        empty_cells = []
        for x in range(self.width):
            for y in range(self.height):
                pos = (x, y)
                if (pos not in self.walls and 
                    pos not in self.dynamic_obstacles and 
                    pos != self.start and 
                    pos != self.target):
                    empty_cells.append(pos)
        
        if empty_cells:
            new_obstacle = random.choice(empty_cells)
            self.dynamic_obstacles.add(new_obstacle)
            return new_obstacle
        
        return None
    
    def is_blocked(self, pos: Tuple[int, int]) -> bool:
        """Check if a position is blocked by static or dynamic obstacles."""
        x, y = pos
        if not self._is_valid_position(pos):
            return True
        return pos in self.walls or pos in self.dynamic_obstacles
    
    def clear_dynamic_obstacles(self) -> None:
        """Clear all dynamic obstacles (useful for resetting search)."""
        self.dynamic_obstacles.clear()
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Get valid neighbors in clockwise order: Up, Right, Down, BottomRight, Left, TopLeft, TopRight, BottomLeft
        
        This follows the strict movement order specified in the assignment.
        
        Args:
            pos: Position (x, y)
            
        Returns:
            List of valid neighbor positions in the specified order
        """
        x, y = pos
        
        # Movement order: Up, Right, Down, BottomRight, Left, TopLeft, TopRight, BottomLeft
        movements = [
            (x, y - 1),        # Up
            (x + 1, y),        # Right
            (x, y + 1),        # Down
            (x + 1, y + 1),    # BottomRight (Diagonal)
            (x - 1, y),        # Left
            (x - 1, y - 1),    # TopLeft (Diagonal)
            (x + 1, y - 1),    # TopRight (Diagonal)
            (x - 1, y + 1),    # BottomLeft (Diagonal)
        ]
        
        # Filter valid and unblocked positions
        neighbors = []
        for neighbor_pos in movements:
            if (self._is_valid_position(neighbor_pos) and 
                not self.is_blocked(neighbor_pos)):
                neighbors.append(neighbor_pos)
        
        return neighbors
    
    def get_heuristic_distance(self, pos: Tuple[int, int]) -> float:
        """
        Calculate Manhattan distance heuristic to target.
        Useful for informed search (though not required for this assignment).
        
        Args:
            pos: Position (x, y)
            
        Returns:
            Manhattan distance to target
        """
        x, y = pos
        tx, ty = self.target
        return abs(x - tx) + abs(y - ty)

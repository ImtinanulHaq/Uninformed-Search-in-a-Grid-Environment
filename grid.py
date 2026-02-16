import random
from typing import List, Tuple, Set
from dataclasses import dataclass
from enum import Enum


class CellType(Enum):

    EMPTY = 0       # Unvisited, walkable cell
    WALL = 1        # Static obstacle that blocks movement
    START = 2       # Starting position of the pathfinder
    TARGET = 3      # Goal/destination position
    EXPLORED = 4    # Cell already visited by the algorithm
    FRONTIER = 5    # Cell waiting to be explored (in queue/stack)
    PATH = 6        # Cell that is part of the final solution path


@dataclass
class Cell:
  
    x: int                                    # X-coordinate (column) of the cell
    y: int                                    # Y-coordinate (row) of the cell
    cell_type: CellType = CellType.EMPTY      # Type of cell (empty, wall, start, etc.)
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):

        if not isinstance(other, Cell):
            return False
        return self.x == other.x and self.y == other.y


class Grid:

    
    def __init__(self, width: int, height: int, start: Tuple[int, int], 
                 target: Tuple[int, int], dynamic_spawn_probability: float = 0.02):
  
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

        x, y = pos
        # Check both x and y are within valid range [0, width) and [0, height)
        return 0 <= x < self.width and 0 <= y < self.height
    
    def add_wall(self, x: int, y: int) -> None:

        pos = (x, y)
        # Only add wall if position is valid and not start/target
        if self._is_valid_position(pos) and pos != self.start and pos != self.target:
            self.walls.add(pos)
    
    def add_walls_randomly(self, count: int) -> None:
   
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
   
        x, y = pos
        # First check if position is within valid grid bounds
        if not self._is_valid_position(pos):
            return True  # Out of bounds is always blocked
        # Check for static walls or dynamic obstacles
        return pos in self.walls or pos in self.dynamic_obstacles
    
    def clear_dynamic_obstacles(self) -> None:
   
        self.dynamic_obstacles.clear()
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:

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
 
        x, y = pos
        tx, ty = self.target
        # Calculate Manhattan distance: sum of absolute differences
        return abs(x - tx) + abs(y - ty)

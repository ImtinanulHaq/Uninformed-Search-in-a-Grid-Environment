"""
Search Algorithms Module

This module implements all six uninformed search algorithms:
1. Breadth-First Search (BFS)
2. Depth-First Search (DFS)
3. Uniform-Cost Search (UCS)
4. Depth-Limited Search (DLS)
5. Iterative Deepening DFS (IDDFS)
6. Bidirectional Search

Each algorithm explores a grid from start to target, tracking explored and frontier nodes
for visualization purposes.
"""

from collections import deque
from typing import Tuple, List, Set, Dict, Optional, Callable
from grid import Grid
import heapq


class SearchResult:
    """
    Container for search algorithm results.
    
    Attributes:
        path: Final path from start to target (empty if not found)
        explored: Set of all explored nodes
        frontier_history: History of frontier nodes at each step
        total_nodes_explored: Number of nodes explored
        found: Whether target was found
        dynamic_obstacles_encountered: List of dynamic obstacles that forced re-planning
    """
    
    def __init__(self):
        self.path: List[Tuple[int, int]] = []
        self.explored: Set[Tuple[int, int]] = set()
        self.frontier_history: List[Set[Tuple[int, int]]] = []
        self.total_nodes_explored: int = 0
        self.found: bool = False
        self.dynamic_obstacles_encountered: List[Tuple[int, int]] = []


class SearchAlgorithm:
    """Base class for all search algorithms."""
    
    def __init__(self, grid: Grid):
        """
        Initialize search algorithm.
        
        Args:
            grid: Grid object to search on
        """
        self.grid = grid
        self.explored: Set[Tuple[int, int]] = set()
        self.parent_map: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {}
        self.frontier_history: List[Set[Tuple[int, int]]] = []
        self.dynamic_obstacles_encountered: List[Tuple[int, int]] = []
    
    def _reconstruct_path(self, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Reconstruct the path from start to current position using parent map.
        
        Args:
            current: Current position
            
        Returns:
            List of positions from start to current
        """
        path = []
        pos = current
        while pos is not None:
            path.append(pos)
            pos = self.parent_map.get(pos)
        path.reverse()
        return path
    
    def _check_dynamic_obstacles(self, frontier: List | deque | Set) -> Optional[Tuple[int, int]]:
        """
        Check if any dynamic obstacles have spawned and handle them.
        
        Args:
            frontier: Current frontier (queue/stack/set)
            
        Returns:
            New obstacle position if spawned, None otherwise
        """
        new_obstacle = self.grid.spawn_dynamic_obstacle()
        if new_obstacle:
            self.dynamic_obstacles_encountered.append(new_obstacle)
        return new_obstacle
    
    def search(self) -> SearchResult:
        """
        Execute the search algorithm. Must be implemented by subclasses.
        
        Returns:
            SearchResult object with path and exploration data
        """
        raise NotImplementedError("Subclasses must implement search()")


class BreadthFirstSearch(SearchAlgorithm):
    """
    Breadth-First Search (BFS)
    
    Explores nodes level by level, guaranteeing the shortest path in unweighted graphs.
    Uses a queue (FIFO) for exploration order.
    
    Time Complexity: O(V + E) where V = vertices, E = edges
    Space Complexity: O(V)
    Best for: Finding shortest path, complete graphs
    """
    
    def search(self) -> SearchResult:
        """Execute Breadth-First Search."""
        result = SearchResult()
        
        # Initialize frontier queue with start node
        frontier = deque([self.grid.start])
        self.explored.add(self.grid.start)
        self.parent_map[self.grid.start] = None
        
        while frontier:
            # Check for dynamic obstacles
            self._check_dynamic_obstacles(frontier)
            
            # Record current frontier state
            self.frontier_history.append(set(frontier))
            
            # Get next node to explore (FIFO)
            current = frontier.popleft()
            
            # Check if we reached the target
            if current == self.grid.target:
                result.path = self._reconstruct_path(current)
                result.found = True
                break
            
            # Explore neighbors in specified order
            neighbors = self.grid.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in self.explored:
                    self.explored.add(neighbor)
                    self.parent_map[neighbor] = current
                    frontier.append(neighbor)
        
        result.explored = self.explored.copy()
        result.frontier_history = self.frontier_history
        result.total_nodes_explored = len(self.explored)
        result.dynamic_obstacles_encountered = self.dynamic_obstacles_encountered
        
        return result


class DepthFirstSearch(SearchAlgorithm):
    """
    Depth-First Search (DFS)
    
    Explores as far as possible along each branch before backtracking.
    Uses a stack (LIFO) for exploration order.
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    Best for: Topological sorting, detecting cycles
    Note: May not find shortest path in unweighted graphs
    """
    
    def search(self) -> SearchResult:
        """Execute Depth-First Search."""
        result = SearchResult()
        
        # Initialize frontier stack with start node
        frontier = [self.grid.start]
        self.explored.add(self.grid.start)
        self.parent_map[self.grid.start] = None
        
        while frontier:
            # Check for dynamic obstacles
            self._check_dynamic_obstacles(frontier)
            
            # Record current frontier state
            self.frontier_history.append(set(frontier))
            
            # Get next node to explore (LIFO)
            current = frontier.pop()
            
            # Check if we reached the target
            if current == self.grid.target:
                result.path = self._reconstruct_path(current)
                result.found = True
                break
            
            # Explore neighbors in reverse order (since we're using a stack, last added is explored first)
            neighbors = self.grid.get_neighbors(current)
            for neighbor in reversed(neighbors):
                if neighbor not in self.explored:
                    self.explored.add(neighbor)
                    self.parent_map[neighbor] = current
                    frontier.append(neighbor)
        
        result.explored = self.explored.copy()
        result.frontier_history = self.frontier_history
        result.total_nodes_explored = len(self.explored)
        result.dynamic_obstacles_encountered = self.dynamic_obstacles_encountered
        
        return result


class UniformCostSearch(SearchAlgorithm):
    """
    Uniform Cost Search (UCS)
    
    Expands nodes with lowest path cost first, using a priority queue.
    Guarantees finding the lowest-cost path.
    
    Time Complexity: O((V + E) * log V)
    Space Complexity: O(V)
    Best for: Weighted graphs, finding minimum cost paths
    """
    
    def search(self) -> SearchResult:
        """Execute Uniform Cost Search."""
        result = SearchResult()
        
        # Priority queue: (cost, node)
        frontier = [(0, self.grid.start)]
        cost_map: Dict[Tuple[int, int], float] = {self.grid.start: 0}
        self.explored.add(self.grid.start)
        self.parent_map[self.grid.start] = None
        
        while frontier:
            # Check for dynamic obstacles
            self._check_dynamic_obstacles(frontier)
            
            # Record current frontier state (extract nodes from priority queue)
            self.frontier_history.append({node for _, node in frontier})
            
            # Get node with lowest cost
            current_cost, current = heapq.heappop(frontier)
            
            # Check if we reached the target
            if current == self.grid.target:
                result.path = self._reconstruct_path(current)
                result.found = True
                break
            
            # Skip if we've already explored this node with a better cost
            if current_cost > cost_map.get(current, float('inf')):
                continue
            
            # Explore neighbors
            neighbors = self.grid.get_neighbors(current)
            for neighbor in neighbors:
                new_cost = current_cost + 1  # Uniform cost (all edges cost 1)
                
                if neighbor not in cost_map or new_cost < cost_map[neighbor]:
                    cost_map[neighbor] = new_cost
                    self.parent_map[neighbor] = current
                    heapq.heappush(frontier, (new_cost, neighbor))
                    
                    if neighbor not in self.explored:
                        self.explored.add(neighbor)
        
        result.explored = self.explored.copy()
        result.frontier_history = self.frontier_history
        result.total_nodes_explored = len(self.explored)
        result.dynamic_obstacles_encountered = self.dynamic_obstacles_encountered
        
        return result


class DepthLimitedSearch(SearchAlgorithm):
    """
    Depth-Limited Search (DLS)
    
    Like DFS but with a maximum depth limit to prevent infinite loops.
    Does not require a priori knowledge of graph structure.
    
    Time Complexity: O(b^l) where b = branching factor, l = depth limit
    Space Complexity: O(b * l)
    Best for: Avoiding infinite loops, limiting search scope
    """
    
    def __init__(self, grid: Grid, depth_limit: int = 10):
        """
        Initialize DLS with a depth limit.
        
        Args:
            grid: Grid object to search on
            depth_limit: Maximum depth to explore
        """
        super().__init__(grid)
        self.depth_limit = depth_limit
    
    def search(self) -> SearchResult:
        """Execute Depth-Limited Search."""
        result = SearchResult()
        
        # Stack: (node, depth)
        frontier = [(self.grid.start, 0)]
        self.explored.add(self.grid.start)
        self.parent_map[self.grid.start] = None
        
        while frontier:
            # Check for dynamic obstacles
            self._check_dynamic_obstacles(frontier)
            
            # Record current frontier state
            self.frontier_history.append({node for node, _ in frontier})
            
            # Get next node
            current, depth = frontier.pop()
            
            # Check if we reached the target
            if current == self.grid.target:
                result.path = self._reconstruct_path(current)
                result.found = True
                break
            
            # Only explore if we haven't exceeded depth limit
            if depth < self.depth_limit:
                neighbors = self.grid.get_neighbors(current)
                for neighbor in reversed(neighbors):
                    if neighbor not in self.explored:
                        self.explored.add(neighbor)
                        self.parent_map[neighbor] = current
                        frontier.append((neighbor, depth + 1))
        
        result.explored = self.explored.copy()
        result.frontier_history = self.frontier_history
        result.total_nodes_explored = len(self.explored)
        result.dynamic_obstacles_encountered = self.dynamic_obstacles_encountered
        
        return result


class IterativeDeepeningDFS(SearchAlgorithm):
    """
    Iterative Deepening Depth-First Search (IDDFS)
    
    Combines DFS and BFS advantages: depth-first search with limited memory
    and guaranteed shortest path (in unweighted graphs).
    Performs multiple DFS iterations with increasing depth limits.
    
    Time Complexity: O(b^d) where b = branching factor, d = solution depth
    Space Complexity: O(b * d)
    Best for: When solution depth is unknown, memory-constrained scenarios
    """
    
    def search(self) -> SearchResult:
        """Execute Iterative Deepening Depth-First Search."""
        result = SearchResult()
        
        # Try increasing depth limits
        max_depth = max(self.grid.width, self.grid.height) * 2
        
        for limit in range(1, max_depth + 1):
            self.explored.clear()
            self.parent_map.clear()
            self.parent_map[self.grid.start] = None
            
            # Perform DLS with current limit
            found, path = self._dls_recursive(self.grid.start, limit, None)
            
            if found:
                result.path = path
                result.found = True
                break
        
        result.explored = self.explored.copy()
        result.frontier_history = self.frontier_history
        result.total_nodes_explored = len(self.explored)
        result.dynamic_obstacles_encountered = self.dynamic_obstacles_encountered
        
        return result
    
    def _dls_recursive(self, current: Tuple[int, int], limit: int, 
                      parent: Optional[Tuple[int, int]]) -> Tuple[bool, List[Tuple[int, int]]]:
        """
        Recursive helper for depth-limited search.
        
        Args:
            current: Current node
            limit: Depth limit
            parent: Parent node
            
        Returns:
            Tuple of (found: bool, path: List)
        """
        # Check for dynamic obstacles periodically
        if len(self.explored) % 10 == 0:
            self._check_dynamic_obstacles([])
        
        self.explored.add(current)
        self.frontier_history.append(self.explored.copy())
        
        # Check if target found
        if current == self.grid.target:
            return True, self._reconstruct_path(current)
        
        # Check depth limit
        if limit == 0:
            return False, []
        
        # Explore neighbors
        neighbors = self.grid.get_neighbors(current)
        for neighbor in neighbors:
            if neighbor not in self.explored:
                self.parent_map[neighbor] = current
                found, path = self._dls_recursive(neighbor, limit - 1, current)
                if found:
                    return True, path
        
        return False, []


class BidirectionalSearch(SearchAlgorithm):
    """
    Bidirectional Search
    
    Searches simultaneously from start and target, meeting in the middle.
    Significantly reduces search space compared to unidirectional search.
    
    Time Complexity: O(b^(d/2)) where b = branching factor, d = solution depth
    Space Complexity: O(b^(d/2))
    Best for: Dense graphs, when both start and target are specified
    """
    
    def search(self) -> SearchResult:
        """Execute Bidirectional Search."""
        result = SearchResult()
        
        # Initialize two frontiers: forward (from start) and backward (from target)
        forward_frontier = deque([self.grid.start])
        backward_frontier = deque([self.grid.target])
        
        forward_explored: Set[Tuple[int, int]] = {self.grid.start}
        backward_explored: Set[Tuple[int, int]] = {self.grid.target}
        
        forward_parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {self.grid.start: None}
        backward_parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {self.grid.target: None}
        
        meeting_point: Optional[Tuple[int, int]] = None
        
        # Alternate between forward and backward search
        while forward_frontier or backward_frontier:
            # Check for dynamic obstacles
            self._check_dynamic_obstacles(forward_frontier)
            
            # Expand from forward frontier
            if forward_frontier:
                current = forward_frontier.popleft()
                self.explored.add(current)
                
                neighbors = self.grid.get_neighbors(current)
                for neighbor in neighbors:
                    if neighbor in backward_explored:
                        # Found meeting point!
                        meeting_point = neighbor
                        forward_parent[neighbor] = current
                        break
                    
                    if neighbor not in forward_explored:
                        forward_explored.add(neighbor)
                        forward_parent[neighbor] = current
                        forward_frontier.append(neighbor)
                
                if meeting_point:
                    break
            
            # Expand from backward frontier
            if backward_frontier:
                current = backward_frontier.popleft()
                self.explored.add(current)
                
                neighbors = self.grid.get_neighbors(current)
                for neighbor in neighbors:
                    if neighbor in forward_explored:
                        # Found meeting point!
                        meeting_point = neighbor
                        backward_parent[neighbor] = current
                        break
                    
                    if neighbor not in backward_explored:
                        backward_explored.add(neighbor)
                        backward_parent[neighbor] = current
                        backward_frontier.append(neighbor)
                
                if meeting_point:
                    break
            
            # Record frontier state
            current_frontier = set(forward_frontier) | set(backward_frontier)
            self.frontier_history.append(current_frontier)
        
        # Reconstruct path if meeting point found
        if meeting_point:
            # Build path from start to meeting point
            path_forward = []
            pos = meeting_point
            while pos is not None:
                path_forward.append(pos)
                pos = forward_parent.get(pos)
            path_forward.reverse()
            
            # Build path from meeting point to target
            path_backward = []
            pos = meeting_point
            while pos is not None:
                path_backward.append(pos)
                pos = backward_parent.get(pos)
            
            # Remove duplicate meeting point
            if path_forward and path_backward and path_forward[-1] == path_backward[0]:
                path_backward.pop(0)
            
            result.path = path_forward + path_backward
            result.found = True
        
        result.explored = self.explored.copy()
        result.frontier_history = self.frontier_history
        result.total_nodes_explored = len(self.explored)
        result.dynamic_obstacles_encountered = self.dynamic_obstacles_encountered
        
        return result

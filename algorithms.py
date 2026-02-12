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
from typing import Tuple, List, Set, Dict, Optional, Union
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
    
    def _check_dynamic_obstacles(self, frontier: Union[List, deque, Set]) -> Optional[Tuple[int, int]]:
        """
        Check if any dynamic obstacles have spawned and handle them.
        
        For dynamic environments, if an obstacle blocks a node in the frontier,
        that node must be removed to trigger replanning.
        
        Handles different tuple formats:
        - BFS/DFS: (x, y) nodes
        - UCS: (cost, counter, (x, y)) tuples
        - DLS: ((x, y), depth) tuples
        
        Args:
            frontier: Current frontier (queue/stack/set)
            
        Returns:
            New obstacle position if spawned, None otherwise
        """
        new_obstacle = self.grid.spawn_dynamic_obstacle()
        if new_obstacle:
            self.dynamic_obstacles_encountered.append(new_obstacle)
            
            # Handle blocked nodes in frontier
            if isinstance(frontier, deque):
                # For queue-based searches (BFS, Bidirectional)
                frontier_list = list(frontier)
                frontier.clear()
                for item in frontier_list:
                    if not self.grid.is_blocked(item):
                        frontier.append(item)
            elif isinstance(frontier, list):
                # For stack-based and priority-based searches
                frontier_copy = frontier.copy()
                frontier.clear()
                for item in frontier_copy:
                    # Extract node from different tuple formats
                    node = self._extract_node_from_item(item)
                    if node and not self.grid.is_blocked(node):
                        frontier.append(item)
                    elif node is None:
                        # Item is just a node tuple, keep it if not blocked
                        if not isinstance(item, tuple) or len(item) != 2:
                            frontier.append(item)
                        elif not self.grid.is_blocked(item):
                            frontier.append(item)
            elif isinstance(frontier, set):
                # For set-based frontiers
                blocked_items = set()
                for item in frontier:
                    node = self._extract_node_from_item(item)
                    if node and self.grid.is_blocked(node):
                        blocked_items.add(item)
                frontier.difference_update(blocked_items)
        
        return new_obstacle
    
    def _extract_node_from_item(self, item) -> Optional[Tuple[int, int]]:
        """
        Extract node coordinates from different frontier item formats.
        
        Args:
            item: Frontier item (node or wrapped node)
            
        Returns:
            Node tuple (x, y) or None if item is just a node
        """
        # UCS format: (cost, counter, node)
        if isinstance(item, tuple) and len(item) == 3:
            try:
                if isinstance(item[2], tuple) and len(item[2]) == 2:
                    return item[2]  # Return the node
            except (TypeError, IndexError):
                pass
        
        # DLS format: (node, depth)
        if isinstance(item, tuple) and len(item) == 2:
            try:
                if isinstance(item[0], tuple) and len(item[0]) == 2:
                    # Check if item[1] looks like a depth (int)
                    if isinstance(item[1], int):
                        return item[0]  # Return the node
            except (TypeError, IndexError):
                pass
        
        # Plain node format: (x, y)
        if isinstance(item, tuple) and len(item) == 2:
            try:
                if isinstance(item[0], int) and isinstance(item[1], int):
                    return item  # Item is already a node
            except (TypeError, IndexError):
                pass
        
        return None
    
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
        self.explored: Set[Tuple[int, int]] = set()  # Mark as explored when POPPING, not when adding
        self.parent_map[self.grid.start] = None
        
        # Track in-frontier nodes to avoid duplicates
        in_frontier: Set[Tuple[int, int]] = {self.grid.start}
        
        while frontier:
            # Check for dynamic obstacles and remove blocked nodes
            self._check_dynamic_obstacles(frontier)
            
            # Record current frontier state for visualization
            self.frontier_history.append(set(frontier))
            
            # Get next node to explore (FIFO)
            current = frontier.popleft()
            in_frontier.discard(current)
            
            # Skip if already explored (can happen with dynamic obstacles)
            if current in self.explored:
                continue
            
            # Mark as explored when POPPING, not when adding
            # This allows dynamic obstacles to trigger reconsideration
            self.explored.add(current)
            
            # Check if we reached the target
            if current == self.grid.target:
                result.path = self._reconstruct_path(current)
                result.found = True
                break
            
            # Explore neighbors in specified order
            neighbors = self.grid.get_neighbors(current)
            for neighbor in neighbors:
                # Only add if not yet explored and not already in frontier
                if neighbor not in self.explored and neighbor not in in_frontier:
                    self.parent_map[neighbor] = current
                    frontier.append(neighbor)
                    in_frontier.add(neighbor)
        
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
        self.explored: Set[Tuple[int, int]] = set()  # Mark as explored when POPPING
        self.parent_map[self.grid.start] = None
        
        # Track in-frontier nodes
        in_frontier: Set[Tuple[int, int]] = {self.grid.start}
        
        while frontier:
            # Check for dynamic obstacles and remove blocked nodes
            self._check_dynamic_obstacles(frontier)
            
            # Record current frontier state
            self.frontier_history.append(set(frontier))
            
            # Get next node to explore (LIFO)
            current = frontier.pop()
            in_frontier.discard(current)
            
            # Skip if already explored (can happen with dynamic obstacles)
            if current in self.explored:
                continue
            
            # Mark as explored when POPPING
            self.explored.add(current)
            
            # Check if we reached the target
            if current == self.grid.target:
                result.path = self._reconstruct_path(current)
                result.found = True
                break
            
            # Explore neighbors in reverse order (since we're using a stack)
            neighbors = self.grid.get_neighbors(current)
            for neighbor in reversed(neighbors):
                if neighbor not in self.explored and neighbor not in in_frontier:
                    self.parent_map[neighbor] = current
                    frontier.append(neighbor)
                    in_frontier.add(neighbor)
        
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
        
        # Priority queue: (cost, counter, node) - counter for stable ordering
        frontier = [(0, 0, self.grid.start)]
        cost_map: Dict[Tuple[int, int], float] = {self.grid.start: 0}
        self.explored: Set[Tuple[int, int]] = set()  # Mark as explored when POPPING
        self.parent_map[self.grid.start] = None
        counter = 1  # For stable ordering in priority queue
        
        while frontier:
            # Check for dynamic obstacles
            self._check_dynamic_obstacles(frontier)
            
            # Record current frontier state
            self.frontier_history.append({node for _, _, node in frontier})
            
            # Get node with lowest cost
            current_cost, _, current = heapq.heappop(frontier)
            
            # Skip if already explored (can happen if node added multiple times)
            if current in self.explored:
                continue
            
            # Skip if we've found a better path already
            if current_cost > cost_map.get(current, float('inf')):
                continue
            
            # Mark as explored when POPPING to allow reconsideration
            self.explored.add(current)
            
            # Check if we reached the target
            if current == self.grid.target:
                result.path = self._reconstruct_path(current)
                result.found = True
                break
            
            # Explore neighbors (do NOT mark explored here)
            neighbors = self.grid.get_neighbors(current)
            for neighbor in neighbors:
                new_cost = current_cost + 1  # Uniform cost (all edges cost 1)
                
                # If we found a better path or first path to this node
                if neighbor not in cost_map or new_cost < cost_map[neighbor]:
                    cost_map[neighbor] = new_cost
                    self.parent_map[neighbor] = current
                    heapq.heappush(frontier, (new_cost, counter, neighbor))
                    counter += 1
        
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
        self.explored: Set[Tuple[int, int]] = set()  # Mark as explored when POPPING
        self.parent_map[self.grid.start] = None
        
        # Track in-frontier nodes to avoid duplicates
        in_frontier: Set[Tuple[int, int]] = {self.grid.start}
        
        while frontier:
            # Check for dynamic obstacles and remove blocked nodes
            self._check_dynamic_obstacles(frontier)
            
            # Record current frontier state
            self.frontier_history.append({node for node, _ in frontier})
            
            # Get next node
            current, depth = frontier.pop()
            in_frontier.discard(current)
            
            # Skip if already explored
            if current in self.explored:
                continue
            
            # Mark as explored when POPPING
            self.explored.add(current)
            
            # Check if we reached the target
            if current == self.grid.target:
                result.path = self._reconstruct_path(current)
                result.found = True
                break
            
            # Only explore if we haven't exceeded depth limit
            if depth < self.depth_limit:
                neighbors = self.grid.get_neighbors(current)
                for neighbor in reversed(neighbors):
                    if neighbor not in self.explored and neighbor not in in_frontier:
                        self.parent_map[neighbor] = current
                        frontier.append((neighbor, depth + 1))
                        in_frontier.add(neighbor)
        
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
        all_explored: Set[Tuple[int, int]] = set()  # Accumulate explored across iterations
        
        for limit in range(1, max_depth + 1):
            # Create fresh structures for each iteration
            self.explored.clear()
            self.parent_map.clear()
            self.parent_map[self.grid.start] = None
            
            # Perform DLS with current limit
            found, path = self._dls_recursive(self.grid.start, limit, None)
            
            # Accumulate explored nodes across iterations for accurate count
            all_explored.update(self.explored)
            
            if found:
                result.path = path
                result.found = True
                # Include all nodes explored up to solution depth
                result.explored = all_explored.copy()
                break
        
        # If not found, report all explored nodes across all iterations
        if not result.found:
            result.explored = all_explored.copy()
        
        result.frontier_history = self.frontier_history
        # Total nodes is accurate count from accumulated exploration
        result.total_nodes_explored = len(all_explored) if all_explored else len(self.explored)
        result.dynamic_obstacles_encountered = self.dynamic_obstacles_encountered
        
        return result
    
    def _dls_recursive(self, current: Tuple[int, int], limit: int, 
                      parent: Optional[Tuple[int, int]]) -> Tuple[bool, List[Tuple[int, int]]]:
        """
        Recursive helper for depth-limited search.
        
        Args:
            current: Current node being explored
            limit: Remaining depth limit before stopping exploration
            parent: Parent node (for reference)
            
        Returns:
            Tuple of (found: bool, path: List) where path is only filled if found=True
        """
        # Check for dynamic obstacles periodically (during recursion)
        if len(self.explored) % 10 == 0:
            self._check_dynamic_obstacles([])
        
        # Mark current node as explored
        self.explored.add(current)
        self.frontier_history.append(self.explored.copy())
        
        # Check if we reached the target
        if current == self.grid.target:
            return True, self._reconstruct_path(current)
        
        # Check if we've exceeded depth limit
        if limit == 0:
            return False, []
        
        # Explore neighbors recursively with reduced depth limit
        neighbors = self.grid.get_neighbors(current)
        for neighbor in neighbors:
            # Skip if already explored in this iteration
            if neighbor not in self.explored:
                # Set parent before recursive call
                self.parent_map[neighbor] = current
                # Recurse with depth limit reduced by 1
                found, path = self._dls_recursive(neighbor, limit - 1, current)
                if found:
                    return True, path
        
        # No solution found from this node at this depth
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
        
        forward_explored: Set[Tuple[int, int]] = set()  # Mark when POPPING
        backward_explored: Set[Tuple[int, int]] = set()  # Mark when POPPING
        
        forward_in_frontier: Set[Tuple[int, int]] = {self.grid.start}
        backward_in_frontier: Set[Tuple[int, int]] = {self.grid.target}
        
        forward_parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {self.grid.start: None}
        backward_parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {self.grid.target: None}
        
        meeting_point: Optional[Tuple[int, int]] = None
        
        # Alternate between forward and backward search
        while forward_frontier or backward_frontier:
            # Check for dynamic obstacles in both frontiers
            self._check_dynamic_obstacles(forward_frontier)
            self._check_dynamic_obstacles(backward_frontier)
            
            # Expand from forward frontier
            if forward_frontier:
                current = forward_frontier.popleft()
                forward_in_frontier.discard(current)
                
                # Skip if already explored
                if current not in forward_explored:
                    forward_explored.add(current)
                    self.explored.add(current)
                    
                    neighbors = self.grid.get_neighbors(current)
                    for neighbor in neighbors:
                        # Check if we found meeting point
                        if neighbor in backward_explored:
                            meeting_point = neighbor
                            forward_parent[neighbor] = current
                            break
                        
                        # Add to forward frontier if not explored and not in frontier
                        if neighbor not in forward_explored and neighbor not in forward_in_frontier:
                            forward_parent[neighbor] = current
                            forward_frontier.append(neighbor)
                            forward_in_frontier.add(neighbor)
                    
                    if meeting_point:
                        break
            
            # Expand from backward frontier
            if backward_frontier and not meeting_point:
                current = backward_frontier.popleft()
                backward_in_frontier.discard(current)
                
                # Skip if already explored
                if current not in backward_explored:
                    backward_explored.add(current)
                    self.explored.add(current)
                    
                    neighbors = self.grid.get_neighbors(current)
                    for neighbor in neighbors:
                        # Check if we found meeting point
                        if neighbor in forward_explored:
                            meeting_point = neighbor
                            backward_parent[neighbor] = current
                            break
                        
                        # Add to backward frontier if not explored and not in frontier
                        if neighbor not in backward_explored and neighbor not in backward_in_frontier:
                            backward_parent[neighbor] = current
                            backward_frontier.append(neighbor)
                            backward_in_frontier.add(neighbor)
                    
                    if meeting_point:
                        break
            
            # Record frontier state for visualization (keep separate for clarity)
            current_frontier = set(forward_frontier) | set(backward_frontier)
            self.frontier_history.append(current_frontier)
        
        # Reconstruct path if meeting point found
        if meeting_point:
            # Build path from start to meeting point using forward parent map
            path_forward = []
            pos = meeting_point
            while pos is not None:
                path_forward.append(pos)
                pos = forward_parent.get(pos)
            path_forward.reverse()
            
            # Build path from meeting point to target using backward parent map
            path_backward = []
            pos = backward_parent.get(meeting_point)  # Start from parent of meeting point
            while pos is not None:
                path_backward.append(pos)
                pos = backward_parent.get(pos)
            
            # Combine paths (no duplicate needed as we skip meeting point parent)
            result.path = path_forward + path_backward
            result.found = True
        
        result.explored = self.explored.copy()
        result.frontier_history = self.frontier_history
        result.total_nodes_explored = len(self.explored)
        result.dynamic_obstacles_encountered = self.dynamic_obstacles_encountered
        
        return result

from collections import deque
from typing import Tuple, List, Set, Dict, Optional, Union
from grid import Grid
import heapq


class SearchResult:

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
       
        path = []
        pos = current
        
        # Trace back from current to start using parent pointers
        while pos is not None:
            path.append(pos)
            pos = self.parent_map.get(pos)
        
        # Reverse to get path from start to current
        path.reverse()
        return path
    
    def _check_dynamic_obstacles(self, frontier: Union[List, deque, Set]) -> Optional[Tuple[int, int]]:
 
        # Check if a new dynamic obstacle has spawned
        new_obstacle = self.grid.spawn_dynamic_obstacle()
        if new_obstacle:
            self.dynamic_obstacles_encountered.append(new_obstacle)
            
            # Remove blocked nodes from frontier based on data structure type
            if isinstance(frontier, deque):
                # For queue-based searches (BFS, Bidirectional)
                frontier_list = list(frontier)
                frontier.clear()
                for item in frontier_list:
                    if not self.grid.is_blocked(item):
                        frontier.append(item)
                        
            elif isinstance(frontier, list):
                # For stack-based and priority-based searches (DFS, UCS, DLS)
                frontier_copy = frontier.copy()
                frontier.clear()
                for item in frontier_copy:
                    # Extract node from wrapped formats
                    node = self._extract_node_from_item(item)
                    if node:
                        # Item is wrapped (UCS or DLS format)
                        if not self.grid.is_blocked(node):
                            frontier.append(item)
                    else:
                        # Item is a plain node tuple
                        if not self.grid.is_blocked(item):
                            frontier.append(item)
                            
            elif isinstance(frontier, set):
                # For set-based frontiers
                blocked_items = {item for item in frontier 
                               if self.grid.is_blocked(self._extract_node_from_item(item) or item)}
                frontier.difference_update(blocked_items)
        
        return new_obstacle
    
    def _extract_node_from_item(self, item) -> Optional[Tuple[int, int]]:
 
        # UCS format: (cost, counter, node)
        if isinstance(item, tuple) and len(item) == 3:
            if isinstance(item[2], tuple) and len(item[2]) == 2:
                try:
                    # Verify it's a valid coordinate pair
                    if isinstance(item[2][0], int) and isinstance(item[2][1], int):
                        return item[2]
                except (TypeError, IndexError):
                    pass
        
        # DLS format: (node, depth)
        if isinstance(item, tuple) and len(item) == 2:
            # Check if first element is a node tuple
            if isinstance(item[0], tuple) and len(item[0]) == 2:
                try:
                    # Verify second element is depth (int)
                    if isinstance(item[1], int) and item[1] >= 0:
                        return item[0]
                except (TypeError, IndexError):
                    pass
        
        # Plain node format: (x, y) - return None to signal it's already a node
        return None
    
    def search(self) -> SearchResult:
    
        raise NotImplementedError("Subclasses must implement search()")


class BreadthFirstSearch(SearchAlgorithm):
 
    
    def search(self) -> SearchResult:
        """Execute Breadth-First Search."""
        result = SearchResult()
        
        # Initialize frontier with start node (FIFO queue)
        frontier = deque([self.grid.start])
        self.explored = set()
        self.parent_map[self.grid.start] = None
        
        # Track nodes currently in frontier to avoid duplicates
        in_frontier: Set[Tuple[int, int]] = {self.grid.start}
        
        while frontier:
            # Check for new dynamic obstacles
            self._check_dynamic_obstacles(frontier)
            
            # Save current frontier state for visualization
            self.frontier_history.append(set(frontier))
            
            # Get next node (First In First Out)
            current = frontier.popleft()
            in_frontier.discard(current)
            
            # Skip if already explored (can happen with dynamic obstacles)
            if current in self.explored:
                continue
            
            # Mark node as explored NOW (not when adding to frontier)
            self.explored.add(current)
            
            # Check if we reached the target
            if current == self.grid.target:
                result.path = self._reconstruct_path(current)
                result.found = True
                break
            
            # Explore all neighbors
            neighbors = self.grid.get_neighbors(current)
            for neighbor in neighbors:
                # Only add if not explored and not in frontier
                if neighbor not in self.explored and neighbor not in in_frontier:
                    self.parent_map[neighbor] = current
                    frontier.append(neighbor)
                    in_frontier.add(neighbor)
        
        # Store results
        result.explored = self.explored.copy()
        result.frontier_history = self.frontier_history
        result.total_nodes_explored = len(self.explored)
        result.dynamic_obstacles_encountered = self.dynamic_obstacles_encountered
        
        return result


class DepthFirstSearch(SearchAlgorithm):
  
    
    def search(self) -> SearchResult:
        """Execute Depth-First Search."""
        result = SearchResult()
        
        # Initialize frontier with start node (LIFO stack)
        frontier = [self.grid.start]
        self.explored = set()
        self.parent_map[self.grid.start] = None
        
        # Track nodes in frontier
        in_frontier: Set[Tuple[int, int]] = {self.grid.start}
        
        while frontier:
            # Check for new dynamic obstacles
            self._check_dynamic_obstacles(frontier)
            
            # Save frontier state for visualization
            self.frontier_history.append(set(frontier))
            
            # Get next node (Last In First Out)
            current = frontier.pop()
            in_frontier.discard(current)
            
            # Skip if already explored
            if current in self.explored:
                continue
            
            # Mark as explored NOW
            self.explored.add(current)
            
            # Check if target found
            if current == self.grid.target:
                result.path = self._reconstruct_path(current)
                result.found = True
                break
            
            # Add neighbors in reverse order (because stack reverses them)
            neighbors = self.grid.get_neighbors(current)
            for neighbor in reversed(neighbors):
                if neighbor not in self.explored and neighbor not in in_frontier:
                    self.parent_map[neighbor] = current
                    frontier.append(neighbor)
                    in_frontier.add(neighbor)
        
        # Store results
        result.explored = self.explored.copy()
        result.frontier_history = self.frontier_history
        result.total_nodes_explored = len(self.explored)
        result.dynamic_obstacles_encountered = self.dynamic_obstacles_encountered
        
        return result


class UniformCostSearch(SearchAlgorithm):
 
    
    def search(self) -> SearchResult:
        """Execute Uniform Cost Search."""
        result = SearchResult()
        
        # Priority queue: (cost, counter, node)
        # Counter ensures stable ordering when costs are equal
        frontier = [(0, 0, self.grid.start)]
        cost_map: Dict[Tuple[int, int], float] = {self.grid.start: 0}
        self.explored = set()
        self.parent_map[self.grid.start] = None
        counter = 1
        
        while frontier:
            # Check for dynamic obstacles
            self._check_dynamic_obstacles(frontier)
            
            # Save frontier state (extract nodes from priority tuples)
            self.frontier_history.append({node for _, _, node in frontier})
            
            # Get node with lowest cost
            current_cost, _, current = heapq.heappop(frontier)
            
            # Skip if already explored
            if current in self.explored:
                continue
            
            # Skip if we found a better path already
            if current_cost > cost_map.get(current, float('inf')):
                continue
            
            # Mark as explored
            self.explored.add(current)
            
            # Check if target found
            if current == self.grid.target:
                result.path = self._reconstruct_path(current)
                result.found = True
                break
            
            # Explore neighbors
            neighbors = self.grid.get_neighbors(current)
            for neighbor in neighbors:
                # Calculate new cost (uniform cost = 1 per edge)
                new_cost = current_cost + 1
                
                # Update if this is a better path
                if neighbor not in cost_map or new_cost < cost_map[neighbor]:
                    cost_map[neighbor] = new_cost
                    self.parent_map[neighbor] = current
                    heapq.heappush(frontier, (new_cost, counter, neighbor))
                    counter += 1
        
        # Store results
        result.explored = self.explored.copy()
        result.frontier_history = self.frontier_history
        result.total_nodes_explored = len(self.explored)
        result.dynamic_obstacles_encountered = self.dynamic_obstacles_encountered
        
        return result


class DepthLimitedSearch(SearchAlgorithm):
    
    
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
        
        # Stack with depth tracking: (node, depth)
        frontier = [(self.grid.start, 0)]
        self.explored = set()
        self.parent_map[self.grid.start] = None
        
        # Track nodes in frontier
        in_frontier: Set[Tuple[int, int]] = {self.grid.start}
        
        while frontier:
            # Check for dynamic obstacles
            self._check_dynamic_obstacles(frontier)
            
            # Save frontier state (extract nodes from tuples)
            self.frontier_history.append({node for node, _ in frontier})
            
            # Get next node with its depth
            current, depth = frontier.pop()
            in_frontier.discard(current)
            
            # Skip if already explored
            if current in self.explored:
                continue
            
            # Mark as explored
            self.explored.add(current)
            
            # Check if target found
            if current == self.grid.target:
                result.path = self._reconstruct_path(current)
                result.found = True
                break
            
            # Only expand if within depth limit
            if depth < self.depth_limit:
                neighbors = self.grid.get_neighbors(current)
                for neighbor in reversed(neighbors):
                    if neighbor not in self.explored and neighbor not in in_frontier:
                        self.parent_map[neighbor] = current
                        frontier.append((neighbor, depth + 1))
                        in_frontier.add(neighbor)
        
        # Store results
        result.explored = self.explored.copy()
        result.frontier_history = self.frontier_history
        result.total_nodes_explored = len(self.explored)
        result.dynamic_obstacles_encountered = self.dynamic_obstacles_encountered
        
        return result


class IterativeDeepeningDFS(SearchAlgorithm):
   
    def search(self) -> SearchResult:
        """Execute Iterative Deepening DFS."""
        result = SearchResult()
        
        # Maximum depth to try
        max_depth = max(self.grid.width, self.grid.height) * 2
        
        # Accumulate explored nodes across all iterations
        all_explored: Set[Tuple[int, int]] = set()
        
        # Try increasing depth limits
        for limit in range(1, max_depth + 1):
            # Reset for each iteration
            self.explored = set()
            self.parent_map = {self.grid.start: None}
            
            # Perform DFS with current depth limit
            found, path = self._dls_recursive(self.grid.start, limit, None)
            
            # Accumulate all explored nodes
            all_explored.update(self.explored)
            
            # Stop if target found
            if found:
                result.path = path
                result.found = True
                result.explored = all_explored.copy()
                break
        
        # If not found, still report all explored nodes
        if not result.found:
            result.explored = all_explored.copy()
        
        result.frontier_history = self.frontier_history
        result.total_nodes_explored = len(all_explored)
        result.dynamic_obstacles_encountered = self.dynamic_obstacles_encountered
        
        return result
    
    def _dls_recursive(self, current: Tuple[int, int], limit: int, 
                      parent: Optional[Tuple[int, int]]) -> Tuple[bool, List[Tuple[int, int]]]:
        
        # Periodically check for dynamic obstacles
        if len(self.explored) % 10 == 0:
            self._check_dynamic_obstacles([])
        
        # Mark current node as explored
        self.explored.add(current)
        self.frontier_history.append(self.explored.copy())
        
        # Check if target reached
        if current == self.grid.target:
            return True, self._reconstruct_path(current)
        
        # Stop if depth limit reached
        if limit == 0:
            return False, []
        
        # Recursively explore neighbors with reduced depth
        neighbors = self.grid.get_neighbors(current)
        for neighbor in neighbors:
            # Skip already explored nodes in this iteration
            if neighbor not in self.explored:
                # Set parent relationship
                self.parent_map[neighbor] = current
                
                # Recursive call with decreased limit
                found, path = self._dls_recursive(neighbor, limit - 1, current)
                
                if found:
                    return True, path
        
        # No solution found from this node
        return False, []


class BidirectionalSearch(SearchAlgorithm):
  
    
    def search(self) -> SearchResult:
        """Execute Bidirectional Search."""
        result = SearchResult()
        
        # Two separate frontiers
        forward_frontier = deque([self.grid.start])
        backward_frontier = deque([self.grid.target])
        
        # Separate explored sets
        forward_explored: Set[Tuple[int, int]] = set()
        backward_explored: Set[Tuple[int, int]] = set()
        
        # Track nodes in frontiers
        forward_in_frontier: Set[Tuple[int, int]] = {self.grid.start}
        backward_in_frontier: Set[Tuple[int, int]] = {self.grid.target}
        
        # Separate parent maps for path reconstruction
        forward_parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {self.grid.start: None}
        backward_parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {self.grid.target: None}
        
        meeting_point: Optional[Tuple[int, int]] = None
        
        # Alternate between forward and backward search
        while forward_frontier or backward_frontier:
            # Check for dynamic obstacles in both frontiers
            self._check_dynamic_obstacles(forward_frontier)
            self._check_dynamic_obstacles(backward_frontier)
            
            # === Forward search step ===
            if forward_frontier:
                current = forward_frontier.popleft()
                forward_in_frontier.discard(current)
                
                # Skip if already explored
                if current not in forward_explored:
                    forward_explored.add(current)
                    self.explored.add(current)
                    
                    # Explore neighbors
                    neighbors = self.grid.get_neighbors(current)
                    for neighbor in neighbors:
                        # Check for meeting point
                        if neighbor in backward_explored:
                            meeting_point = neighbor
                            forward_parent[neighbor] = current
                            break
                        
                        # Add to frontier if not explored
                        if neighbor not in forward_explored and neighbor not in forward_in_frontier:
                            forward_parent[neighbor] = current
                            forward_frontier.append(neighbor)
                            forward_in_frontier.add(neighbor)
                    
                    if meeting_point:
                        break
            
            # === Backward search step ===
            if backward_frontier and not meeting_point:
                current = backward_frontier.popleft()
                backward_in_frontier.discard(current)
                
                # Skip if already explored
                if current not in backward_explored:
                    backward_explored.add(current)
                    self.explored.add(current)
                    
                    # Explore neighbors
                    neighbors = self.grid.get_neighbors(current)
                    for neighbor in neighbors:
                        # Check for meeting point
                        if neighbor in forward_explored:
                            meeting_point = neighbor
                            backward_parent[neighbor] = current
                            break
                        
                        # Add to frontier if not explored
                        if neighbor not in backward_explored and neighbor not in backward_in_frontier:
                            backward_parent[neighbor] = current
                            backward_frontier.append(neighbor)
                            backward_in_frontier.add(neighbor)
                    
                    if meeting_point:
                        break
            
            # Save combined frontier state for visualization
            combined_frontier = set(forward_frontier) | set(backward_frontier)
            self.frontier_history.append(combined_frontier)
        
        # Reconstruct complete path if meeting point found
        if meeting_point:
            # Path from start to meeting point
            path_forward = []
            pos = meeting_point
            while pos is not None:
                path_forward.append(pos)
                pos = forward_parent.get(pos)
            path_forward.reverse()
            
            # Path from meeting point to target
            path_backward = []
            pos = backward_parent.get(meeting_point)
            while pos is not None:
                path_backward.append(pos)
                pos = backward_parent.get(pos)
            
            # Combine paths (meeting point already in forward path)
            result.path = path_forward + path_backward
            result.found = True
        
        # Store results
        result.explored = self.explored.copy()
        result.frontier_history = self.frontier_history
        result.total_nodes_explored = len(self.explored)
        result.dynamic_obstacles_encountered = self.dynamic_obstacles_encountered
        
        return result

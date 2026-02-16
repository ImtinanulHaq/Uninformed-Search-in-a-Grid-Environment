from collections import deque
from . import SearchResult

class BidirectionalSearch:
    def __init__(self, grid):
        self.grid = grid
        self.explored_forward = set()
        self.explored_backward = set()
        self.parent_forward = {}
        self.parent_backward = {}
        self.frontier_history = []
    
    def search(self):
        frontier_f = deque([self.grid.start])
        frontier_b = deque([self.grid.target])
        
        in_frontier_f = {self.grid.start}
        in_frontier_b = {self.grid.target}
        
        self.parent_forward[self.grid.start] = None
        self.parent_backward[self.grid.target] = None
        
        while frontier_f or frontier_b:
            if frontier_f:
                node_f = frontier_f.popleft()
                in_frontier_f.discard(node_f)
                
                if node_f in self.explored_backward:
                    path = self.reconstruct_path(node_f)
                    explored = self.explored_forward | self.explored_backward
                    return SearchResult(True, path, explored, self.frontier_history)
                
                self.explored_forward.add(node_f)
                
                neighbors = self.grid.get_neighbors(node_f)
                for neighbor in neighbors:
                    if neighbor not in self.explored_forward and neighbor not in in_frontier_f:
                        self.parent_forward[neighbor] = node_f
                        frontier_f.append(neighbor)
                        in_frontier_f.add(neighbor)
            
            if frontier_b:
                node_b = frontier_b.popleft()
                in_frontier_b.discard(node_b)
                
                if node_b in self.explored_forward:
                    path = self.reconstruct_path(node_b)
                    explored = self.explored_forward | self.explored_backward
                    return SearchResult(True, path, explored, self.frontier_history)
                
                self.explored_backward.add(node_b)
                
                neighbors = self.grid.get_neighbors(node_b)
                for neighbor in neighbors:
                    if neighbor not in self.explored_backward and neighbor not in in_frontier_b:
                        self.parent_backward[neighbor] = node_b
                        frontier_b.append(neighbor)
                        in_frontier_b.add(neighbor)
        
        explored = self.explored_forward | self.explored_backward
        return SearchResult(False, [], explored, self.frontier_history)
    
    def reconstruct_path(self, meeting_point):
        path_f = []
        current = meeting_point
        while current is not None:
            path_f.append(current)
            current = self.parent_forward.get(current)
        path_f.reverse()
        
        path_b = []
        current = self.parent_backward.get(meeting_point)
        while current is not None:
            path_b.append(current)
            current = self.parent_backward.get(current)
        
        return path_f + path_b

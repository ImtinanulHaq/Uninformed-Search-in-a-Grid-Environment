from . import SearchResult

class IDDFS:
    def __init__(self, grid):
        self.grid = grid
        self.explored = set()
        self.parent = {}
        self.frontier_history = []
    
    def search(self):
        max_depth = max(self.grid.width, self.grid.height) * 2
        all_explored = set()
        
        for limit in range(1, max_depth + 1):
            self.explored = set()
            self.parent = {}
            
            result = self.dfs_limited(limit)
            
            all_explored.update(self.explored)
            
            if result is not None:
                return SearchResult(True, result, all_explored, self.frontier_history)
        
        return SearchResult(False, [], all_explored, self.frontier_history)
    
    def dfs_limited(self, limit):
        self.parent[self.grid.start] = None
        result = self.dfs_recursive(self.grid.start, 0, limit)
        return result
    
    def dfs_recursive(self, node, depth, limit):
        if node in self.explored:
            return None
        
        self.explored.add(node)
        
        if node == self.grid.target:
            path = self.reconstruct_path(node)
            return path
        
        if depth < limit:
            neighbors = self.grid.get_neighbors(node)
            for neighbor in neighbors:
                if neighbor not in self.explored:
                    self.parent[neighbor] = node
                    result = self.dfs_recursive(neighbor, depth + 1, limit)
                    if result is not None:
                        return result
        
        return None
    
    def reconstruct_path(self, node):
        path = []
        current = node
        while current is not None:
            path.append(current)
            current = self.parent[current]
        path.reverse()
        return path

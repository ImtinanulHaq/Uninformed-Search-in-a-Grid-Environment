from . import SearchResult

class DFS:
    def __init__(self, grid):
        self.grid = grid
        self.explored = set()
        self.parent = {}
        self.frontier_history = []
    
    def search(self):
        frontier = [self.grid.start]
        in_frontier = {self.grid.start}
        self.parent[self.grid.start] = None
        
        while frontier:
            self.frontier_history.append(set(frontier))
            
            node = frontier.pop()
            in_frontier.discard(node)
            
            if node in self.explored:
                continue
            
            self.explored.add(node)
            
            if node == self.grid.target:
                path = self.reconstruct_path(node)
                return SearchResult(True, path, self.explored, self.frontier_history)
            
            neighbors = self.grid.get_neighbors(node)
            for neighbor in reversed(neighbors):
                if neighbor not in self.explored and neighbor not in in_frontier:
                    self.parent[neighbor] = node
                    frontier.append(neighbor)
                    in_frontier.add(neighbor)
        
        return SearchResult(False, [], self.explored, self.frontier_history)
    
    def reconstruct_path(self, node):
        path = []
        current = node
        while current is not None:
            path.append(current)
            current = self.parent[current]
        path.reverse()
        return path

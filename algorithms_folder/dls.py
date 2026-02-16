from . import SearchResult

class DLS:
    def __init__(self, grid, depth_limit=150):
        self.grid = grid
        self.explored = set()
        self.parent = {}
        self.frontier_history = []
        self.depth_limit = depth_limit
    
    def search(self):
        frontier = [(self.grid.start, 0)]
        in_frontier = {self.grid.start}
        self.parent[self.grid.start] = None
        
        while frontier:
            frontier_nodes = set([item[0] for item in frontier])
            self.frontier_history.append(frontier_nodes)
            
            node, depth = frontier.pop()
            in_frontier.discard(node)
            
            if node in self.explored:
                continue
            
            self.explored.add(node)
            
            if node == self.grid.target:
                path = self.reconstruct_path(node)
                return SearchResult(True, path, self.explored, self.frontier_history)
            
            if depth < self.depth_limit:
                neighbors = self.grid.get_neighbors(node)
                for neighbor in reversed(neighbors):
                    if neighbor not in self.explored and neighbor not in in_frontier:
                        self.parent[neighbor] = node
                        frontier.append((neighbor, depth + 1))
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

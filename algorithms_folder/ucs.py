import heapq
from . import SearchResult

class UCS:
    def __init__(self, grid):
        self.grid = grid
        self.explored = set()
        self.parent = {}
        self.frontier_history = []
        self.counter = 0
    
    def search(self):
        frontier = [(0, self.counter, self.grid.start)]
        self.counter += 1
        in_frontier = {self.grid.start}
        self.parent[self.grid.start] = None
        
        while frontier:
            frontier_nodes = set([item[2] for item in frontier])
            self.frontier_history.append(frontier_nodes)
            
            cost, _, node = heapq.heappop(frontier)
            in_frontier.discard(node)
            
            if node in self.explored:
                continue
            
            self.explored.add(node)
            
            if node == self.grid.target:
                path = self.reconstruct_path(node)
                return SearchResult(True, path, self.explored, self.frontier_history)
            
            neighbors = self.grid.get_neighbors(node)
            for neighbor in neighbors:
                if neighbor not in self.explored and neighbor not in in_frontier:
                    self.parent[neighbor] = node
                    new_cost = cost + 1
                    heapq.heappush(frontier, (new_cost, self.counter, neighbor))
                    self.counter += 1
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

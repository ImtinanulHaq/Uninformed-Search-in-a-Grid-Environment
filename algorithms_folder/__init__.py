class SearchResult:
    def __init__(self, found, path, explored, frontier_history):
        self.found = found
        self.path = path
        self.explored = explored
        self.frontier_history = frontier_history
        self.total_nodes_explored = len(explored)
        self.dynamic_obstacles_encountered = []

from .bfs import BFS
from .dfs import DFS
from .ucs import UCS
from .dls import DLS
from .iddfs import IDDFS
from .bidirectional import BidirectionalSearch

__all__ = ['SearchResult', 'BFS', 'DFS', 'UCS', 'DLS', 'IDDFS', 'BidirectionalSearch']

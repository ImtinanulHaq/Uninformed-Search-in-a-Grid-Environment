from grid import Grid
from algorithms_folder.bfs import BFS
from algorithms_folder.dfs import DFS
from algorithms_folder.ucs import UCS
from algorithms_folder.dls import DLS
from algorithms_folder.iddfs import IDDFS
from algorithms_folder.bidirectional import BidirectionalSearch
from visualizer_folder import GridVisualizer
import random


class GridPathfinder:
 
    
    def __init__(self, width: int = 50, height: int = 50, 
                 start: tuple = (5, 5), target: tuple = (45, 45),
                 num_walls: int = 250, dynamic_obstacle_probability: float = 0.0):
        """
        Initialize the pathfinder application.
        
        Args:
            width: Grid width
            height: Grid height
            start: Start position (x, y)
            target: Target position (x, y)
            num_walls: Number of static walls to generate
            dynamic_obstacle_probability: Probability of dynamic obstacle spawn
        """
        # Create grid with specified parameters
        self.grid = Grid(width, height, start, target, dynamic_obstacle_probability)
        
        # Add static walls randomly
        print(f"Generating {num_walls} random walls...")
        self.grid.add_walls_randomly(num_walls)
        print(f"✓ Created grid {width}×{height} with {len(self.grid.walls)} walls")
        print(f"  Start: {start}, Target: {target}")
        
        # Dictionary of available algorithms
        self.algorithms = {
            "BFS": BFS,
            "DFS": DFS,
            "UCS": UCS,
            "DLS": DLS,
            "IDDFS": IDDFS,
            "BIDIRECTIONAL": BidirectionalSearch,
        }
    
    def run_algorithm(self, algorithm_name: str, show_visualization: bool = True) -> None:
   
        if algorithm_name not in self.algorithms:
            print(f"✗ Algorithm '{algorithm_name}' not found!")
            print(f"  Available algorithms: {', '.join(self.algorithms.keys())}")
            return
        
        print(f"\n{'='*60}")
        print(f"Running {algorithm_name} algorithm...")
        print(f"{'='*60}")
        
        # Clear previous dynamic obstacles
        self.grid.clear_dynamic_obstacles()
        
        try:
            # Create algorithm instance
            algorithm_class = self.algorithms[algorithm_name]
            algorithm = algorithm_class(self.grid)
            
            # Execute search
            print("Executing search...")
            result = algorithm.search()
            
            # Print results
            self._print_results(algorithm_name, result)
            
            # Visualize if requested
            if show_visualization:
                print("\nStarting visualization... (Press SPACE or close window to continue)")
                visualizer = GridVisualizer(self.grid, animation_delay=0.01)
                visualizer.visualize_algorithm(algorithm_name, result)
                visualizer.close()
        
        except Exception as e:
            print(f"✗ Error running algorithm: {e}")
            import traceback
            traceback.print_exc()
    
    def run_all_algorithms(self, show_visualization: bool = False) -> None:

        print(f"\n{'='*60}")
        print("Running ALL algorithms for comparison...")
        print(f"{'='*60}\n")
        
        results_summary = {}
        
        for algorithm_name in self.algorithms.keys():
            # Clear previous dynamic obstacles for fair comparison
            self.grid.clear_dynamic_obstacles()
            
            try:
                # Create and run algorithm
                algorithm_class = self.algorithms[algorithm_name]
                algorithm = algorithm_class(self.grid)
                result = algorithm.search()
                
                # Store results
                results_summary[algorithm_name] = {
                    "found": result.found,
                    "path_length": len(result.path) if result.path else 0,
                    "nodes_explored": result.total_nodes_explored,
                }
                
                # Visualize if requested
                if show_visualization:
                    print(f"\nVisualizing {algorithm_name}...")
                    visualizer = GridVisualizer(self.grid, animation_delay=0.01)
                    visualizer.visualize_algorithm(algorithm_name, result)
                    visualizer.close()
            
            except Exception as e:
                print(f"✗ Error running {algorithm_name}: {e}")
        
        # Print comparison table
        self._print_comparison_table(results_summary)
    
    def _print_results(self, algorithm_name: str, result) -> None:

        print(f"\n{'─'*60}")
        print("RESULTS:")
        print(f"{'─'*60}")
        
        if result.found:
            print(f"✓ Target found!")
            print(f"  Path length: {len(result.path)} steps")
        else:
            print(f"✗ Target not found")
        
        print(f"  Nodes explored: {result.total_nodes_explored}")
        
        if result.dynamic_obstacles_encountered:
            print(f"  Dynamic obstacles encountered: {len(result.dynamic_obstacles_encountered)}")
            print(f"    Positions: {result.dynamic_obstacles_encountered}")
        
        print(f"{'─'*60}\n")
    
    def _print_comparison_table(self, results: dict) -> None:

        print(f"\n{'='*80}")
        print("COMPARISON OF ALL ALGORITHMS")
        print(f"{'='*80}")
        
        # Print header
        print(f"{'Algorithm':<20} {'Found':<8} {'Path Length':<15} {'Nodes Explored':<15}")
        print(f"{'-'*80}")
        
        # Print each result
        for algo_name, metrics in results.items():
            found_str = "Yes" if metrics["found"] else "No"
            path_len = metrics["path_length"] if metrics["path_length"] > 0 else "N/A"
            
            print(f"{algo_name:<20} {found_str:<8} {str(path_len):<15} {metrics['nodes_explored']:<15}")
        
        print(f"{'='*80}\n")
    
    def interactive_menu(self) -> None:

        while True:
            print(f"\n{'='*60}")
            print("UNINFORMED SEARCH PATHFINDER - INTERACTIVE MENU")
            print(f"{'='*60}")
            print("1. Run Breadth-First Search (BFS)")
            print("2. Run Depth-First Search (DFS)")
            print("3. Run Uniform Cost Search (UCS)")
            print("4. Run Depth-Limited Search (DLS)")
            print("5. Run Iterative Deepening DFS (IDDFS)")
            print("6. Run Bidirectional Search")
            print("7. Run ALL algorithms (with comparison)")
            print("8. Create new grid")
            print("0. Exit")
            print(f"{'='*60}")
            
            choice = input("Select option (0-8): ").strip()
            
            if choice == "1":
                self.run_algorithm("BFS", show_visualization=True)
            elif choice == "2":
                self.run_algorithm("DFS", show_visualization=True)
            elif choice == "3":
                self.run_algorithm("UCS", show_visualization=True)
            elif choice == "4":
                self.run_algorithm("DLS", show_visualization=True)
            elif choice == "5":
                self.run_algorithm("IDDFS", show_visualization=True)
            elif choice == "6":
                self.run_algorithm("BIDIRECTIONAL", show_visualization=True)
            elif choice == "7":
                self.run_all_algorithms(show_visualization=True)
            elif choice == "8":
                self._create_new_grid()
            elif choice == "0":
                print("Thank you for using the Uninformed Search Pathfinder!")
                break
            else:
                print("✗ Invalid option. Please try again.")
    
    def _create_new_grid(self) -> None:
        """Interactive grid creation."""
        print("\n" + "="*60)
        print("CREATE NEW GRID")
        print("="*60)
        
        try:
            width = int(input("Grid width (default 50): ") or "50")
            height = int(input("Grid height (default 50): ") or "50")
            
            num_walls = int(input("Number of walls (default 250): ") or "250")
            
            # Create new instance
            self.grid = Grid(width, height, (5, 5), (width - 6, height - 6), 0.02)
            self.grid.add_walls_randomly(num_walls)
            
            print(f"\n✓ Created new grid {width}×{height} with {len(self.grid.walls)} walls")
        
        except ValueError:
            print("✗ Invalid input. Please enter numbers only.")


def main():
    
    print("\n")
    print("(" + "═"*58 + ")")
    print("(" + " UNINFORMED SEARCH IN GRID ENVIRONMENT ".center(58) + ")")
    print("(" + " AI Pathfinder with Static Obstacles ".center(58) + ")")
    print("(" + "═"*58 + ")")
    
    # Create pathfinder with default settings
    # You can modify these parameters for different scenarios
    pathfinder = GridPathfinder(
        width=50,                           # Grid width
        height=50,                          # Grid height
        start=(5, 5),                       # Start position
        target=(45, 45),                    # Target position
        num_walls=250,                      # Number of static walls
        dynamic_obstacle_probability=0.0    # Disabled: obstacles are now static
    )
    
    # Start interactive menu
    pathfinder.interactive_menu()


if __name__ == "__main__":
    main()

"""
Visualization Module

This module provides a professional GUI visualization using Pygame.
It displays the grid, walls, obstacles, explored nodes, frontier nodes, and final paths.
Updates in real-time to show the algorithm's progress step-by-step.
"""

import pygame
from typing import List, Set, Tuple, Optional
from grid import Grid
from algorithms import SearchResult
import time


class Colors:
    """Color constants for visualization."""
    
    # Basic colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    
    # Grid element colors
    WALL = (40, 40, 40)              # Dark gray for walls
    EMPTY = (255, 255, 255)          # White for empty cells
    START = (0, 255, 0)              # Green for start position
    TARGET = (255, 0, 0)             # Red for target position
    EXPLORED = (173, 216, 230)       # Light blue for explored nodes
    FRONTIER = (255, 255, 0)         # Yellow for frontier nodes
    DYNAMIC_OBSTACLE = (255, 165, 0) # Orange for dynamic obstacles
    PATH = (0, 0, 255)               # Blue for final path
    
    # UI colors
    TEXT_COLOR = (0, 0, 0)           # Black text
    UI_BACKGROUND = (230, 230, 230)  # Light gray background


class GridVisualizer:
    """
    Professional GUI for visualizing search algorithms.
    
    Features:
    - Real-time animation of algorithm execution
    - Color-coded visualization of different node states
    - Information panel showing algorithm details and statistics
    - Progress bar for animation tracking
    - Legend explaining color meanings
    """
    
    def __init__(self, grid: Grid, window_width: int = 1200, 
                 animation_delay: float = 0.02, show_dynamic_obstacles: bool = True):
        """
        Initialize the visualizer.
        
        Args:
            grid: Grid object to visualize
            window_width: Total width of the window in pixels
            animation_delay: Delay between animation frames in seconds (lower = faster)
            show_dynamic_obstacles: Whether to highlight dynamic obstacles
        """
        self.grid = grid
        self.animation_delay = animation_delay
        self.show_dynamic_obstacles = show_dynamic_obstacles
        
        # Calculate optimal cell size based on window dimensions
        ui_width = 350  # Reserved space for information panel
        available_width = window_width - ui_width
        self.cell_size = max(10, available_width // grid.width)
        
        # Calculate actual dimensions
        self.grid_width = grid.width * self.cell_size
        self.grid_height = grid.height * self.cell_size
        self.window_width = self.grid_width + ui_width
        self.window_height = self.grid_height
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("GOOD PERFORMANCE TIME APP - Uninformed Search Visualization")
        
        # Setup fonts for different text sizes
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        self.font_title = pygame.font.Font(None, 28)
    
    def draw_grid(self) -> None:
        """Draw the grid with horizontal and vertical lines."""
        # Fill background with white
        self.screen.fill(Colors.WHITE)
        
        # Draw vertical grid lines
        for x in range(self.grid.width + 1):
            start_pos = (x * self.cell_size, 0)
            end_pos = (x * self.cell_size, self.grid_height)
            pygame.draw.line(self.screen, Colors.LIGHT_GRAY, start_pos, end_pos, 1)
        
        # Draw horizontal grid lines
        for y in range(self.grid.height + 1):
            start_pos = (0, y * self.cell_size)
            end_pos = (self.grid_width, y * self.cell_size)
            pygame.draw.line(self.screen, Colors.LIGHT_GRAY, start_pos, end_pos, 1)
    
    def draw_cell(self, pos: Tuple[int, int], color: Tuple[int, int, int], 
                  border: bool = False) -> None:
        """
        Draw a colored cell at the given position.
        
        Args:
            pos: Cell position (x, y) in grid coordinates
            color: RGB color tuple (r, g, b)
            border: Whether to draw a black border around the cell
        """
        x, y = pos
        
        # Calculate pixel coordinates with small padding
        rect = pygame.Rect(
            x * self.cell_size + 1,
            y * self.cell_size + 1,
            self.cell_size - 2,
            self.cell_size - 2
        )
        
        # Fill cell with color
        pygame.draw.rect(self.screen, color, rect)
        
        # Draw border if requested
        if border:
            pygame.draw.rect(self.screen, Colors.BLACK, rect, 2)
    
    def draw_ui_panel(self, algorithm_name: str, result: Optional[SearchResult] = None,
                     current_step: int = 0, total_steps: int = 0) -> None:
        """
        Draw the information panel on the right side of the screen.
        
        Shows:
        - Application title
        - Algorithm name
        - Grid dimensions
        - Search results (if available)
        - Animation progress
        
        Args:
            algorithm_name: Name of the search algorithm
            result: Search result object (None during initial setup)
            current_step: Current step in animation
            total_steps: Total steps in animation
        """
        # Draw panel background
        panel_rect = pygame.Rect(self.grid_width, 0, 350, self.window_height)
        pygame.draw.rect(self.screen, Colors.UI_BACKGROUND, panel_rect)
        pygame.draw.rect(self.screen, Colors.BLACK, panel_rect, 2)
        
        # Starting position for text
        x_offset = self.grid_width + 20
        y_offset = 20
        line_height = 30
        
        # === Application Title ===
        title_surface = self.font_title.render("GOOD PERFORMANCE", True, Colors.TEXT_COLOR)
        self.screen.blit(title_surface, (x_offset, y_offset))
        y_offset += 20
        
        title_surface2 = self.font_title.render("TIME APP", True, Colors.TEXT_COLOR)
        self.screen.blit(title_surface2, (x_offset, y_offset))
        y_offset += 40
        
        # === Algorithm Information ===
        algo_label = self.font_large.render("Algorithm:", True, Colors.TEXT_COLOR)
        self.screen.blit(algo_label, (x_offset, y_offset))
        y_offset += line_height
        
        algo_name = self.font_small.render(algorithm_name, True, (0, 100, 200))
        self.screen.blit(algo_name, (x_offset + 10, y_offset))
        y_offset += line_height + 10
        
        # === Grid Information ===
        grid_text = f"Grid Size: {self.grid.width} × {self.grid.height}"
        grid_surface = self.font_small.render(grid_text, True, Colors.TEXT_COLOR)
        self.screen.blit(grid_surface, (x_offset, y_offset))
        y_offset += line_height
        
        # === Search Results ===
        if result:
            # Show success or failure
            if result.found:
                status_text = "✓ Target Found!"
                status_color = (0, 150, 0)  # Green for success
            else:
                status_text = "✗ Target Not Found"
                status_color = (200, 0, 0)  # Red for failure
            
            status_surface = self.font_large.render(status_text, True, status_color)
            self.screen.blit(status_surface, (x_offset, y_offset))
            y_offset += line_height + 10
            
            # Show path length if path exists
            if result.path:
                path_text = f"Path Length: {len(result.path)} steps"
                path_surface = self.font_small.render(path_text, True, Colors.TEXT_COLOR)
                self.screen.blit(path_surface, (x_offset, y_offset))
                y_offset += line_height
            
            # Show number of explored nodes
            explored_text = f"Nodes Explored: {result.total_nodes_explored}"
            explored_surface = self.font_small.render(explored_text, True, Colors.TEXT_COLOR)
            self.screen.blit(explored_surface, (x_offset, y_offset))
            y_offset += line_height
            
            # Show dynamic obstacles if any
            if result.dynamic_obstacles_encountered:
                dyn_count = len(result.dynamic_obstacles_encountered)
                dyn_text = f"Dynamic Obstacles: {dyn_count}"
                dyn_surface = self.font_small.render(dyn_text, True, Colors.TEXT_COLOR)
                self.screen.blit(dyn_surface, (x_offset, y_offset))
                y_offset += line_height
        
        # === Animation Progress ===
        y_offset += 10
        if total_steps > 0:
            # Progress text
            progress_text = f"Progress: {current_step}/{total_steps}"
            progress_surface = self.font_small.render(progress_text, True, Colors.TEXT_COLOR)
            self.screen.blit(progress_surface, (x_offset, y_offset))
            y_offset += line_height
            
            # Progress bar
            bar_width = 300
            bar_height = 20
            
            # Draw background bar
            bar_background = pygame.Rect(x_offset, y_offset, bar_width, bar_height)
            pygame.draw.rect(self.screen, Colors.LIGHT_GRAY, bar_background)
            
            # Draw filled portion
            progress_ratio = current_step / total_steps if total_steps > 0 else 0
            filled_width = int(bar_width * progress_ratio)
            bar_filled = pygame.Rect(x_offset, y_offset, filled_width, bar_height)
            pygame.draw.rect(self.screen, (0, 150, 100), bar_filled)
            
            # Draw border
            pygame.draw.rect(self.screen, Colors.BLACK, bar_background, 2)
    
    def draw_legend(self) -> None:
        """Draw a color legend at the bottom of the UI panel."""
        # Legend items: (label, color)
        legend_items = [
            ("Start", Colors.START),
            ("Target", Colors.TARGET),
            ("Explored", Colors.EXPLORED),
            ("Frontier", Colors.FRONTIER),
            ("Final Path", Colors.PATH),
            ("Wall", Colors.WALL),
        ]
        
        # Position legend at bottom of UI panel
        x_offset = self.grid_width + 20
        y_offset = self.window_height - 200
        
        # Legend title
        legend_title = self.font_small.render("Legend:", True, Colors.TEXT_COLOR)
        self.screen.blit(legend_title, (x_offset, y_offset))
        y_offset += 25
        
        # Draw each legend item
        for label, color in legend_items:
            # Draw color box
            box_size = 15
            box_rect = pygame.Rect(x_offset, y_offset, box_size, box_size)
            pygame.draw.rect(self.screen, color, box_rect)
            pygame.draw.rect(self.screen, Colors.BLACK, box_rect, 1)
            
            # Draw label text
            label_surface = self.font_small.render(label, True, Colors.TEXT_COLOR)
            self.screen.blit(label_surface, (x_offset + 20, y_offset - 2))
            
            y_offset += 25
    
    def visualize_algorithm(self, algorithm_name: str, result: SearchResult,
                          explored_animation: Optional[List[Tuple[int, int]]] = None) -> None:
        """
        Animate the algorithm execution step-by-step.
        
        Shows two phases:
        1. Exploration phase: Nodes being explored one by one
        2. Path phase: Final path being drawn
        
        Args:
            algorithm_name: Name of the algorithm for display
            result: Complete search results
            explored_animation: Optional ordered list of explored nodes for smooth animation
        """
        step = 0
        total_steps = len(result.explored) + len(result.path)
        
        # Use custom animation order if provided
        if explored_animation:
            total_steps = len(explored_animation) + len(result.path)
        
        # === PHASE 1: Exploration Animation ===
        if explored_animation:
            # Animate exploration in order
            for i, pos in enumerate(explored_animation):
                # Check for quit event
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                
                # Draw base grid
                self.draw_grid()
                
                # Draw static walls
                for wall_pos in self.grid.walls:
                    self.draw_cell(wall_pos, Colors.WALL)
                
                # Draw explored nodes up to current step
                for explored_pos in explored_animation[:i + 1]:
                    # Don't overwrite start/target
                    if explored_pos != self.grid.start and explored_pos != self.grid.target:
                        self.draw_cell(explored_pos, Colors.EXPLORED)
                
                # Draw start and target on top
                self.draw_cell(self.grid.start, Colors.START, border=True)
                self.draw_cell(self.grid.target, Colors.TARGET, border=True)
                
                # Draw dynamic obstacles if enabled
                if self.show_dynamic_obstacles:
                    for dyn_obs in self.grid.dynamic_obstacles:
                        self.draw_cell(dyn_obs, Colors.DYNAMIC_OBSTACLE)
                
                # Update UI panel and legend
                self.draw_ui_panel(algorithm_name, result, i + 1, total_steps)
                self.draw_legend()
                
                # Update display
                pygame.display.flip()
                time.sleep(self.animation_delay)
                step = i + 1
        else:
            # Fallback: show all explored nodes at once
            self.draw_grid()
            for wall_pos in self.grid.walls:
                self.draw_cell(wall_pos, Colors.WALL)
            for pos in result.explored:
                if pos != self.grid.start and pos != self.grid.target:
                    self.draw_cell(pos, Colors.EXPLORED)
            self.draw_cell(self.grid.start, Colors.START, border=True)
            self.draw_cell(self.grid.target, Colors.TARGET, border=True)
            step = len(result.explored)
        
        # === PHASE 2: Path Animation ===
        if result.path:
            path_steps = len(result.path)
            
            for i in range(1, path_steps):
                # Check for quit event
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                
                # Redraw everything
                self.draw_grid()
                
                # Draw walls
                for wall_pos in self.grid.walls:
                    self.draw_cell(wall_pos, Colors.WALL)
                
                # Draw all explored nodes
                for explored_pos in result.explored:
                    if explored_pos != self.grid.start and explored_pos != self.grid.target:
                        self.draw_cell(explored_pos, Colors.EXPLORED)
                
                # Draw path up to current step (overwrites explored color)
                for path_pos in result.path[:i + 1]:
                    if path_pos != self.grid.start and path_pos != self.grid.target:
                        self.draw_cell(path_pos, Colors.PATH)
                
                # Draw start and target on top
                self.draw_cell(self.grid.start, Colors.START, border=True)
                self.draw_cell(self.grid.target, Colors.TARGET, border=True)
                
                # Draw dynamic obstacles if enabled
                if self.show_dynamic_obstacles:
                    for dyn_obs in self.grid.dynamic_obstacles:
                        self.draw_cell(dyn_obs, Colors.DYNAMIC_OBSTACLE)
                
                # Update UI and legend
                self.draw_ui_panel(algorithm_name, result, step + i, total_steps)
                self.draw_legend()
                
                # Update display
                pygame.display.flip()
                time.sleep(self.animation_delay)
        
        # === FINAL STATE: Show complete result ===
        self.draw_grid()
        
        # Draw walls
        for wall_pos in self.grid.walls:
            self.draw_cell(wall_pos, Colors.WALL)
        
        # Draw all explored nodes
        for explored_pos in result.explored:
            if explored_pos != self.grid.start and explored_pos != self.grid.target:
                self.draw_cell(explored_pos, Colors.EXPLORED)
        
        # Draw complete final path
        if result.path:
            for path_pos in result.path:
                if path_pos != self.grid.start and path_pos != self.grid.target:
                    self.draw_cell(path_pos, Colors.PATH)
        
        # Draw start and target
        self.draw_cell(self.grid.start, Colors.START, border=True)
        self.draw_cell(self.grid.target, Colors.TARGET, border=True)
        
        # Draw dynamic obstacles
        if self.show_dynamic_obstacles:
            for dyn_obs in self.grid.dynamic_obstacles:
                self.draw_cell(dyn_obs, Colors.DYNAMIC_OBSTACLE)
        
        # Final UI update
        self.draw_ui_panel(algorithm_name, result, total_steps, total_steps)
        self.draw_legend()
        
        pygame.display.flip()
        
        # Wait for user to close window or press space
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        waiting = False
    
    def close(self) -> None:
        """Clean up and close the Pygame window."""
        pygame.quit()
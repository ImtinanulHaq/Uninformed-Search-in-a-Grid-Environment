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
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    
    # Algorithm visualization colors
    WALL = (40, 40, 40)
    EMPTY = (255, 255, 255)
    START = (0, 255, 0)  # Green
    TARGET = (255, 0, 0)  # Red
    EXPLORED = (173, 216, 230)  # Light blue
    FRONTIER = (255, 255, 0)  # Yellow
    DYNAMIC_OBSTACLE = (255, 165, 0)  # Orange
    PATH = (0, 0, 255)  # Blue
    
    # UI colors
    TEXT_COLOR = (0, 0, 0)
    UI_BACKGROUND = (230, 230, 230)


class GridVisualizer:
    """
    Professional GUI for visualizing search algorithms.
    
    Attributes:
        grid: Grid object being visualized
        cell_size: Size of each grid cell in pixels
        animation_delay: Delay between animation frames in seconds
        show_dynamic_obstacles: Whether to highlight dynamic obstacles
    """
    
    def __init__(self, grid: Grid, window_width: int = 1200, 
                 animation_delay: float = 0.02, show_dynamic_obstacles: bool = True):
        """
        Initialize the visualizer.
        
        Args:
            grid: Grid to visualize
            window_width: Width of the display window
            animation_delay: Delay between animation frames
            show_dynamic_obstacles: Show dynamic obstacles during animation
        """
        self.grid = grid
        self.animation_delay = animation_delay
        self.show_dynamic_obstacles = show_dynamic_obstacles
        
        # Calculate cell size based on window width
        ui_width = 350  # Width reserved for UI panel
        self.cell_size = max(10, (window_width - ui_width) // grid.width)
        
        self.grid_width = grid.width * self.cell_size
        self.grid_height = grid.height * self.cell_size
        
        self.window_width = self.grid_width + ui_width
        self.window_height = self.grid_height
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("GOOD PERFORMANCE TIME APP - Uninformed Search Visualization")
        
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        self.font_title = pygame.font.Font(None, 28)
    
    def draw_grid(self) -> None:
        """Draw the empty grid."""
        self.screen.fill(Colors.WHITE)
        
        # Draw grid lines
        for x in range(self.grid.width + 1):
            pygame.draw.line(
                self.screen,
                Colors.LIGHT_GRAY,
                (x * self.cell_size, 0),
                (x * self.cell_size, self.grid_height),
                1
            )
        
        for y in range(self.grid.height + 1):
            pygame.draw.line(
                self.screen,
                Colors.LIGHT_GRAY,
                (0, y * self.cell_size),
                (self.grid_width, y * self.cell_size),
                1
            )
    
    def draw_cell(self, pos: Tuple[int, int], color: Tuple[int, int, int], 
                  border: bool = False) -> None:
        """
        Draw a cell at the given position.
        
        Args:
            pos: Cell position (x, y)
            color: RGB color tuple
            border: Whether to draw a border around the cell
        """
        x, y = pos
        rect = pygame.Rect(
            x * self.cell_size + 1,
            y * self.cell_size + 1,
            self.cell_size - 2,
            self.cell_size - 2
        )
        pygame.draw.rect(self.screen, color, rect)
        
        if border:
            pygame.draw.rect(self.screen, Colors.BLACK, rect, 2)
    
    def draw_ui_panel(self, algorithm_name: str, result: Optional[SearchResult] = None,
                     current_step: int = 0, total_steps: int = 0) -> None:
        """
        Draw the UI information panel on the right side.
        
        Args:
            algorithm_name: Name of the algorithm being run
            result: Search result object (if available)
            current_step: Current animation step
            total_steps: Total animation steps
        """
        # Draw background panel
        panel_rect = pygame.Rect(self.grid_width, 0, 350, self.window_height)
        pygame.draw.rect(self.screen, Colors.UI_BACKGROUND, panel_rect)
        pygame.draw.rect(self.screen, Colors.BLACK, panel_rect, 2)
        
        x_offset = self.grid_width + 20
        y_offset = 20
        line_height = 30
        
        # Title
        title_surface = self.font_title.render("GOOD PERFORMANCE", True, Colors.TEXT_COLOR)
        self.screen.blit(title_surface, (x_offset, y_offset))
        y_offset += 20
        title_surface2 = self.font_title.render("TIME APP", True, Colors.TEXT_COLOR)
        self.screen.blit(title_surface2, (x_offset, y_offset))
        y_offset += 40
        
        # Algorithm name
        algo_surface = self.font_large.render(f"Algorithm:", True, Colors.TEXT_COLOR)
        self.screen.blit(algo_surface, (x_offset, y_offset))
        y_offset += line_height
        
        name_surface = self.font_small.render(algorithm_name, True, (0, 100, 200))
        self.screen.blit(name_surface, (x_offset + 10, y_offset))
        y_offset += line_height + 10
        
        # Grid information
        grid_info = self.font_small.render(f"Grid: {self.grid.width}×{self.grid.height}", 
                                           True, Colors.TEXT_COLOR)
        self.screen.blit(grid_info, (x_offset, y_offset))
        y_offset += line_height
        
        # Results if available
        if result:
            if result.found:
                status = "✓ Target Found!"
                status_color = (0, 150, 0)
            else:
                status = "✗ Target Not Found"
                status_color = (200, 0, 0)
            
            status_surface = self.font_large.render(status, True, status_color)
            self.screen.blit(status_surface, (x_offset, y_offset))
            y_offset += line_height + 10
            
            # Path length
            if result.path:
                path_length = self.font_small.render(
                    f"Path Length: {len(result.path)}", True, Colors.TEXT_COLOR
                )
                self.screen.blit(path_length, (x_offset, y_offset))
                y_offset += line_height
            
            # Nodes explored
            explored_text = self.font_small.render(
                f"Nodes Explored: {result.total_nodes_explored}", True, Colors.TEXT_COLOR
            )
            self.screen.blit(explored_text, (x_offset, y_offset))
            y_offset += line_height
            
            # Dynamic obstacles encountered
            if result.dynamic_obstacles_encountered:
                dyn_text = self.font_small.render(
                    f"Dynamic Obstacles: {len(result.dynamic_obstacles_encountered)}", 
                    True, Colors.TEXT_COLOR
                )
                self.screen.blit(dyn_text, (x_offset, y_offset))
                y_offset += line_height
        
        # Animation progress
        y_offset += 10
        if total_steps > 0:
            progress_text = self.font_small.render(
                f"Progress: {current_step}/{total_steps}", True, Colors.TEXT_COLOR
            )
            self.screen.blit(progress_text, (x_offset, y_offset))
            y_offset += line_height
            
            # Progress bar
            bar_width = 300
            bar_height = 20
            bar_rect = pygame.Rect(x_offset, y_offset, bar_width, bar_height)
            pygame.draw.rect(self.screen, Colors.LIGHT_GRAY, bar_rect)
            
            progress = current_step / total_steps if total_steps > 0 else 0
            filled_width = int(bar_width * progress)
            filled_rect = pygame.Rect(x_offset, y_offset, filled_width, bar_height)
            pygame.draw.rect(self.screen, (0, 150, 100), filled_rect)
            pygame.draw.rect(self.screen, Colors.BLACK, bar_rect, 2)
    
    def draw_legend(self) -> None:
        """Draw a legend explaining the colors."""
        legend_items = [
            ("Start", Colors.START),
            ("Target", Colors.TARGET),
            ("Explored", Colors.EXPLORED),
            ("Frontier", Colors.FRONTIER),
            ("Final Path", Colors.PATH),
            ("Wall", Colors.WALL),
        ]
        
        x_offset = self.grid_width + 20
        y_offset = self.window_height - 200
        
        legend_title = self.font_small.render("Legend:", True, Colors.TEXT_COLOR)
        self.screen.blit(legend_title, (x_offset, y_offset))
        y_offset += 25
        
        for label, color in legend_items:
            # Draw color box
            box_rect = pygame.Rect(x_offset, y_offset, 15, 15)
            pygame.draw.rect(self.screen, color, box_rect)
            pygame.draw.rect(self.screen, Colors.BLACK, box_rect, 1)
            
            # Draw label
            label_surface = self.font_small.render(label, True, Colors.TEXT_COLOR)
            self.screen.blit(label_surface, (x_offset + 20, y_offset - 2))
            
            y_offset += 25
    
    def visualize_algorithm(self, algorithm_name: str, result: SearchResult,
                          explored_animation: List[Tuple[int, int]] = None) -> None:
        """
        Animate the algorithm execution step-by-step.
        
        Args:
            algorithm_name: Name of the algorithm
            result: Search result with exploration and path data
            explored_animation: Optional list of exploration order for smooth animation
        """
        step = 0
        total_steps = len(result.explored) + len(result.path)
        
        if explored_animation:
            total_steps = len(explored_animation) + len(result.path)
        
        # Animation phase 1: Show exploration
        if explored_animation:
            for i, pos in enumerate(explored_animation):
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                
                # Draw everything
                self.draw_grid()
                
                # Draw walls
                for wall_pos in self.grid.walls:
                    self.draw_cell(wall_pos, Colors.WALL)
                
                # Draw explored nodes up to current step
                for explored_pos in explored_animation[:i + 1]:
                    if explored_pos != self.grid.start and explored_pos != self.grid.target:
                        self.draw_cell(explored_pos, Colors.EXPLORED)
                
                # Draw start and target
                self.draw_cell(self.grid.start, Colors.START, border=True)
                self.draw_cell(self.grid.target, Colors.TARGET, border=True)
                
                # Draw dynamic obstacles
                if self.show_dynamic_obstacles:
                    for dyn_obs in self.grid.dynamic_obstacles:
                        self.draw_cell(dyn_obs, Colors.DYNAMIC_OBSTACLE)
                
                # Draw UI
                self.draw_ui_panel(algorithm_name, result, i + 1, total_steps)
                self.draw_legend()
                
                pygame.display.flip()
                time.sleep(self.animation_delay)
                step = i + 1
        else:
            # Fallback: just show all explored nodes
            for pos in result.explored:
                if pos != self.grid.start and pos != self.grid.target:
                    self.draw_cell(pos, Colors.EXPLORED)
            step = len(result.explored)
        
        # Animation phase 2: Show final path
        if result.path:
            path_animation_steps = len(result.path)
            for i in range(1, path_animation_steps):
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                
                # Draw everything
                self.draw_grid()
                
                # Draw walls
                for wall_pos in self.grid.walls:
                    self.draw_cell(wall_pos, Colors.WALL)
                
                # Draw explored nodes
                for explored_pos in result.explored:
                    if explored_pos != self.grid.start and explored_pos != self.grid.target:
                        self.draw_cell(explored_pos, Colors.EXPLORED)
                
                # Draw path up to current step
                for path_pos in result.path[:i + 1]:
                    if path_pos != self.grid.start and path_pos != self.grid.target:
                        self.draw_cell(path_pos, Colors.PATH)
                
                # Draw start and target
                self.draw_cell(self.grid.start, Colors.START, border=True)
                self.draw_cell(self.grid.target, Colors.TARGET, border=True)
                
                # Draw dynamic obstacles
                if self.show_dynamic_obstacles:
                    for dyn_obs in self.grid.dynamic_obstacles:
                        self.draw_cell(dyn_obs, Colors.DYNAMIC_OBSTACLE)
                
                # Draw UI
                self.draw_ui_panel(algorithm_name, result, step + i, total_steps)
                self.draw_legend()
                
                pygame.display.flip()
                time.sleep(self.animation_delay)
        
        # Show final result
        self.draw_grid()
        
        # Draw walls
        for wall_pos in self.grid.walls:
            self.draw_cell(wall_pos, Colors.WALL)
        
        # Draw explored nodes
        for explored_pos in result.explored:
            if explored_pos != self.grid.start and explored_pos != self.grid.target:
                self.draw_cell(explored_pos, Colors.EXPLORED)
        
        # Draw final path
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
        
        # Draw UI
        self.draw_ui_panel(algorithm_name, result, total_steps, total_steps)
        self.draw_legend()
        
        pygame.display.flip()
        
        # Wait for user interaction
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
    
    def close(self) -> None:
        """Close the visualization window."""
        pygame.quit()

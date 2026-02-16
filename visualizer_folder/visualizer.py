import pygame
from typing import List, Set, Tuple, Optional
from grid import Grid
from algorithms_folder import SearchResult
import time
from .colors import Colors


class GridVisualizer:
    
    def __init__(self, grid: Grid, window_width: int = 1200, 
                 animation_delay: float = 0.02, show_dynamic_obstacles: bool = True):
  
        self.grid = grid
        self.animation_delay = animation_delay
        self.show_dynamic_obstacles = show_dynamic_obstacles
        
        ui_width = 350
        available_width = window_width - ui_width
        self.cell_size = max(10, available_width // grid.width)
        
        self.grid_width = grid.width * self.cell_size
        self.grid_height = grid.height * self.cell_size
        self.window_width = self.grid_width + ui_width
        self.window_height = self.grid_height
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Pathfinder Algorithm Visualizer - Uninformed Search")
        
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        self.font_title = pygame.font.Font(None, 28)
    
    def draw_grid(self) -> None:
        self.screen.fill(Colors.WHITE)
        
        for x in range(self.grid.width + 1):
            start_pos = (x * self.cell_size, 0)
            end_pos = (x * self.cell_size, self.grid_height)
            pygame.draw.line(self.screen, Colors.LIGHT_GRAY, start_pos, end_pos, 1)
        
        for y in range(self.grid.height + 1):
            start_pos = (0, y * self.cell_size)
            end_pos = (self.grid_width, y * self.cell_size)
            pygame.draw.line(self.screen, Colors.LIGHT_GRAY, start_pos, end_pos, 1)
    
    def draw_cell(self, pos: Tuple[int, int], color: Tuple[int, int, int], 
                  border: bool = False) -> None:
 
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

        panel_rect = pygame.Rect(self.grid_width, 0, 350, self.window_height)
        pygame.draw.rect(self.screen, Colors.UI_BACKGROUND, panel_rect)
        pygame.draw.rect(self.screen, Colors.BLACK, panel_rect, 2)
        
        x_offset = self.grid_width + 20
        y_offset = 20
        line_height = 30
        
        title_surface = self.font_title.render("Pathfinder", True, Colors.TEXT_COLOR)
        self.screen.blit(title_surface, (x_offset, y_offset))
        y_offset += 20
        
        title_surface2 = self.font_title.render("Engine", True, Colors.TEXT_COLOR)
        self.screen.blit(title_surface2, (x_offset, y_offset))
        y_offset += 40
        
        algo_label = self.font_large.render("Algorithm:", True, Colors.TEXT_COLOR)
        self.screen.blit(algo_label, (x_offset, y_offset))
        y_offset += line_height
        
        algo_name = self.font_small.render(algorithm_name, True, (0, 100, 200))
        self.screen.blit(algo_name, (x_offset + 10, y_offset))
        y_offset += line_height + 10
        
        grid_text = f"Grid Size: {self.grid.width} × {self.grid.height}"
        grid_surface = self.font_small.render(grid_text, True, Colors.TEXT_COLOR)
        self.screen.blit(grid_surface, (x_offset, y_offset))
        y_offset += line_height
        
        if result:
            if result.found:
                status_text = " Target Found!"
                status_color = (0, 150, 0)
            else:
                status_text = " Target Not Found"
                status_color = (200, 0, 0)
            
            status_surface = self.font_large.render(status_text, True, status_color)
            self.screen.blit(status_surface, (x_offset, y_offset))
            y_offset += line_height + 10
            
            if result.path:
                path_text = f"Path Length: {len(result.path)} steps"
                path_surface = self.font_small.render(path_text, True, Colors.TEXT_COLOR)
                self.screen.blit(path_surface, (x_offset, y_offset))
                y_offset += line_height
            
            explored_text = f"Nodes Explored: {result.total_nodes_explored}"
            explored_surface = self.font_small.render(explored_text, True, Colors.TEXT_COLOR)
            self.screen.blit(explored_surface, (x_offset, y_offset))
            y_offset += line_height
            
            if result.dynamic_obstacles_encountered:
                dyn_count = len(result.dynamic_obstacles_encountered)
                dyn_text = f"Dynamic Obstacles: {dyn_count}"
                dyn_surface = self.font_small.render(dyn_text, True, Colors.TEXT_COLOR)
                self.screen.blit(dyn_surface, (x_offset, y_offset))
                y_offset += line_height
        
        y_offset += 10
        if total_steps > 0:
            progress_text = f"Progress: {current_step}/{total_steps}"
            progress_surface = self.font_small.render(progress_text, True, Colors.TEXT_COLOR)
            self.screen.blit(progress_surface, (x_offset, y_offset))
            y_offset += line_height
            
            bar_width = 300
            bar_height = 20
            
            bar_background = pygame.Rect(x_offset, y_offset, bar_width, bar_height)
            pygame.draw.rect(self.screen, Colors.LIGHT_GRAY, bar_background)
            
            progress_ratio = current_step / total_steps if total_steps > 0 else 0
            filled_width = int(bar_width * progress_ratio)
            bar_filled = pygame.Rect(x_offset, y_offset, filled_width, bar_height)
            pygame.draw.rect(self.screen, (0, 150, 100), bar_filled)
            
            pygame.draw.rect(self.screen, Colors.BLACK, bar_background, 2)
    
    def draw_legend(self) -> None:
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
            box_size = 15
            box_rect = pygame.Rect(x_offset, y_offset, box_size, box_size)
            pygame.draw.rect(self.screen, color, box_rect)
            pygame.draw.rect(self.screen, Colors.BLACK, box_rect, 1)
            
            label_surface = self.font_small.render(label, True, Colors.TEXT_COLOR)
            self.screen.blit(label_surface, (x_offset + 20, y_offset - 2))
            
            y_offset += 25
    
    def visualize_algorithm(self, algorithm_name: str, result: SearchResult,
                          explored_animation: Optional[List[Tuple[int, int]]] = None) -> None:
   
        step = 0
        total_steps = len(result.explored) + len(result.path)
        
        if explored_animation:
            total_steps = len(explored_animation) + len(result.path)
        
        if explored_animation:
            for i, pos in enumerate(explored_animation):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                
                self.draw_grid()
                
                for wall_pos in self.grid.walls:
                    self.draw_cell(wall_pos, Colors.WALL)
                
                for explored_pos in explored_animation[:i + 1]:
                    if explored_pos != self.grid.start and explored_pos != self.grid.target:
                        self.draw_cell(explored_pos, Colors.EXPLORED)
                
                self.draw_cell(self.grid.start, Colors.START, border=True)
                self.draw_cell(self.grid.target, Colors.TARGET, border=True)
                
                if self.show_dynamic_obstacles:
                    for dyn_obs in self.grid.dynamic_obstacles:
                        self.draw_cell(dyn_obs, Colors.DYNAMIC_OBSTACLE)
                
                self.draw_ui_panel(algorithm_name, result, i + 1, total_steps)
                self.draw_legend()
                
                pygame.display.flip()
                time.sleep(self.animation_delay)
                step = i + 1
        else:
            self.draw_grid()
            for wall_pos in self.grid.walls:
                self.draw_cell(wall_pos, Colors.WALL)
            for pos in result.explored:
                if pos != self.grid.start and pos != self.grid.target:
                    self.draw_cell(pos, Colors.EXPLORED)
            self.draw_cell(self.grid.start, Colors.START, border=True)
            self.draw_cell(self.grid.target, Colors.TARGET, border=True)
            step = len(result.explored)
        
        if result.path:
            path_steps = len(result.path)
            
            for i in range(1, path_steps):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                
                self.draw_grid()
                
                for wall_pos in self.grid.walls:
                    self.draw_cell(wall_pos, Colors.WALL)
                
                for explored_pos in result.explored:
                    if explored_pos != self.grid.start and explored_pos != self.grid.target:
                        self.draw_cell(explored_pos, Colors.EXPLORED)
                
                for path_pos in result.path[:i + 1]:
                    if path_pos != self.grid.start and path_pos != self.grid.target:
                        self.draw_cell(path_pos, Colors.PATH)
                
                self.draw_cell(self.grid.start, Colors.START, border=True)
                self.draw_cell(self.grid.target, Colors.TARGET, border=True)
                
                if self.show_dynamic_obstacles:
                    for dyn_obs in self.grid.dynamic_obstacles:
                        self.draw_cell(dyn_obs, Colors.DYNAMIC_OBSTACLE)
                
                self.draw_ui_panel(algorithm_name, result, step + i, total_steps)
                self.draw_legend()
                
                pygame.display.flip()
                time.sleep(self.animation_delay)
        
        self.draw_grid()
        
        for wall_pos in self.grid.walls:
            self.draw_cell(wall_pos, Colors.WALL)
        
        for explored_pos in result.explored:
            if explored_pos != self.grid.start and explored_pos != self.grid.target:
                self.draw_cell(explored_pos, Colors.EXPLORED)
        
        if result.path:
            for path_pos in result.path:
                if path_pos != self.grid.start and path_pos != self.grid.target:
                    self.draw_cell(path_pos, Colors.PATH)
        
        self.draw_cell(self.grid.start, Colors.START, border=True)
        self.draw_cell(self.grid.target, Colors.TARGET, border=True)
        
        if self.show_dynamic_obstacles:
            for dyn_obs in self.grid.dynamic_obstacles:
                self.draw_cell(dyn_obs, Colors.DYNAMIC_OBSTACLE)
        
        self.draw_ui_panel(algorithm_name, result, total_steps, total_steps)
        self.draw_legend()
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        waiting = False
    
    def close(self) -> None:
        pygame.quit()

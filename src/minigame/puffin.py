import pygame
import random
import sys

class PuffinMaze:
    def __init__(self, display):
        pygame.init()
        
        # Use display parameters
        self.display = display
        self.screen = display.screen
        self.width = display.width
        self.height = display.height
        
        # Constants
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)

        # Clock for controlling game speed
        self.clock = pygame.time.Clock()
        
        # Background image
        try:
            self.background_image = pygame.image.load("src/images/minigame_backgrounds/puffin_habitat2.png")
            self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        except pygame.error:
            # Fallback to a simple background if image can't be loaded
            self.background_image = pygame.Surface((self.width, self.height))
            self.background_image.fill((135, 206, 235))  # Sky blue
        
        # Load puffin image
        try:
            self.puffin_image = pygame.image.load("src/images/animals/puffin.png")
        except pygame.error:
            # Create a placeholder if image can't be loaded
            self.puffin_image = pygame.Surface((50, 50))
            self.puffin_image.fill((255, 0, 0))
        
        # Font setup
        self.font = pygame.font.SysFont('Arial', 24)
        self.level_font = pygame.font.SysFont('Arial', 36)
        
        # Level configurations
        self.LEVELS = [
            {"name": "Easy", "grid_width": 10, "grid_height": 8, "color": self.GREEN},
            {"name": "Medium", "grid_width": 15, "grid_height": 12, "color": self.YELLOW},
            {"name": "Hard", "grid_width": 20, "grid_height": 15, "color": self.RED}
        ]

    class Cell:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.visited = False
            self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
            
        def get_neighbors(self, grid):
            neighbors = []
            directions = [('top', 0, -1), ('right', 1, 0), ('bottom', 0, 1), ('left', -1, 0)]
            
            for direction, dx, dy in directions:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and not grid[ny][nx].visited:
                    neighbors.append((direction, grid[ny][nx]))
            
            return neighbors
        
        def remove_wall(self, other, direction):
            opposite = {'top': 'bottom', 'right': 'left', 'bottom': 'top', 'left': 'right'}
            self.walls[direction] = False
            other.walls[opposite[direction]] = False
        
        def draw(self, surface, cell_size, offset_x, offset_y, wall_color=(0,0,0), wall_width=8):
            x, y = offset_x + self.x * cell_size, offset_y + self.y * cell_size
            
            if self.walls['top']:
                pygame.draw.line(surface, wall_color, (x, y), (x + cell_size, y), wall_width)  
            if self.walls['right']:
                pygame.draw.line(surface, wall_color, (x + cell_size, y), (x + cell_size, y + cell_size), wall_width)
            if self.walls['bottom']:
                pygame.draw.line(surface, wall_color, (x, y + cell_size), (x + cell_size, y + cell_size), wall_width)
            if self.walls['left']:
                pygame.draw.line(surface, wall_color, (x, y), (x, y + cell_size), wall_width)

    def generate_maze(self, width, height):
        # Create grid of cells
        grid = [[self.Cell(x, y) for x in range(width)] for y in range(height)]
        
        # Start from a random cell
        start_x, start_y = random.randint(0, width-1), random.randint(0, height-1)
        current = grid[start_y][start_x]
        current.visited = True
        
        # Stack for backtracking
        stack = [current]
        
        while stack:
            current = stack[-1]
            neighbors = current.get_neighbors(grid)
            
            if not neighbors:
                stack.pop()
                continue
            
            direction, next_cell = random.choice(neighbors)
            current.remove_wall(next_cell, direction)
            next_cell.visited = True
            stack.append(next_cell)
        
        # Reset visited flag
        for row in grid:
            for cell in row:
                cell.visited = False
                
        return grid

    class Puffin:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            
        def move(self, dx, dy, grid):
            new_x, new_y = self.x + dx, self.y + dy
            
            # Check if the move is valid (no wall in the way)
            if dx == 1 and not grid[self.y][self.x].walls['right']:
                self.x = new_x
            elif dx == -1 and not grid[self.y][self.x].walls['left']:
                self.x = new_x
            elif dy == 1 and not grid[self.y][self.x].walls['bottom']:
                self.y = new_y
            elif dy == -1 and not grid[self.y][self.x].walls['top']:
                self.y = new_y
                
        def draw(self, surface, cell_size, puffin_image, offset_x=0, offset_y=0):
            # Draw puffin image
            x = offset_x + self.x * cell_size
            y = offset_y + self.y * cell_size
            surface.blit(puffin_image, (x, y))

    def draw_family(self, surface, x, y, cell_size, puffin_image, offset_x=0, offset_y=0):
        # Draw a group of puffins
        real_x = offset_x + x
        real_y = offset_y + y
        
        scale = cell_size / 40  # Scale factor based on original cell size
        positions = [
            (real_x + 5 * scale, real_y - 5 * scale), 
            (real_x - 10 * scale, real_y + 5 * scale), 
            (real_x + 10 * scale, real_y + 10 * scale)
        ]
        
        for px, py in positions:
            # Draw puffin image
            surface.blit(puffin_image, (px - puffin_image.get_width() // 2, py - puffin_image.get_height() // 2))

    def show_level_transition(self, surface, level_name, color):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill(self.BLACK)
        surface.blit(overlay, (0, 0))
        
        # Display level name
        level_text = self.level_font.render(f"Level: {level_name}", True, color)
        text_rect = level_text.get_rect(center=(self.width // 2, self.height // 2))
        surface.blit(level_text, text_rect)
        
        # Display "Get Ready" message
        ready_text = self.font.render("Get Ready...", True, self.WHITE)
        ready_rect = ready_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        surface.blit(ready_text, ready_rect)
        
        pygame.display.flip()
        pygame.time.delay(2000)  # Show for 2 seconds

    def show_puffin_fun_fact(self):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(220)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Prepare fun fact text about puffins in Aberdeen
        title = "Congratulations! The puffin made it back to their family."
        fact_lines = [
            "Fun Fact: Puffins in Aberdeen!",
            "",
            "The Troup Head nature reserve near Aberdeen is home to one of the largest",
            "gannet colonies in the world, and also hosts a significant population of puffins.",
            "Over 1,500 puffin pairs nest on the rocky cliffs, making it a prime location", 
            "for these charming seabirds in Scotland."
        ]
        
        # Render puffin image
        scaled_puffin = pygame.transform.scale(self.puffin_image, (200, 200))
        puffin_rect = scaled_puffin.get_rect(center=(self.width // 2, self.height // 2 - 140))
        self.screen.blit(scaled_puffin, puffin_rect)
        
        # Render fact text with improved positioning
        title_font = pygame.font.SysFont('Arial', 36, bold = True)
        body_font = self.display.font
        
        # Render title separately
        title = title_font.render(title, True, (100, 255, 100))
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(title, title_rect)
        
        # Render body text
        for i, line in enumerate(fact_lines):
            text = body_font.render(line, True, self.WHITE)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2 + (i+1) * 30))
            self.screen.blit(text, text_rect)
        
        # Render continue instruction
        continue_text = body_font.render("Press any key to continue", True, self.WHITE)
        continue_rect = continue_text.get_rect(center=(self.width // 2, self.height - 40))
        self.screen.blit(continue_text, continue_rect)
        
        pygame.display.flip()
        
        # Wait for key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    waiting = False
        
        return

    def run(self):
        current_level = 0
        level_transition = True
        
        while True:  # Main game loop that handles multiple levels
            # Get current level configuration
            level_config = self.LEVELS[current_level]
            grid_width = level_config["grid_width"]
            grid_height = level_config["grid_height"]
            level_color = level_config["color"]
            
            # Calculate cell size based on maze dimensions to fill the screen
            cell_size = min(self.width // grid_width, self.height // grid_height)
            maze_width = cell_size * grid_width
            maze_height = cell_size * grid_height
            maze_x = (self.width - maze_width) // 2
            maze_y = (self.height - maze_height) // 2
            
            # Scale puffin image based on cell size
            puffin_image = pygame.transform.scale(self.puffin_image, (cell_size, cell_size))
            
            # Generate maze for this level
            maze = self.generate_maze(grid_width, grid_height)
            
            # Set up puffin and family positions
            puffin = self.Puffin(0, 0)
            family_x, family_y = grid_width - 1, grid_height - 1
            
            moves = 0  # Keep the moves counter
            level_complete = False
            
            # Show level transition screen
            if level_transition:
                self.show_level_transition(self.screen, level_config["name"], level_color)
                level_transition = False
            
            # Level game loop
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    
                    if event.type == pygame.KEYDOWN and not level_complete:
                        if event.key == pygame.K_UP:
                            puffin.move(0, -1, maze)
                            moves += 1  # Increment moves counter
                        elif event.key == pygame.K_DOWN:
                            puffin.move(0, 1, maze)
                            moves += 1
                        elif event.key == pygame.K_LEFT:
                            puffin.move(-1, 0, maze)
                            moves += 1
                        elif event.key == pygame.K_RIGHT:
                            puffin.move(1, 0, maze)
                            moves += 1
                        
                        # Check if puffin found family
                        if puffin.x == family_x and puffin.y == family_y:
                            level_complete = True
                    if event.type == pygame.VIDEORESIZE:
                        pygame.display.set_mode((self.display.width, self.display.height))
                
                # Draw background image
                self.screen.blit(self.background_image, (0, 0))
                
                # Draw maze with offsets
                for row in maze:
                    for cell in row:
                        cell.draw(self.screen, cell_size, maze_x, maze_y, wall_color=self.BLACK)
                
                # Draw family at destination with offsets
                family_center_x = family_x * cell_size + cell_size // 2
                family_center_y = family_y * cell_size + cell_size // 2
                self.draw_family(self.screen, family_center_x, family_center_y, cell_size, puffin_image, maze_x, maze_y)
                
                # Draw puffin with offsets
                puffin.draw(self.screen, cell_size, puffin_image, maze_x, maze_y)
                
                # Draw moves counter and level info
                moves_text = self.font.render(f"Moves: {moves}", True, self.BLACK)
                level_text = self.font.render(f"Level: {level_config['name']}", True, self.BLACK)
                
                self.screen.blit(moves_text, (10, 10))
                self.screen.blit(level_text, (10, 40))
                
                # Display level complete message
                if level_complete:
                    # Create message box
                    msg_surface = pygame.Surface((self.width - 200, 150))
                    msg_surface.fill(self.WHITE)
                    msg_surface.set_alpha(230)
                    
                    complete_text = self.font.render("Level Complete!", True, self.BLACK)
                    moves_used_text = self.font.render(f"Moves used: {moves}", True, self.BLACK)
                    
                    if current_level < len(self.LEVELS) - 1:
                        next_text = self.font.render("Next level starting in 3 seconds...", True, self.BLACK)
                        msg_surface.blit(complete_text, (50, 30))
                        msg_surface.blit(moves_used_text, (50, 60))
                        msg_surface.blit(next_text, (50, 90))
                        self.screen.blit(msg_surface, (100, self.height // 2 - 75))
                        
                        pygame.display.flip()
                        pygame.time.delay(3000)  # Wait 3 seconds before next level
                        
                        # Move to next level
                        current_level += 1
                        level_transition = True
                        running = False
                    else:
                        # Game complete - show fun fact before ending
                        self.show_puffin_fun_fact()
                        return True
                
                pygame.display.flip()
                self.clock.tick(60)


def main():
    from test_display import TestDisplay
    pygame.init()
    game = PuffinMaze(TestDisplay())
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
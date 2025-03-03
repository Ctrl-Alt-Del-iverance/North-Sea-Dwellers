import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puffin's Journey Home")
clock = pygame.time.Clock()

# Load background image
background_image = pygame.image.load("../images/minigame_backgrounds/puffin_habitat.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load puffin image
puffin_image = pygame.image.load("../images/animals/puffin.png")
# Puffin image will be scaled properly later based on cell size

# Font setup
font = pygame.font.SysFont('Arial', 24)
level_font = pygame.font.SysFont('Arial', 36)

# Level configurations
LEVELS = [
    {"name": "Easy", "grid_width": 10, "grid_height": 8, "color": GREEN},
    {"name": "Medium", "grid_width": 15, "grid_height": 12, "color": YELLOW},
    {"name": "Hard", "grid_width": 20, "grid_height": 15, "color": RED}
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
    
    def draw(self, surface, cell_size, offset_x=0, offset_y=0):
        x, y = offset_x + self.x * cell_size, offset_y + self.y * cell_size
        
        if self.walls['top']:
            pygame.draw.line(surface, BLACK, (x, y), (x + cell_size, y), 6)  # Thicker walls
        if self.walls['right']:
            pygame.draw.line(surface, BLACK, (x + cell_size, y), (x + cell_size, y + cell_size), 6)
        if self.walls['bottom']:
            pygame.draw.line(surface, BLACK, (x, y + cell_size), (x + cell_size, y + cell_size), 6)
        if self.walls['left']:
            pygame.draw.line(surface, BLACK, (x, y), (x, y + cell_size), 6)

def generate_maze(width, height):
    # Create grid of cells
    grid = [[Cell(x, y) for x in range(width)] for y in range(height)]
    
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
            
    def draw(self, surface, cell_size, offset_x=0, offset_y=0):
        # Draw puffin image
        x = offset_x + self.x * cell_size
        y = offset_y + self.y * cell_size
        surface.blit(puffin_image, (x, y))

def draw_family(surface, x, y, cell_size, offset_x=0, offset_y=0):
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

def show_level_transition(surface, level_name, color):
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))
    
    # Display level name
    level_text = level_font.render(f"Level: {level_name}", True, color)
    text_rect = level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    surface.blit(level_text, text_rect)
    
    # Display "Get Ready" message
    ready_text = font.render("Get Ready...", True, WHITE)
    ready_rect = ready_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    surface.blit(ready_text, ready_rect)
    
    pygame.display.flip()
    pygame.time.delay(2000)  # Show for 2 seconds

def main():
    current_level = 0
    total_score = 0
    level_transition = True
    
    while True:  # Main game loop that handles multiple levels
        # Get current level configuration
        level_config = LEVELS[current_level]
        grid_width = level_config["grid_width"]
        grid_height = level_config["grid_height"]
        level_color = level_config["color"]
        
        # Calculate cell size based on maze dimensions to fill the screen
        cell_size = min(WIDTH // grid_width, HEIGHT // grid_height)
        maze_width = cell_size * grid_width
        maze_height = cell_size * grid_height
        maze_x = (WIDTH - maze_width) // 2
        maze_y = (HEIGHT - maze_height) // 2
        
        # Scale puffin image based on cell size
        global puffin_image
        puffin_image = pygame.image.load("../images/animals/puffin.png")
        puffin_image = pygame.transform.scale(puffin_image, (cell_size, cell_size))
        
        # Generate maze for this level
        maze = generate_maze(grid_width, grid_height)
        
        # Set up puffin and family positions
        puffin = Puffin(0, 0)
        family_x, family_y = grid_width - 1, grid_height - 1
        
        moves = 0
        level_complete = False
        
        # Show level transition screen
        if level_transition:
            show_level_transition(screen, level_config["name"], level_color)
            level_transition = False
        
        # Level game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN and not level_complete:
                    if event.key == pygame.K_UP:
                        puffin.move(0, -1, maze)
                        moves += 1
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
                        total_score += 1000 - moves  # Score based on moves
            
            # Draw background image
            screen.blit(background_image, (0, 0))
            
            # Draw maze with offsets
            for row in maze:
                for cell in row:
                    cell.draw(screen, cell_size, maze_x, maze_y)
            
            # Draw family at destination with offsets
            family_center_x = family_x * cell_size + cell_size // 2
            family_center_y = family_y * cell_size + cell_size // 2
            draw_family(screen, family_center_x, family_center_y, cell_size, maze_x, maze_y)
            
            # Draw puffin with offsets
            puffin.draw(screen, cell_size, maze_x, maze_y)
            
            # Draw move counter and level info
            moves_text = font.render(f"Moves: {moves}", True, BLACK)
            level_text = font.render(f"Level: {level_config['name']}", True, BLACK)
            score_text = font.render(f"Score: {total_score}", True, BLACK)
            
            screen.blit(moves_text, (10, 10))
            screen.blit(level_text, (10, 40))
            screen.blit(score_text, (10, 70))
            
            # Display level complete message
            if level_complete:
                # Create message box
                msg_surface = pygame.Surface((WIDTH - 200, 150))
                msg_surface.fill(WHITE)
                msg_surface.set_alpha(230)
                
                level_score = 1000 - moves
                complete_text = font.render(f"Level Complete! Score: {level_score}", True, BLACK)
                
                if current_level < len(LEVELS) - 1:
                    next_text = font.render("Next level starting in 3 seconds...", True, BLACK)
                    msg_surface.blit(complete_text, (50, 50))
                    msg_surface.blit(next_text, (50, 80))
                    screen.blit(msg_surface, (100, HEIGHT // 2 - 75))
                    
                    pygame.display.flip()
                    pygame.time.delay(3000)  # Wait 3 seconds before next level
                    
                    # Move to next level
                    current_level += 1
                    level_transition = True
                    running = False
                else:
                    # Game complete
                    complete_text = font.render(f"Game Complete! Final Score: {total_score}", True, BLACK)
                    restart_text = font.render("Press 'R' to restart or 'Q' to quit", True, BLACK)
                    msg_surface.blit(complete_text, (50, 50))
                    msg_surface.blit(restart_text, (50, 80))
                    screen.blit(msg_surface, (100, HEIGHT // 2 - 75))
                    
                    pygame.display.flip()
                    
                    # Wait for restart or quit
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_r:
                                    # Reset game
                                    current_level = 0
                                    total_score = 0
                                    level_transition = True
                                    waiting = False
                                    running = False
                                elif event.key == pygame.K_q:
                                    pygame.quit()
                                    sys.exit()
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    main()
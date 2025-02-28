import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puffin's Journey Home")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont('Arial', 24)

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
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and not grid[ny][nx].visited:
                neighbors.append((direction, grid[ny][nx]))
        
        return neighbors
    
    def remove_wall(self, other, direction):
        opposite = {'top': 'bottom', 'right': 'left', 'bottom': 'top', 'left': 'right'}
        self.walls[direction] = False
        other.walls[opposite[direction]] = False
    
    def draw(self, surface):
        x, y = self.x * CELL_SIZE, self.y * CELL_SIZE
        
        if self.walls['top']:
            pygame.draw.line(surface, WHITE, (x, y), (x + CELL_SIZE, y), 8)
        if self.walls['right']:
            pygame.draw.line(surface, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 8)
        if self.walls['bottom']:
            pygame.draw.line(surface, WHITE, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 8)
        if self.walls['left']:
            pygame.draw.line(surface, WHITE, (x, y), (x, y + CELL_SIZE), 8)

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
            
    def draw(self, surface):
        # Simple puffin representation
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        
        # Body
        pygame.draw.circle(surface, BLACK, (center_x, center_y), 15)
        
        # White belly
        pygame.draw.circle(surface, WHITE, (center_x, center_y + 5), 10)
        
        # Orange beak
        pygame.draw.polygon(surface, (255, 165, 0), [
            (center_x + 15, center_y),
            (center_x + 25, center_y - 2),
            (center_x + 15, center_y + 5)
        ])
        
        # Eyes
        pygame.draw.circle(surface, WHITE, (center_x + 7, center_y - 5), 4)
        pygame.draw.circle(surface, BLACK, (center_x + 7, center_y - 5), 2)

def draw_family(surface, x, y):
    # Draw a group of puffins
    positions = [(x + 5, y - 5), (x - 10, y + 5), (x + 10, y + 10)]
    
    for px, py in positions:
        # Body
        pygame.draw.circle(surface, BLACK, (px, py), 10)
        
        # White belly
        pygame.draw.circle(surface, WHITE, (px, py + 3), 7)
        
        # Orange beak
        pygame.draw.polygon(surface, (255, 165, 0), [
            (px + 10, py),
            (px + 18, py - 2),
            (px + 10, py + 3)
        ])
        
        # Eyes
        pygame.draw.circle(surface, WHITE, (px + 5, py - 3), 3)
        pygame.draw.circle(surface, BLACK, (px + 5, py - 3), 1)

def main():
    # Generate maze
    maze = generate_maze(GRID_WIDTH, GRID_HEIGHT)
    
    # Set up puffin and family positions
    puffin = Puffin(0, 0)
    family_x, family_y = GRID_WIDTH - 1, GRID_HEIGHT - 1
    
    moves = 0
    game_won = False
    
    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN and not game_won:
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
                    game_won = True
        
        # Draw sky background
        screen.fill(SKY_BLUE)
        
        # Draw ocean background at the bottom
        ocean_rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 100)
        pygame.draw.rect(screen, BLUE, ocean_rect)
        
        # Draw maze
        for row in maze:
            for cell in row:
                cell.draw(screen)
        
        # Draw family at destination
        family_center_x = family_x * CELL_SIZE + CELL_SIZE // 2
        family_center_y = family_y * CELL_SIZE + CELL_SIZE // 2
        draw_family(screen, family_center_x, family_center_y)
        
        # Draw puffin
        puffin.draw(screen)
        
        # Draw move counter
        moves_text = font.render(f"Moves: {moves}", True, BLACK)
        screen.blit(moves_text, (10, 10))
        
        # Display win message
        if game_won:
            win_surface = pygame.Surface((WIDTH - 100, 100))
            win_surface.fill(WHITE)
            win_text = font.render(f"Puffin found its family in {moves} moves!", True, BLACK)
            win_surface.blit(win_text, (50, 40))
            screen.blit(win_surface, (50, HEIGHT // 2 - 50))
            
            restart_text = font.render("Press 'R' to restart or 'Q' to quit", True, BLACK)
            screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 70))
            
            # Check for restart or quit
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                # Reset game
                maze = generate_maze(GRID_WIDTH, GRID_HEIGHT)
                puffin = Puffin(0, 0)
                moves = 0
                game_won = False
            elif keys[pygame.K_q]:
                running = False
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
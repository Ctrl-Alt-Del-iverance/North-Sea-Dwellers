import pygame
import random
import os
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hungry Minke Whale")

# Colors
BLUE = (0, 119, 190)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load ocean floor background
try:
    ocean_floor = pygame.image.load('../images/minigame_backgrounds/ocean_floor.png').convert()
    ocean_floor = pygame.transform.scale(ocean_floor, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Couldn't load ocean floor image: {e}")
    ocean_floor = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    ocean_floor.fill(BLUE)

# Game variables
score = 0
time_left = 60  # 60 seconds
target_score = 20  # Score needed to win
game_over = False
game_won = False

# Font
font = pygame.font.SysFont(None, 36)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Whale class
class Whale(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load whale image
        try:
            self.image = pygame.image.load('../images/animals/whale.png').convert_alpha()
            # Scale image if needed
            self.image = pygame.transform.scale(self.image, (120, 80))
        except pygame.error as e:
            print(f"Couldn't load whale image: {e}")
            # Create a placeholder if image can't be loaded
            self.image = pygame.Surface((120, 80))
            self.image.fill(BLUE)
            
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        
    def update(self):
        pass

# Fish class
class Fish(pygame.sprite.Sprite):
    def __init__(self, fish_type):
        super().__init__()
        self.fish_type = fish_type
        fish_images = {
            'krill': '../images/animals/krill.png',
            'mackerel': '../images/animals/mackerel.png',
            'fish': '../images/animals/fish.png',
            'monkfish': '../images/animals/monkfish.png'
        }
        
        try:
            self.image = pygame.image.load(fish_images.get(fish_type, '../images/animals/fish.png')).convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 25))
        except pygame.error:
            self.image = pygame.Surface((50, 25))
            self.image.fill(RED if fish_type in ['fish', 'monkfish'] else GREEN)

        self.rect = self.image.get_rect()
        
        # Start from random side (left or right)
        if random.choice([True, False]):
            # Start from left side
            self.rect.x = -self.rect.width
            self.speed = random.uniform(1.0, 3.0)  # Move right
        else:
            # Start from right side
            self.rect.x = SCREEN_WIDTH
            self.speed = random.uniform(-3.0, -1.0)  # Move left
        
        # Random vertical position
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 100)
        
    def update(self):
        # Move the fish horizontally
        self.rect.x += self.speed
        
        # Remove if it goes off the screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
fish_sprites = pygame.sprite.Group()

# Create whale
whale = Whale()
all_sprites.add(whale)

# Define which fish are correct for Minke Whale diet
correct_fish = ['krill', 'mackerel']
wrong_fish = [ 'monkfish', 'flounder']
all_fish_types = correct_fish + wrong_fish

# Function to spawn a new fish
def spawn_fish():
    fish_type = random.choice(all_fish_types)
    new_fish = Fish(fish_type)
    all_sprites.add(new_fish)
    fish_sprites.add(new_fish)

# Set up a timer for spawning fish
SPAWN_FISH = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_FISH, 500)  # Spawn a fish every 500ms

# Set up a timer for the game countdown
COUNTDOWN = pygame.USEREVENT + 2
pygame.time.set_timer(COUNTDOWN, 1000)  # Countdown every second

# Weight status indicator
weight_status = "Underweight"
weight_status_color = RED

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == SPAWN_FISH and not game_over and not game_won:
            spawn_fish()
            
        elif event.type == COUNTDOWN and not game_over and not game_won:
            time_left -= 1
            if time_left <= 0:
                game_over = True
                
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and not game_won:
            # Check if a fish was clicked
            pos = pygame.mouse.get_pos()
            for fish in fish_sprites:
                if fish.rect.collidepoint(pos):
                    if fish.fish_type in correct_fish:
                        score += 1
                        if score >= target_score:
                            game_won = True
                    else:
                        # Penalty for wrong fish
                        score -= 1
                        if score < 0:
                            score = 0
                    fish.kill()  # Remove the clicked fish
                    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (game_over or game_won):
                # Reset the game
                score = 0
                time_left = 60
                game_over = False
                game_won = False
                weight_status = "Underweight"
                weight_status_color = RED
                
                # Clear all fish
                for fish in fish_sprites:
                    fish.kill()
    
    # Update all sprites
    all_sprites.update()
    
    # Update weight status based on score
    if score < target_score // 3:
        weight_status = "Severely Underweight"
        weight_status_color = RED
    elif score < target_score // 3 * 2:
        weight_status = "Underweight"
        weight_status_color = (255, 165, 0)  # Orange
    elif score < target_score:
        weight_status = "Almost Healthy"
        weight_status_color = (255, 255, 0)  # Yellow
    else:
        weight_status = "Healthy Weight"
        weight_status_color = GREEN
    
    # Clear the screen with ocean floor background
    screen.blit(ocean_floor, (0, 0))
    
    # Draw all sprites
    all_sprites.draw(screen)
    
    # Display score, time, and target
    score_text = font.render(f"Fish Eaten: {score}/{target_score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    time_text = font.render(f"Time: {time_left}s", True, WHITE)
    screen.blit(time_text, (10, 50))
    
    status_text = font.render(f"Status: {weight_status}", True, weight_status_color)
    screen.blit(status_text, (10, 90))
    
    # Game over or game won screen
    if game_over:
        over_text = font.render("GAME OVER - Whale still hungry!", True, WHITE)
        screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        restart_text = font.render("Press 'R' to Restart", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))
        
    if game_won:
        win_text = font.render("CONGRATULATIONS! Whale is healthy now!", True, GREEN)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        restart_text = font.render("Press 'R' to Restart", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))
    
    # Draw instructions at the bottom
    if not game_over and not game_won:
        inst_text = font.render("Click correct fish: herring, krill, mackerel", True, WHITE)
        screen.blit(inst_text, (SCREEN_WIDTH // 2 - inst_text.get_width() // 2, SCREEN_HEIGHT - 30))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()
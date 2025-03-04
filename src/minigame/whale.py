import pygame
import random
import time
from pygame.locals import *

class Whale(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.weight_status = "Underweight"
        # Load whale image
        try:
            self.image = pygame.image.load('src/images/animals/whale.png').convert_alpha()
            # Scale image if needed
            self.image = pygame.transform.scale(self.image, (213, 184))
        except pygame.error as e:
            print(f"Couldn't load whale image: {e}")
            # Create a placeholder if image can't be loaded
            self.image = pygame.Surface((213, 184))
            self.image.fill((0, 119, 190))
            
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10
        
    def update(self):
        pass

# Fish class
class Fish(pygame.sprite.Sprite):
    def __init__(self, fish_type, width, height):
        super().__init__()
        self.fish_type = fish_type
        self.screen_width = width
        self.screen_height = height
        fish_images = {
            'krill': 'src/images/animals/krill.png',
            'mackerel': 'src/images/animals/mackerel.png',
            'fish': 'src/images/animals/fish.png',
            'monkfish': 'src/images/animals/monkfish.png'
        }
        
        try:
            self.image = pygame.image.load(fish_images.get(fish_type, 'src/images/animals/fish.png')).convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 25))
        except pygame.error:
            self.image = pygame.Surface((50, 25))
            self.image.fill((255, 0, 0) if fish_type in ['fish', 'monkfish'] else (0, 255, 0))

        self.rect = self.image.get_rect()
        
        # Start from random side (left or right)
        if random.choice([True, False]):
            # Start from left side
            self.rect.x = -self.rect.width
            self.speed = random.uniform(1.0, 3.0)  # Move right
        else:
            # Start from right side
            self.rect.x = self.screen_width
            self.speed = random.uniform(-3.0, -1.0)  # Move left
        
        # Random vertical position
        self.rect.y = random.randint(50, self.screen_height - 70)
        
    def update(self):
        # Move the fish horizontally
        self.rect.x += self.speed
        
        # Remove if it goes off the screen
        if self.rect.right < 0 or self.rect.left > self.screen_width:
            self.kill() 

class HungryMinkeWhale:
    def __init__(self, display):
        self.running = True
        self.display = display
        self.score = 0
        self.target_score = 20
        self.start_time = time.time()

        self.all_sprites = pygame.sprite.Group()
        self.fish_sprites = pygame.sprite.Group()
        self.whale = Whale(self.display.width, self.display.height)

        self.correct_fish = ['krill', 'mackerel'] # for minke whale diet
        self.wrong_fish = [ 'monkfish', 'flounder']
        self.all_fish = self.correct_fish + self.wrong_fish
        self.SPAWN_FISH = pygame.USEREVENT + 1

        self.all_sprites.add(self.whale)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == self.SPAWN_FISH:
                self.spawn_fish()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a fish was clicked
                pos = pygame.mouse.get_pos()
                for fish in self.fish_sprites:
                    if fish.rect.collidepoint(pos):
                        if fish.fish_type in self.correct_fish:
                            self.score += 1
                        else:
                            # Penalty for wrong fish
                            self.score -= 1
                            if self.score < 0:
                                self.score = 0
                        fish.kill()  # Remove the clicked fish
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((self.display.width, self.display.height))

    def whale_full(self):
        return self.score >= self.target_score

    def run(self):
        pygame.display.set_caption("Hungry Minke Whale")
        clock = pygame.time.Clock()
        pygame.time.set_timer(self.SPAWN_FISH, 500)  # Spawn a fish every 500ms
        self.all_sprites.add(self.whale)
        success = False
        time_left = 60

        while self.running:
            self.display.screen.blit(self.display.location_bg["Deep Sea"], (0, 0))
            time_left = max(0, 60 - int((time.time() - self.start_time)))
            self.handle_events()
            self.all_sprites.update()
            
            # Update weight status based on score
            if self.score < self.target_score // 3:
                self.whale.weight_status = "Severely Underweight"
                weight_status_color = (255, 0, 0)
            elif self.score < self.target_score // 3 * 2:
                self.whale.weight_status = "Underweight"
                weight_status_color = (225, 115, 0)  # Orange
            elif self.score < self.target_score:
                self.whale.weight_status = "Almost Healthy"
                weight_status_color = (220, 220, 0)  # Yellow
            else:
                self.whale.weight_status = "Healthy Weight"
                weight_status_color = (0, 180, 0)
            
            # Draw all the fish
            self.all_sprites.draw(self.display.screen)
            self.display.draw_text(f"Fish Eaten: {self.score}/{self.target_score}", (10, 10), (0, 0, 150))
            self.display.draw_text(f"Time: {time_left}s", (230, 10), (0, 0, 150))
            self.display.draw_text(f"Status: {self.whale.weight_status}", (367, 10), weight_status_color)
            
            # Game over or game won screen
            if time_left == 0:
                over_text = self.display.font.render("GAME OVER - Whale still hungry!", True, (255, 0, 0))
                self.display.screen.blit(over_text, (self.display.width // 2 - over_text.get_width() // 2, self.display.height // 2 - 50))
                self.running = False  
            elif self.whale_full():
                win_text = self.display.font.render("CONGRATULATIONS! Whale is healthy now!", True, (0, 255, 0))
                self.display.screen.blit(win_text, (self.display.width // 2 - win_text.get_width() // 2, self.display.height // 2 - 50))
                self.running = False
                success = True
            # Draw instructions at the bottom
            else:
                inst_text = self.display.font.render("Click on the correct fish to eat : krill and mackerel", True, (0, 0, 0))
                self.display.screen.blit(inst_text, (self.display.width // 2 - inst_text.get_width() // 2, self.display.height - 40))
            
            # Update the display
            pygame.display.flip()
            # Cap the frame rate
            clock.tick(60)

        pygame.time.delay(2000)
        return success
            
    def spawn_fish(self):
        fish_type = random.choice(self.all_fish)
        new_fish = Fish(fish_type, self.display.width, self.display.height)
        self.all_sprites.add(new_fish)
        self.fish_sprites.add(new_fish)

def main():
    from test_display import TestDisplay
    pygame.init()
    game = HungryMinkeWhale(TestDisplay())
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
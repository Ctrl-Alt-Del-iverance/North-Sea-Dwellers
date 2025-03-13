import pygame
import random
import time
from pygame.locals import *

class Whale(pygame.sprite.Sprite):
    def __init__(self, display):
        super().__init__()

        self.weight_status = "Underweight"
        
        try: # Load whale image
            self.image = display.scale('src/images/animals/whale.png', (213, 184))
        except pygame.error as e:
            print(f"Couldn't load whale image: {e}")
            # Create a placeholder if image can't be loaded
            self.image = pygame.Surface((213, 184))
            self.image.fill((0, 119, 190))
            
        self.rect = self.image.get_rect()
        self.rect.centerx = display.width // 2
        self.rect.bottom = display.height - 10
        
    def update(self):
        pass

# Fish class
class Fish(pygame.sprite.Sprite):
    def __init__(self, fish_type, display):
        super().__init__()
        self.fish_type = fish_type
        fish_images = {
            'krill': 'src/images/animals/krill.png',
            'mackerel': 'src/images/animals/mackerel.png',
            'fish': 'src/images/animals/fish.png', # this is a flounder
            'monkfish': 'src/images/animals/monkfish.png'
        }
        
        try:
            self.image = display.scale(fish_images.get(fish_type, 'src/images/animals/fish.png'), (50, 25))
        except pygame.error:
            self.image = pygame.Surface((50, 25)) # boxes for fish
            self.image.fill((255, 0, 0) if fish_type in ['fish', 'monkfish'] else (0, 255, 0))
        self.rect = self.image.get_rect()
        
        # Start from random side (left or right)
        if random.choice([True, False]): # left
            self.rect.x = -self.rect.width
            self.speed = random.uniform(1.0, 3.0)  # Move right
        else: # right
            self.rect.x = display.width
            self.speed = random.uniform(-3.0, -1.0)  # Move left
        
        # Random vertical position, but not covering the text
        self.rect.y = random.randint(50, display.height - 70)
        
    def update(self): # move the fishy horizontally
        self.rect.x += self.speed
        # Remove if it goes off the screen
        if self.rect.right < 0 or self.rect.left > 1000:
            self.kill() #byebye

class HungryMinkeWhale:
    def __init__(self, display, difficulty):
        self.running = True
        self.state = "playing"
        self.display = display
        self.score = 0
        self.target_score = 20
        self.start_time = time.time()

        self.all_sprites = pygame.sprite.Group()
        self.fish_sprites = pygame.sprite.Group()
        self.whale = Whale(self.display)

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
            
            if self.state == "facts":
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = "input_recieved"

    def whale_full(self):
        return self.score >= self.target_score
    
    def spawn_fish(self):
        fish_type = random.choice(self.all_fish)
        new_fish = Fish(fish_type, self.display)
        self.all_sprites.add(new_fish)
        self.fish_sprites.add(new_fish)

    def run(self):
        pygame.display.set_caption("Hungry Minke Whale")
        clock = pygame.time.Clock()
        pygame.time.set_timer(self.SPAWN_FISH, 500)  # Spawn a fish every 500ms
        self.all_sprites.add(self.whale)
        success = False
        time_left = 60

        while self.running:
            self.handle_events()

            if self.state == "playing":
                self.display.screen.blit(self.display.location_bg["Deep Sea"], (0, 0))
                time_left = max(0, 60 - int((time.time() - self.start_time)))
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
                    self.state = "facts" 
                elif self.whale_full():
                    self.state = "facts"
                    success = True
                # Draw instructions at the bottom
                else:
                    inst_text = self.display.font.render("Click on the correct fish to eat : krill and mackerel", True, (0, 0, 0))
                    self.display.screen.blit(inst_text, (self.display.width // 2 - inst_text.get_width() // 2, self.display.height - 40))
                
                pygame.display.flip() # Update the display
                clock.tick(60) # Cap the frame rate
                if self.state == "facts": # game is over
                    self.show_popup(success)
                    pygame.time.delay(700) # prevent accidental exit

            elif self.state == "input_recieved":       
                pygame.time.delay(700)
                return success # lets the main game know if the player won

        pygame.quit()

    def show_popup(self, success):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.display.width, self.display.height))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        self.display.screen.blit(overlay, (0, 0))
        title_colour = (100, 255, 100) if success else (255, 100, 100)

        # Prepare fun fact text about Minke whales in Aberdeen
        if success:
            title = "Congratulations! Whale is healthy!"
            fact_lines = [
                "Fun Fact: Minke Whales near Aberdeen!",
                "",
                "Minke whales are often spotted in the North Sea which is just off the coast",
                "of Aberdeen. These whales are known for their curiosity and are sometimes",
                "seen by fishermen and sailors. Aberdeen's coastal waters are rich in krill",
                "and small fish, so are a good feeding ground for Minke whales during summer."
            ]
        else:
            title = "Game Over - Whale is still hungry!"
            fact_lines = [
                "Fun Fact: Minke Whales near Aberdeen!",
                "",
                "Minke whales in the North Sea rely on a diet of krill and small fish to",
                "survive. Aberdeen's coastal waters are an important habitat for these",
                "whales, but overfishing and pollution can threaten their food supply.",      
            ]

        whale_image = self.display.scale('src/images/animals/whale.png', (325, 280))
        whale_rect = whale_image.get_rect(center=(self.display.width // 2, self.display.height // 2 - 140))
        self.display.screen.blit(whale_image, whale_rect)
        font = self.display.font

        # Render title
        title_font = pygame.font.SysFont('Arial', 36, bold=True)
        title_text = title_font.render(title, True, title_colour)
        title_rect = title_text.get_rect(center=(self.display.width // 2, self.display.height // 2 - 20))
        self.display.screen.blit(title_text, title_rect)

        # Render fact text
        
        for i, line in enumerate(fact_lines):
            text = font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.display.width // 2, self.display.height // 2 + (i+1) * 30))
            self.display.screen.blit(text, text_rect)

        # Render continue instruction
        continue_text = font.render("Press any key to continue", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(self.display.width // 2, self.display.height - 40))
        self.display.screen.blit(continue_text, continue_rect)

        pygame.display.flip()

def main():
    from test_display import TestDisplay
    pygame.init()
    game = HungryMinkeWhale(TestDisplay())
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
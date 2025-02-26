import pygame
import random

# define all the game displays

class Game:
    def __init__(self, running = True, current_screen="start"):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        self.start_screen = pygame.image.load("images/start_screen.png")
        self.map_screen = pygame.image.load("images/map.png")
        self.running = running
        self.state = current_screen

    def render_screen(self):
        self.screen.fill((0, 0, 0)) # fill to black
        if self.state == "start":
            self.screen.blit(self.start_screen, (0, 0))
        elif self.state == "map":
            self.screen.blit(self.map_screen, (0, 0))
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return "clicked"

class Player:
    def __init__(self, name="player", level=1, exp=0, coins=0):
        self.name = name
        self.level = level
        self.exp = exp
        self.coins = coins
    
    class Catalogue:
        pass

    def get_level(self):
        return self.level
    
    def get_exp(self):
        return self.exp
    
    def get_balance(self):
        return self.coins
    
    def level_up(self):
        self.level +=1
        self.exp = 0

class Animal:
    def __init__(self, name, rarity, base_chance, sprite, exp, shells):
        self.name = name
        self.rarity = rarity
        self.base_chance = base_chance
        self.sprite = sprite
        self.exp = exp
        self.shells = shells

    def does_animal_escape(self, player_level):
        pass

    def get_exp(self):
        # fetches exp to give to player after rescue
        return self.exp
    
    def get_shells(self):
        # fetches shells to give to player after rescue
        pass

def main():
    game = Game()
    player = Player()
    animals = generate_animals()
    
    while game.running:
        user_action = game.handle_events()
        # here we want to add control for the start button
        if game.state == "start" and user_action == "clicked":
            game.state = "map"
        elif game.state == "map" and user_action == "clicked":
            # here we want to transfer to the screem of where the clicked pin is
            pass
        game.draw_screen()

    pygame.quit()

def generate_animals():
    return [
        Animal("harbour seal", 1, 40.0, "harbour_seal_image", 10, 2),
        Animal("harbour seal", 1, 5.0, "grey_seal_image", 25, 5)
    ]


def encounter():
    pass

if __name__ == "__main__":
    main()
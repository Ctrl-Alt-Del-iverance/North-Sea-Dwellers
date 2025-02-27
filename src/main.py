from src.player import Player
import pygame
import random

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

class Animal:
    def __init__(self, name, rarity, base_chance, sprite, exp, shells):
        self.name = name
        self.rarity = rarity
        self.base_chance = base_chance
        self.sprite = sprite
        self.exp = exp
        self.shells = shells

    def animal_escapes(self, player_level):
        base_chances = {1: 0.0, 2: 0.5, 3: 0.70, 4: 0.85, 5: 1.0} # starting chance of animal escaping for each level
        min_chances = {1:0.0, 3:0.10, 4:0.20, 5:0.30} # minimum chance of it escaping

        if self.rarity == 2:
            if player_level >= 10:
                return False # rarity 2 animals will no longer escape
            if player_level >= 5:
                escape_chance = 0.1
            else:
                escape_chance = base_chances[2]

        # the chance should go down by 0.15 every 5 levels
        else:
            escape_chance = max(min_chances[self.rarity], base_chances[self.rarity] - 0.15 * ((player_level-1) // 5))
        # returns true escape_chance% of the time
        return random.random() <= escape_chance

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
    harbour_seal = Animal("harbour seal", 1, 40.0, "harbour_seal_image", 10, 2)
    grey_seal = Animal("grey seal", 4, 5.0, "grey_seal_image", 25, 5)

    return {harbour_seal, grey_seal}


def encounter(animals):
    """ Select animal to spawn. """
    random_chance = random.randint

    pass

if __name__ == "__main__":
    main()
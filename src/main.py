from player import Player
import pygame
import random

class Game:
    def __init__(self, is_running = True, current_screen="start"):
        pygame.init()

        self.screen = pygame.display.set_mode((1000, 500)) # dimentions of the window
        self.running = is_running
        self.state = current_screen
        self.clock = pygame.time.Clock()

        self.title_img = pygame.image.load("images/start_layers/title3.png") # title text for start screen
        self.layers = [] # layers for the start screen
        self.loop_positions = [0] * 7 # positions for the start screen layers

        # load the layers of the start screen
        for i in range(1, 8):
            img = pygame.image.load(f"images/start_layers/pixil-layer-{i}.png")
            self.layers.append(img)  

    def set_display(self):
        """ Render an new screen. """

        self.screen.fill((0, 0, 0)) # fill to black

        if self.state == "start":
            self.render_start_screen()
        else:
            pass

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return "clicked"
            
    def render_start_screen(self):
        """ This will render all layers of the start screen and control the continuous loop. """
        speeds = [6, 6, 6, 6, 4, 2, 1]

        for i in range(len(self.layers)):
            self.loop_positions[i] -= speeds[i]

            if self.loop_positions[i] <= -1000:
                self.loop_positions[i] = 0

            self.screen.blit(self.layers[i], (self.loop_positions[i], 0))
            self.screen.blit(self.layers[i], (self.loop_positions[i] + 1000, 0))

        self.screen.blit(self.title_img, (0, 0))


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
        game.set_display()
        game.clock.tick(30)

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
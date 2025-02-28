import pygame
import random

""" The Game class is an instance of pygame, which controls the state of the game, 
display logic and user interaction logic. """

class Display:
    def __init__(self, is_running = True, current_screen="start"):
        pygame.init()

        self.screen = pygame.display.set_mode((1000, 500)) # dimensions of the window
        self.running = is_running
        self.state = current_screen
        self.clock = pygame.time.Clock()
        self.loop_positions = [0] * 7 # positions for the start screen layers  

        """ Declare the displays here """
        self.layers = self.load_layers() # paralax layers for the start screen
        self.title_img = pygame.image.load("images/start_layers/title3.png") # title text for start screen
        # put map image here
        # put button images here
        # put encounter screen here

    def set_display(self):
        """ Render an new screen. """

        self.screen.fill((0, 0, 0)) # fill to black

        if self.state == "start":
            self.render_start_screen()
        elif self.state =="map":
            # get map display from map class
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

    def load_layers(self):
        layers = []
        for i in range(1, 8):
            img = pygame.image.load(f"images/start_layers/pixil-layer-{i}.png")
            layers.append(img)
        return layers


""" The animal class stores and manages the animal attributes
and their corresponding minigames"""

class Animal:
    def __init__(self, name, rarity, sprite, minigame):
        self.name = name
        self.rarity = rarity
        self.sprite = sprite
        self.minigame = minigame

    def run(self):
        self.minigame()

    def get_game_exp(self):
        exp = {1: 5, 2: 10, 3: 15, 4: 25, 5: 40}
        return exp.get(self.rarity)
    
    def get_reward(self):
        shells = {1: 2, 2: 3, 3: 5, 4: 8, 5: 12}
        return shells.get(self.rarity)

    def escapes(self, player_level):
        base_chances = {3: 0.70, 4: 0.85, 5: 1.0} # starting chance of animal escaping for each level
        min_chances = {3:0.10, 4:0.20, 5:0.30} # minimum chance of it escaping

        if self.rarity == 2:
            if player_level >= 10:
                return False # rarity 2 animals will no longer escape
            if player_level >= 5:
                escape_chance = 0.1
            else:
                escape_chance = 0.5
        # the chance should go down by 0.15 every 5 levels
        # ensure it does not go bellow the minimum chance
        else:
            escape_chance = max(min_chances[self.rarity], base_chances[self.rarity] - 0.15 * ((player_level-1) // 5))
        # returns true escape_chance% of the time
        return random.random() <= escape_chance

    

""" This class will set up all the animals available in the game. """

class AnimalManager:

    def get_animals(self):
        """ Define all the animals for the game. """

        harbour_seal = Animal("harbour seal", 1, self.set_sprite("images/animals/seal.png"))
        grey_seal = Animal("grey seal", 4, self.set_sprite("images/animals/seal.png"))
        minke_whale = Animal("minke whale", 3, self.set_sprite("images/animals/whale.png"))
        bottlenose_dolphin = Animal("bottlenose dolphin", 2, self.set_sprite("images/animals/dolphin.png"))
        puffin = Animal("puffin", 4, self.set_sprite("images/animals/puffin.png"))

        return {harbour_seal, grey_seal, minke_whale, bottlenose_dolphin, puffin}

    def set_sprite(self, filepath):
        return pygame.image.load(filepath)
                                                 
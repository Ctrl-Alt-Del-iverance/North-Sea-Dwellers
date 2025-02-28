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
    def __init__(self, name, rarity, sprite, exp, shells, minigame):
        self.name = name
        self.rarity = rarity
        self.sprite = sprite
        self.exp = exp
        self.shells = shells
        self.minigame = minigame

    def run(self):
        self.minigame()

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

    def get_exp(self):
        # fetches exp to give to player after rescue
        return self.exp
    
    def get_shells(self):
        # fetches shells to give to player after rescue
        return self.shells
    

""" This class will return a list of animals available in the game. """

class GetAnimals:
    def generate_animals():
        #change this to pygame.image.load
        harbour_seal = Animal("harbour seal", 1, "harbour_seal_image", 10, 2)
        grey_seal = Animal("grey seal", 4, "grey_seal_image", 25, 5)

        return {harbour_seal, grey_seal}

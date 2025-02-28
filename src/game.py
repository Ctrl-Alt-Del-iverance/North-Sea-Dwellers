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
        self.loop_positions = [0] * 8 # positions for the start screen layers  

        """ Declare the displays here """
        self.layers = self.load_layers() # paralax layers for the start screen
        self.title_img = pygame.image.load("src/images/start_layers/title7.png") # title text for start screen
        self.title_img = pygame.transform.scale(self.title_img, (750, 375))

        self.continue_button_img = pygame.image.load("src/images/continue_button.png") # title text for start screen
        self.continue_button_img = pygame.transform.scale(self.continue_button_img, (375, 187.5))

        self.new_game_button_img = pygame.image.load("src/images/new_game_button.png") # title text for start screen
        self.new_game_button_img = pygame.transform.scale(self.new_game_button_img, (375, 187.5))

        self.continue_button_rect = pygame.Rect(190, 330, 375, 188)
        self.new_game_button_rect = pygame.Rect(420, 270, 375, 188)

        self.map_rect = pygame.Rect(1000, 50, 800, 400)
        self.transitioning = Transition() #to cahgne holly stuff
        self.transition = False #TO CHANGE HOLLY STUFF
        
        # put map image here
        # put button images here
        # put encounter screen here

    def set_display(self):
        """ Render an new screen. """

        self.screen.fill((0, 0, 0)) # fill to black

        match self.state:
            case "start":
                self.render_start_screen()
            case "map":
                self.render_map_screen()
            case "deep ocean":
              self.screen.fill((50, 80, 20))  

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Clicked")

                if self.state == "start":
                    if self.continue_button_rect.collidepoint(event.pos):
                        print("continue")
                        return "continue"
                    elif self.new_game_button_rect.collidepoint(event.pos):
                        print("New Game")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.transition = True
                if self.state == "map":
                    if self.pin_react.collidepoint(event.pos):
                        print("PIN")
                        return "pin"
                

    def render_start_screen(self):
        """ This will render all layers of the start screen and control the continuous loop. """
        speeds = [6, 6, 6, 6, 4, 2, 1, 6, 6]
        if self.transition:
            y_offset = self.transitioning.get_y_offset()
            #y_offset = 0
            coefficient = self.transitioning.get_x_coefficent(self.map_rect.x)
            #coefficient = 1
            speeds = [speed * coefficient for speed in speeds]
        else:
            y_offset = 0

        #y_offset
        for i in range(len(self.layers)):
            self.loop_positions[i] -= speeds[i]

            if self.loop_positions[i] <= -1000:
                self.loop_positions[i] = 0
            if i != 7:
                self.screen.blit(self.layers[i], (self.loop_positions[i], 0-y_offset))
                self.screen.blit(self.layers[i], (self.loop_positions[i] + 1000, 0-y_offset))
            else: 
                self.screen.blit(self.layers[i], (self.loop_positions[i], 500-y_offset))
                self.screen.blit(self.layers[i], (self.loop_positions[i] + 1000, 500-y_offset))

        self.screen.blit(self.title_img, (125, 20-y_offset))
            # Use the rect positions for button rendering

        self.screen.blit(self.continue_button_img, (self.continue_button_rect.topleft[0],int(self.continue_button_rect.topleft[1])-y_offset))
        self.screen.blit(self.new_game_button_img, (self.new_game_button_rect.topleft[0],int(self.new_game_button_rect.topleft[1])-y_offset))

        # Visualize button hitboxes for debugging
        pygame.draw.rect(self.screen, (255, 0, 0), self.continue_button_rect, 2)
        pygame.draw.rect(self.screen, (0, 255, 0), self.new_game_button_rect, 2)
        #map rect
        if self.transition:
            self.map_rect.x -= speeds[8]
            pygame.draw.rect(self.screen, (0,0,0), self.map_rect)

    def render_map_screen(self):
        self.screen.blit(self.pin, (190, 330))

    def load_layers(self):
        layers = []
        for i in range(1, 9):
            img = pygame.image.load(f"src/images/start_layers/pixil-layer-{i}.png")
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


class Transition:
    def __init__(self, height=500, width=1000):
        self.y_offset = 0
        self.speedy = 0
        self.speedx = 6
        self.height = height
        self.width = width
        self.halfwayy = height / 2
        self.halfwayx = width / 2
        self.finishedy = False
        self.finishedx = False
        self.coefficient = 1

    def get_y_offset(self):
        if self.finishedy:
            return self.y_offset

        if self.y_offset < 250:
            self.speedy += 0.9877
            self.y_offset += self.speedy
        else:
            self.speedy -= 0.9877
            self.y_offset += self.speedy

        if self.y_offset > 500:
            self.finishedy = True

        return self.y_offset
    
    def get_x_coefficent(self, x_location):
        if self.finishedx:
            print("I ran 1")
            return self.coefficient
        print(x_location, self.halfwayx)
        if x_location > 566:
            self.speedx += 1.567
            self.coefficient = self.speedx/6
            print("I ran 2")
        else:
            self.speedx -= 1.493
            self.coefficient = self.speedx/6
            print("I ran 3")
        print("I ran 1")
        if x_location < 108:
            self.finishedx = True
            self.coefficient = 0
        return self.coefficient

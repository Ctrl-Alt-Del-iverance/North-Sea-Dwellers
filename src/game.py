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
        self.layers = self.load_layers() # paralax layers for the start screens
        self.title_img = self.scale("src/images/start_layers/title7.png", (750, 375))
        self.continue_button_img = self.scale("src/images/buttons/continue_button.png", (375, 187.5))
        self.new_game_button_img = self.scale("src/images/buttons/new_game_button.png", (375, 187.5))
        self.pin = self.scale("src/images/map/Pin.png", (375, 187.5))
        self.back_button = self.scale("src/images/buttons/back_button.jpg", (100, 100))
        self.call_button = self.scale("src/images/buttons/back_button.jpg", (100, 100))

        """ Declare hit boxes here. """
        self.continue_button_rect = pygame.Rect(190, 330, 375, 188)
        self.new_game_button_rect = pygame.Rect(420, 270, 375, 188)
        self.back_rect = pygame.Rect(50, 50, 100, 100)
        self.call_rect = pygame.Rect(750, 350, 100, 100)

        self.pin_react = pygame.Rect(190, 330, 375, 188)
        self.map_rect = pygame.Rect(1000, 50, 800, 400)
        self.transitioning = Transition() #to cahgne holly stuff
        self.transition = False #TO CHANGE HOLLY STUFF


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
              self.screen.blit(self.back_button, (50, 50))
              self.screen.blit(self.call_button, (750, 350))

        pygame.display.flip()

    def handle_events(self):
        locations = ["deep ocean", "lighthouse", "seal beach", "puffin cave", "exploring"]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Clicked")
                print(self.state)
                if self.state == "start":
                    if self.continue_button_rect.collidepoint(event.pos):
                        return "continue"
                    elif self.new_game_button_rect.collidepoint(event.pos):
                        print("New Game")
                if self.state == "map":
                    if self.pin_react.collidepoint(event.pos):
                        return "pin"
                if self.state in locations:
                    if self.back_rect.collidepoint(event.pos):
                        return "back"
                    if self.call_rect.collidepoint(event.pos):
                        return "searching"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.transition = True
                       

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
        self.screen.blit(self.pin, (270, 130))
        self.screen.blit(self.pin, (50, 100))
        self.screen.blit(self.pin, (300, 50))

    def render_sprite(self, animal_file):
        self.screen.blit(self.scale(animal_file, (375, 187)), (270, 130))
        pygame.display.flip()

    def load_layers(self):
        layers = []
        for i in range(1, 9):
            img = pygame.image.load(f"src/images/start_layers/pixil-layer-{i}.png")
            layers.append(img)
        return layers
    
    def scale(self, file, scale):
        img = pygame.image.load(file)
        return pygame.transform.scale(img, scale)


""" The animal class stores and manages the animal attributes
and their corresponding minigames"""

class Animal:
    def __init__(self, name, rarity, sprite, minigame=None):
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

    @classmethod
    def get_animals(cls):
        """ Define all the animals for the game. """

        harbour_seal = Animal("harbour seal", 1, "src/images/animals/seal.png")
        grey_seal = Animal("grey seal", 5, "src/images/animals/seal.png")
        minke_whale = Animal("minke whale", 3, "src/images/animals/whale.png")
        bottlenose_dolphin = Animal("bottlenose dolphin", 2, "src/images/animals/dolphin.png")
        puffin = Animal("puffin", 4, "src/images/animals/puffin.png")

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

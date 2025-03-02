import pygame
import random
from animals import Animal, AnimalManager
from player import Player, LevelUpManager

""" The Display class initialises all graphics and controls what is visible on the screen . """

class Display:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 500)) # dimensions of the window
        self.font = pygame.font.SysFont("arial", 25)

        """ Put backgrounds here. """
        self.layers = self.load_layers() # paralax layers for the start screens
        self.title_img = self.scale("src/images/start_layers/title7.png", (750, 375))
        self.map_bg = self.scale("src/images/map/Map.png", (1000, 500))
        #self.locations_bg = {"deep sea": self.scale("filepathtodeapseabg", (1000, 500)),
        #                  "lighthouse": self.scale("filepath", (1000, 500))} #etc...

        """ Buttons """
        self.continue_button_img = self.scale("src/images/buttons/continue_button.png", (375, 187.5))
        self.new_game_button_img = self.scale("src/images/buttons/new_game_button.png", (375, 187.5))
        self.pin = self.scale("src/images/map/Pin.png", (375, 187.5))
        self.back_button = self.scale("src/images/buttons/back_button.jpg", (100, 100))
        self.call_button = self.scale("src/images/buttons/call_button.png", (100, 100))
        self.begin_button = self.scale("src/images/buttons/begin_button.png", (100, 100))

        """ Text """
        self.ran_away_text = self.font.render("Oh no! It ran away.Maybe leveling up will help", True, (200,200,200))
        self.no_animal_text = self.font.render("Looks like nobody is here...", True, (200,200,200))

    def scale(self, file, scale):
        img = pygame.image.load(file)
        return pygame.transform.scale(img, scale)
    
    def load_layers(self):
        layers = []
        for i in range(1, 9):
            img = pygame.image.load(f"src/images/start_layers/pixil-layer-{i}.png")
            layers.append(img)
        return layers

""" The Game class controls game logic and user interaction. """

class Game:
    def __init__(self):
        self.running = True
        self.display = Display()
        self.player = Player()
        self.state = "start"
        self.location = None # we will use this to swap out the different backgrounds
        self.encounter_result = None # what animal spawned if any
        self.cur_animal = None
        self.loop_positions = [0] * 8 # positions for the start screen layers  

        """ Declare hit boxes here. """
        self.continue_button_rect = pygame.Rect(190, 330, 375, 188)
        self.new_game_button_rect = pygame.Rect(420, 270, 375, 188)
        self.back_rect = pygame.Rect(50, 50, 100, 100)
        self.call_rect = pygame.Rect(750, 350, 100, 100)
        self.begin_rect = pygame.Rect(500, 350, 100, 100)
        self.pin_react = pygame.Rect(190, 330, 375, 188)
        self.map_rect = pygame.Rect(1000, 50, 800, 400)

        self.transitioning = Transition() #to cahgne holly stuff
        self.transition = False #TO CHANGE HOLLY STUFF

    def handle_events(self):
        """ Detect user input. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.transition = True

    def handle_click(self, pos):
        """ Handle user input for buttons, and game logic """

        if self.state == "start":
            if self.continue_button_rect.collidepoint(pos):
                self.state = "map"

        # when clicking a pin on the map, go to relevant location:
        elif self.state == "map":
            if self.pin_react.collidepoint(pos):
                self.location = "deep sea"
                self.state = "location"
            #more pins here

        # call for an animal:
        elif self.state == "location":
            if self.call_rect.collidepoint(pos):
                self.encounter() # encounter an animal if there is one

        # if animal is hiding, call again:
        elif self.state == "peeking":
            if self.call_rect.collidepoint(pos): # determine if animal escapes based on player experience
                if self.cur_animal.escapes(self.player.level):
                    self.state = "ran away"
                else: 
                    self.state = "encountered"

        elif self.state == "encountered":
            if self.begin_rect.collidepoint(pos):
                self.state = "minigame"
                    
        # control for the back button:
        if self.state in ["location", "peeking", "encountered", "no animal", "ran away"]:
            if self.back_rect.collidepoint(pos):
                self.state = "map"

    def set_display(self):
        """ Update the display based on the game state. """

        self.display.screen.fill((0, 0, 0)) # erase

        # while you are searching/encountering an animal:
        if self.state in ["location", "encountered", "peeking", "no animal", "ran away"]:
            # change the background from plain green here to 
            # self.display.screen.blit(self.display.location_bg[self.location], (0,0))
            # uncomment locations_bg in Display
            self.display.screen.fill((50, 80, 20))
            self.display.screen.blit(self.display.back_button, (50, 50))
            level = self.display.font.render(f"Player Level: {self.player.level}", True, (0,0,0))
            exp = self.display.font.render(f"Exp: {self.player.exp}", True, (0,0,0))
            self.display.screen.blit(level, (835, 20))
            self.display.screen.blit(exp, (835, 40))
            cur_location = self.display.font.render(f"{self.location}", True, (0, 0,0))
            self.display.screen.blit(cur_location, (450, 20))

        if self.state == "start":
            self.render_start_screen()

        elif self.state == "map":
            self.render_map_screen()
        
        elif self.state == "location":
            self.display.screen.blit(self.display.call_button, (750, 350))

        # let the animal "peak:"
        elif self.state == "peeking":
            self.display.screen.blit(self.display.call_button, (750, 350))
            self.render_sprite(self.encounter_result, 810, 150)

        # display the results of the encounter:
        elif self.state == "encountered":
            self.render_sprite(self.encounter_result, 270, 130)
            self.display.screen.blit(self.display.begin_button, (450, 350))

        elif self.state == "no animal":
            self.display.screen.blit(self.display.no_animal_text, (270, 130))
        
        elif self.state == "ran away":
            self.display.screen.blit(self.display.ran_away_text, (270, 130))

        pygame.display.flip()  # Update screen
                       
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
        for i in range(len(self.display.layers)):
            self.loop_positions[i] -= speeds[i]

            if self.loop_positions[i] <= -1000:
                self.loop_positions[i] = 0
            if i != 7:
                self.display.screen.blit(self.display.layers[i], (self.loop_positions[i], 0-y_offset))
                self.display.screen.blit(self.display.layers[i], (self.loop_positions[i] + 1000, 0-y_offset))
            else: 
                self.display.screen.blit(self.display.layers[i], (self.loop_positions[i], 500-y_offset))
                self.display.screen.blit(self.display.layers[i], (self.loop_positions[i] + 1000, 500-y_offset))

        self.display.screen.blit(self.display.title_img, (125, 20-y_offset))
        # Use the rect positions for button rendering
        self.display.screen.blit(self.display.continue_button_img, (self.continue_button_rect.topleft[0],int(self.continue_button_rect.topleft[1])-y_offset))
        self.display.screen.blit(self.display.new_game_button_img, (self.new_game_button_rect.topleft[0],int(self.new_game_button_rect.topleft[1])-y_offset))

        # Visualize button hitboxes for debugging
        pygame.draw.rect(self.display.screen, (255, 0, 0), self.continue_button_rect, 2)
        pygame.draw.rect(self.display.screen, (0, 255, 0), self.new_game_button_rect, 2)
        #map rect
        if self.transition:
            self.map_rect.x -= speeds[8]
            pygame.draw.rect(self.display.screen, (0,0,0), self.map_rect)

    def render_map_screen(self):
        self.display.screen.blit(self.display.map_bg, (0, 0))
        self.display.screen.blit(self.display.pin, (190, 330))
        self.display.screen.blit(self.display.pin, (270, 130))
        self.display.screen.blit(self.display.pin, (50, 100))
        self.display.screen.blit(self.display.pin, (300, 50))

    def render_sprite(self, file, x, y):
        """ Add an object to the screen. """
        self.display.screen.blit(self.display.scale(file, (375, 187)), (x, y))

    def encounter(self):
        """ Searching for an animal. """

        # chance of each animal at each location
        weights = {"seal beach": [15, 40, 17, 13, 0, 15], 
                "puffin cave": [15, 30, 15, 10, 25, 5],
                "lighthouse": [15, 35, 25, 15, 0, 10],
                "deep sea": [10, 30, 20, 15, 10, 15]}
        # 0 is associated with no animal at all
        rarities = [0, 1, 2, 3, 4, 5]

        # applies the probability of an animal spawning
        selected_rarity = random.choices(rarities, weights[self.location])[0]
        animals = AnimalManager.get_animals()
        candidates = []

        # sees which animals are eligible to spawn, based on selected rarity
        for animal in animals:
            if animal.rarity == selected_rarity:
                candidates.append(animal)

        if candidates: # if there is any animal of that rarity
            spawned_animal = random.choice(candidates)
            print(spawned_animal.name)

            if spawned_animal.rarity == 1: # if the animal is common
                self.state = "encountered" # encounter is done
            else: # animal is rare
                self.state = "peeking" # animal hides
            # display chosen animal
            self.cur_animal = spawned_animal
            self.encounter_result = spawned_animal.sprite
        else: # there is no animal at that location right now
            self.state = "no animal" # encounter is done

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.set_display()
            clock.tick(30)  


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

def main():  
    pygame.init() 
    game = Game()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
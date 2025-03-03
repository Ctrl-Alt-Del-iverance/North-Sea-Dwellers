import pygame
import random
from animals import Animal, AnimalManager
from player import Player, LevelUpManager
from display import Display

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
        self.call_rect = pygame.Rect(750, 300, 100, 100)
        self.begin_rect = pygame.Rect(450, 350, 100, 100)
        self.ocean_pin_rect = pygame.Rect(650, 100, 100, 100)
        self.beach_pin_rect = pygame.Rect(150, 50, 100, 100)
        self.lighthouse_pin_rect = pygame.Rect(260, 210, 100, 100)
        self.cave_pin_rect = pygame.Rect(310, 340, 100, 100)
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
            # stop the player from resizing the window
            # prevent them from seeing uglyness
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((1000, 500))

    def handle_click(self, pos):
        """ Handle user input for buttons, and game logic """

        if self.state == "start":
            if self.continue_button_rect.collidepoint(pos):
                self.state = "map"

        # when clicking a pin on the map, go to relevant location:
        elif self.state == "map":
            if self.ocean_pin_rect.collidepoint(pos):
                self.location = "Deep Sea"
                self.state = "searching"
            if self.lighthouse_pin_rect.collidepoint(pos):
                self.location = "Aberdeen Lighthouse"
                self.state = "searching"
            if self.beach_pin_rect.collidepoint(pos):
                self.location = "Seal Beach"
                self.state = "searching"
            if self.cave_pin_rect.collidepoint(pos):
                self.location = "Puffin Cave"
                self.state = "searching"

        # call for an animal:
        elif self.state == "searching":
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
                try:
                    success = self.cur_animal.run(self.display)
                    self.state = "lost"
                    if success:
                        LevelUpManager.add_exp(self.player, self.cur_animal.get_game_exp())
                        self.state = "won"
                    pygame.display.set_caption("North Sea Dwellers")
                except: # there is no minigame for this animal
                    self.state = "searching" # for testing purposes
                    LevelUpManager.add_exp(self.player, self.cur_animal.get_game_exp())
                    print("couldnt fetch game")
                    
        # control for the back button:
        if self.state not in ["map", "start"]:
            if self.back_rect.collidepoint(pos):
                self.state = "map"

    def set_display(self):
        """ Update the display based on the game state. """

        self.display.screen.fill((0, 0, 0)) # erase

        # while you are searching/encountering an animal:
        if self.state not in ["map", "start"]:
            self.render_location_screen()

        match self.state:
            case "start":
                self.render_start_screen(with_map=False)
            case "map":
                self.transition = True
                self.render_start_screen(with_map=True)
            case "searching":
                self.display.screen.blit(self.display.call_button, (750, 300))
            case "peeking": # animal partially visible
                self.display.draw_object(self.encounter_result, (860, 150))
                self.display.screen.blit(self.display.call_button, (750, 300))
                self.display.draw_text(f"{self.cur_animal.name}", (200, 27))
                self.display.screen.blit(self.display.dialogue_layer, (0, 420))
                self.display.draw_text(f"{self.cur_animal.name} is hiding, lets encourage it to come out!", (50, 450))
            case "encountered": # animal caught!
                self.display.draw_object(self.encounter_result, (400, 130))
                self.display.screen.blit(self.display.begin_button, (450, 370))
                self.display.draw_text(f"{self.cur_animal.name}", (200, 27))
            case "ran away":
                self.display.screen.blit(self.display.dialogue_layer, (0, 420))
                self.display.draw_text("Oh no! It ran away... Maybe leveling up will help", (50, 450))
            case "no animal":
                self.display.screen.blit(self.display.dialogue_layer, (0, 420))
                self.display.draw_text("Looks like nobody is here...", (50, 450), (250, 250, 250))
            case "won":
                self.display.draw_text(f"You Won! Gained {self.cur_animal.get_game_exp()} exp", (450, 270))
            case "lost":
                self.display.draw_text("Too bad. You lost", (450, 270), (250, 250, 250))
            case _:
                raise Exception(f"Invalid game state {self.state}")

        pygame.display.flip()  # Update screend
                       
    def render_start_screen(self, with_map):
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
        print(y_offset)
        print(self.map_rect[0])

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
        x_offset = 1000-self.map_rect[0]
        if with_map:
            self.render_map_screen(x_offset)

    def render_map_screen(self, x_offset):
        self.display.screen.blit(self.display.map_bg, (100+900-x_offset, 50))
        self.display.screen.blit(self.display.pin, (650+900-x_offset, 100)) #deap ocean
        self.display.screen.blit(self.display.pin, (150+900-x_offset, 50)) # seal beach
        self.display.screen.blit(self.display.pin, (260+900-x_offset, 210)) # lighthouse
        self.display.screen.blit(self.display.pin, (310+900-x_offset, 340)) # puffin cave

    def render_location_screen(self):
        self.display.screen.blit(self.display.location_bg[self.location], (0,0))
        self.display.screen.blit(self.display.back_button, (50, 50))
        self.display.draw_text(f"Player Level: {self.player.level}", (822, 5))
        self.display.draw_text(f"Exp: {self.player.exp}", (822, 27))
        self.display.draw_text(f"{self.location}", (200, 5))

    def encounter(self):
        """ Searching for an animal. """

        # chance of each animal at each location
        # in order of none, harbour seal, dolphin, whale, puffin, grey seal
        weights = {"Seal Beach": [10, 43, 20, 10, 0, 17], 
                "Puffin Cave": [10, 25, 20, 10, 30, 5],
                "Aberdeen Lighthouse": [10, 35, 30, 20, 0, 5],
                "Deep Sea": [10, 35, 25, 15, 10, 5]}
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
            clock.tick(60)  


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
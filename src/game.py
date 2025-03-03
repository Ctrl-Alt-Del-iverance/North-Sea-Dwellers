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

    def handle_click(self, pos):
        """ Handle user input for buttons, and game logic """

        if self.state == "start":
            if self.continue_button_rect.collidepoint(pos):
                self.state = "map"

        # when clicking a pin on the map, go to relevant location:
        elif self.state == "map":
            if self.pin_react.collidepoint(pos):
                self.location = "deep sea"
                self.state = "searching"
            #more pins here

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
                self.display.screen.blit(self.display.call_button, (750, 350))
            case "searching":
                self.render_start_screen(with_map=True)
                self.display.screen.blit(self.display.call_button, (750, 350))
            case "peeking": # animal partially visible
                self.display.draw_object(self.encounter_result, (810, 150))
                self.display.screen.blit(self.display.call_button, (750, 350))
                self.display.draw_text(f"{self.cur_animal.name}", (450, 50))
            case "encountered": # animal caught!
                self.display.draw_object(self.encounter_result, (270, 130))
                self.display.screen.blit(self.display.begin_button, (450, 350))
                self.display.draw_text(f"{self.cur_animal.name}", (450, 50))
            case "ran away":
                self.display.draw_text("Oh no! It ran away.Maybe leveling up will help", (270, 130), (250, 250, 250))
            case "no animal":
                self.display.draw_text("Looks like nobody is here...", (270, 130), (250, 250, 250))
            case "won":
                self.display.draw_text(f"You Won! Gained {self.cur_animal.get_game_exp()} exp", (450, 270), (250, 250, 250))
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
        self.display.screen.blit(self.display.pin, (190+900-x_offset, 330))
        self.display.screen.blit(self.display.pin, (270+900-x_offset, 130))
        self.display.screen.blit(self.display.pin, (50+900-x_offset, 100))
        self.display.screen.blit(self.display.pin, (300+900-x_offset, 50))
    
    def render_location_screen(self):
        # change the background from plain green here to 
        # self.display.screen.blit(self.display.location_bg[self.location], (0,0))
        # uncomment locations_bg in Display
        self.display.screen.fill((50, 80, 20))
        self.display.screen.blit(self.display.back_button, (50, 50))
        self.display.draw_text(f"Player Level: {self.player.level}", (835, 20))
        self.display.draw_text(f"Exp: {self.player.exp}", (835, 40))
        self.display.draw_text(f"{self.location}", (450, 20))

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
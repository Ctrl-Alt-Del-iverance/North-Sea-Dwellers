import pygame
import os
""" The Display class initialises all graphics and controls what is visible on the screen . """

class TestDisplay:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 500)) # dimensions of the window
        self.font = pygame.font.Font("src/pixelfont.ttf", 25)
        pygame.display.set_caption("North Sea Dwellers")
        self.width = 1000
        self.height = 500
    
        """ Put backgrounds here. """
        self.layers = self.load_layers() # paralax layers for the start screens
        self.title_img = self.scale("src/images/start_layers/title7.png", (750, 375))
        self.map_bg = self.scale("src/images/map/Map.png", (800, 400))
        self.location_bg = {"Deep Sea": self.scale("src/images/minigame_backgrounds/ocean_floor.png", (1000, 500)),
                          "Aberdeen Lighthouse": self.scale("src/images/map/lighthouse.png", (1000, 500)),
                          "Newburgh Seal Beach": self.scale("src/images/minigame_backgrounds/seal_hab.png", (1000, 500)),
                          "Puffin Cave": self.scale("src/images/map/beachcave.png", (1000, 500))}
        self.dialogue_layer = self.scale("src/images/miscellaneous/dialogue_layer.png", (1000, 95))
        self.frames = self.load_frames()

        """ Buttons """
        self.continue_button_img = self.scale("src/images/buttons/continue_button.png", (375, 187.5))
        self.new_game_button_img = self.scale("src/images/buttons/new_game_button.png", (375, 187.5))
        self.pin = self.scale("src/images/map/Pin.png", (100, 100))
        self.back_button = self.scale("src/images/buttons/back_button.png", (100, 100))
        self.call_button = self.scale("src/images/buttons/call_button.png", (100, 100))
        self.begin_button = self.scale("src/images/buttons/begin_button.png", (100, 100))

    def scale(self, file, scale):
        img = pygame.image.load(file)
        return pygame.transform.scale(img, scale)
    
    def load_layers(self):
        layers = []
        for i in range(1, 9):
            img = pygame.image.load(f"src/images/start_layers/pixil-layer-{i}.png")
            layers.append(img)
        return layers
    
    def draw_text(self, text, pos, colour = (0, 0, 250)):
        message = self.font.render(text, True, colour)
        self.screen.blit(message, pos)

    def draw_object(self, file, pos):
        """ Add an object to the screen. """
        # may need to make scale args
        self.screen.blit(self.scale(file, (220, 220)), pos)

    def load_frames(self, folder="src/dolphin_video/output_folder"):
        frames = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(folder, filename)
                img = pygame.image.load(img_path).convert()
                img = pygame.transform.scale(img, (self.width, self.height))
                frames.append(img)
        return frames
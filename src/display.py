import pygame
""" The Display class initialises all graphics and controls what is visible on the screen . """

class Display:
    def __init__(self):
        self.width = 1000
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height)) # dimensions of the window
        self.font = pygame.font.Font("src/garamond.ttf", 30)
        pygame.display.set_caption("North Sea Dwellers")
        
    
        """ Put backgrounds here. """
        self.layers = self.load_layers() # paralax layers for the start screens
        self.title_img = self.scale("src/images/start_layers/title8.png", (750, 375))
        self.map_bg = self.scale("src/images/map/Map.png", (800, 400))
        self.location_bg = {"Deep Sea": self.scale("src/images/minigame_backgrounds/ocean_floor.png"),
                          "Aberdeen Lighthouse": self.scale("src/images/map/lighthouse.png"),
                          "Newburgh Seal Beach": self.scale("src/images/minigame_backgrounds/seal_hab.png"),
                          "Puffin Cave, Fowlsheugh": self.scale("src/images/map/beachcave.png")}
        self.dialogue_layer = self.scale("src/images/miscellaneous/dialogue_layer.png", (self.width, 95))
        self.caption_layer = self.scale("src/images/miscellaneous/caption_layer.png", (460, 50))

        """ Buttons """
        self.continue_button_img = self.scale("src/images/buttons/continue_button.png", (375, 187.5))
        self.new_game_button_img = self.scale("src/images/buttons/new_game_button.png", (375, 187.5))
        self.pin = self.scale("src/images/map/Pin.png", (100, 100))
        self.back_button = self.scale("src/images/buttons/back_button.png", (90, 90))
        self.call_button = self.scale("src/images/buttons/call_button.png", (220, 68))
        self.begin_button = self.scale("src/images/buttons/begin_button.png", (256, 87))
        self.info_button = self.scale("src/images/buttons/info_button.png", (40, 40))

    def scale(self, file, scale = (1000, 500)):
        img = pygame.image.load(file)
        return pygame.transform.scale(img, scale)
    
    def load_layers(self):
        layers = []
        for i in range(1, 9):
            img = pygame.image.load(f"src/images/start_layers/pixil-layer-{i}.png")
            layers.append(img)
        return layers
    
    def draw_text(self, text, pos, colour = (70, 70, 255)):
        message = self.font.render(text, True, colour)
        self.screen.blit(message, pos)

    def draw_object(self, file, pos):
        """ Add an object to the screen. """
        # may need to make scale args
        self.screen.blit(self.scale(file, (220, 220)), pos)
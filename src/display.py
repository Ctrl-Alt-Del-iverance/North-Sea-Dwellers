import pygame
""" The Display class initialises all graphics and controls what is visible on the screen . """

class Display:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 500)) # dimensions of the window
        self.font = pygame.font.SysFont("arial", 25)
        pygame.display.set_caption("North Sea Dwellers")

        """ Put backgrounds here. """
        self.layers = self.load_layers() # paralax layers for the start screens
        self.title_img = self.scale("src/images/start_layers/title7.png", (750, 375))
        self.map_bg = self.scale("src/images/map/Map.png", (800, 400))
        #self.locations_bg = {"deep sea": self.scale("filepathtodeapseabg", (1000, 500)),
        #                  "lighthouse": self.scale("filepath", (1000, 500))} #etc...

        """ Buttons """
        self.continue_button_img = self.scale("src/images/buttons/continue_button.png", (375, 187.5))
        self.new_game_button_img = self.scale("src/images/buttons/new_game_button.png", (375, 187.5))
        self.pin = self.scale("src/images/map/Pin.png", (375, 187.5))
        self.back_button = self.scale("src/images/buttons/back_button.jpg", (100, 100))
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
    
    def draw_text(self, text, pos, colour = (0, 0, 0)):
        message = self.font.render(text, True, colour)
        self.screen.blit(message, pos)

    def draw_object(self, file, pos):
        """ Add an object to the screen. """
        # may need to make scale args
        self.screen.blit(self.scale(file, (375, 187)), pos)
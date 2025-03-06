import pygame
import os
""" The Display class initialises all graphics and controls what is visible on the screen . """

class Display:
    def __init__(self):
        self.width = 1000
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height)) # dimensions of the window
        self.screen.fill((0, 0, 0))
        self.font = pygame.font.Font("src/pixelfont.ttf", 25)
        pygame.display.set_caption("North Sea Dwellers")
        self.draw_text("Loading...", (450, 230), (255, 255, 255))
        pygame.display.flip()
    
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
        self.instruction_bg = self.scale("src/images/miscellaneous/text_background.jpg", (self.width, self.height))
        self.frames = self.load_frames()

        """ Buttons """
        self.continue_button_img = self.scale("src/images/buttons/continue_button.png", (375, 187.5))
        self.new_game_button_img = self.scale("src/images/buttons/new_game_button.png", (300, 187.5))
        self.pin = self.scale("src/images/map/Pin.png", (100, 100))
        self.back_button = self.scale("src/images/buttons/back_button.png", (104, 81))
        self.call_button = self.scale("src/images/buttons/call_button.png", (220, 68))
        self.begin_button = self.scale("src/images/buttons/begin_button.png", (256, 87))
        self.info_button = self.scale("src/images/buttons/info_button.png", (40, 40))
        self.save_button = self.scale("src/images/buttons/save.png", (90, 40))

        """ Text """

        self.instructions = ["Welcome to North Sea Dwellers! Discover the coastal wildlife of Aberdeen.",
                             "   ",
                             "Use the map to travel through various iconic areas of the Aberdeen",
                             "coastline. Throughout your journey you will encounter various animals",
                             "that are commonly found near here. Animals such as harbour seals and",
                             "dolphins can be frequently sighted, but there are also some rarer,",
                             "endangered species such as puffins and grey seals",
                             "   ",
                             "However, the animals need your help! They are in need of assistance:",
                             "from leading a puffin home, to helping a dolphin with its dance.",
                             "The rarer animals are shy, so they might run away, but as you level up",
                             "your reputation will improve and they will become more friendly and trusting."] 

    def scale(self, file, scale = (1000, 500)):
        img = pygame.image.load(file).convert_alpha()
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

    def draw_object(self, file, pos, scale = (220, 220)):
        """ Add an object to the screen. """
        # may need to make scale args
        self.screen.blit(self.scale(file, scale), pos)

    def load_frames(self, folder="src/dolphin_video/output_folder"):
        frames = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(folder, filename)
                img = pygame.image.load(img_path).convert()
                img = pygame.transform.scale(img, (self.width, self.height))
                frames.append(img)
        return frames
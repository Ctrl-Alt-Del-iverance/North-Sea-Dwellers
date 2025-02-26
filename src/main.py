import pygame
import random

pygame.init()

start_screen = pygame.image.load("images/start_screen.png")
map_screen = pygame.image.load("images/map.png")
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("North Sea Dwellers")
fonr = pygame.font.Font(None, 36)

class Animals:
    def __init__(self, name, rarity, base_chance, sprite, exp, shells):
        self.name = name
        self.rarity = rarity
        self.base_chance = base_chance
        self.sprite = sprite
        self.exp = exp
        self.shells = shells

    def does_animal_escape(self, player_level):
        pass

    def get_exp(self):
        # fetches exp to give to player after rescue
        return self.exp
    
    def get_shells(self):
        # fetches shells to give to player after rescue
        pass

def main():
    pass

def generate_animals():
    pass

if __name__ == "__main__":
    main()
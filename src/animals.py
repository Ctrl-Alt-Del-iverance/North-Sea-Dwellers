import random
import pygame
from minigame.seal_net import SealNetGame
from minigame.whale import HungryMinkeWhale
from minigame.puffin import PuffinMaze
from minigame.dolphin import DolphinGame

""" The animal class stores and manages the animal attributes
and their corresponding minigames"""

class Animal:
    def __init__(self, name, rarity, sprite, minigame=None):
        self.name = name
        self.rarity = rarity
        self.sprite = sprite
        self.minigame = minigame

    def run(self, display, level):
        game = self.minigame(display, level)
        return game.run()

    def get_game_exp(self):
        exp = {1: 8, 2: 15, 3: 25, 4: 35, 5: 50}
        return exp.get(self.rarity)
    
    def get_reward(self):
        shells = {1: 2, 2: 3, 3: 5, 4: 8, 5: 12}
        return shells.get(self.rarity)

    def escapes(self, player_level):
        # based on endangered status
        base_chances = {2: 0.45, 3: 0.60, 4: 0.75, 5: 0.90} # starting chance of animal escaping for each level
        min_chances = {2: 0, 3:0.05, 4:0.15, 5:0.30} # minimum chance of it escaping

        # the chance should go down by 0.10 every 5 levels
        # ensure it does not go bellow the minimum chance
        escape_chance = max(min_chances[self.rarity], base_chances[self.rarity] - 0.10 * ((player_level) // 5))
        # returns true escape_chance% of the time
        return random.random() <= escape_chance

    

""" This class will set up all the animals available in the game. """

class AnimalManager:

    @classmethod
    def get_animals(cls):
        """ Define all the animals for the game. """

        harbour_seal = Animal("Harbour Seal", 1, "src/images/animals/seal.png", SealNetGame)
        grey_seal = Animal("Grey Seal", 5, "src/images/animals/GreySeal.png", SealNetGame)
        minke_whale = Animal("Minke Whale", 3, "src/images/animals/whale.png", HungryMinkeWhale)
        bottlenose_dolphin = Animal("Bottlenose Dolphin", 2, "src/images/animals/dolphin.png", DolphinGame)
        puffin = Animal("Puffin", 4, "src/images/animals/puffin.png", PuffinMaze)
        


        return {harbour_seal, grey_seal, minke_whale, bottlenose_dolphin, puffin}

    def set_sprite(self, filepath):
        return pygame.image.load(filepath)
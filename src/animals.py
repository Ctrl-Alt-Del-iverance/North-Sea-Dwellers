import random
from minigame.seal_net import SealNetGame

""" The animal class stores and manages the animal attributes
and their corresponding minigames"""

class Animal:
    def __init__(self, name, rarity, sprite, minigame=None):
        self.name = name
        self.rarity = rarity
        self.sprite = sprite
        self.minigame = minigame

    def run(self, display):
        game = self.minigame(display)
        return game.run()

    def get_game_exp(self):
        exp = {1: 5, 2: 10, 3: 15, 4: 25, 5: 40}
        return exp.get(self.rarity)
    
    def get_reward(self):
        shells = {1: 2, 2: 3, 3: 5, 4: 8, 5: 12}
        return shells.get(self.rarity)

    def escapes(self, player_level):
        base_chances = {3: 0.65, 4: 0.80, 5: 1.0} # starting chance of animal escaping for each level
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

        harbour_seal = Animal("harbour seal", 1, "src/images/animals/seal.png", SealNetGame)
        grey_seal = Animal("grey seal", 5, "src/images/animals/seal.png", SealNetGame)
        minke_whale = Animal("minke whale", 3, "src/images/animals/whale.png")
        bottlenose_dolphin = Animal("bottlenose dolphin", 2, "src/images/animals/dolphin.png")
        puffin = Animal("puffin", 4, "src/images/animals/puffin.png")

        return {harbour_seal, grey_seal, minke_whale, bottlenose_dolphin, puffin}

    def set_sprite(self, filepath):
        return pygame.image.load(filepath)
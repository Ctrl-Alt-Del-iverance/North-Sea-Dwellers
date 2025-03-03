""" Stores all data unique to a player
May be useful to make this save-able. """

class Player:
    def __init__(self, name="player", level=0, exp=0, shells=0):
        self.name = name # should probably make this a user input
        self.level = level
        self.exp = exp
        self.shells = shells
    
    class Catalogue:
        """ This will record the animals that a player has discovered,
        and the occurences. """
        pass

    def get_level(self):
        return self.level
    
    def get_exp(self):
        return self.exp
    
    def get_balance(self):
        return self.coins
    
    def level_up(self):
        """ Update the player level. """
        self.level +=1
        self.exp = 0

class LevelUpManager:
    base_threshold = 15
    thresh_multiplier = 1.5

    @classmethod
    def get_thresholds(cls, level):
        return int(cls.base_threshold*cls.thresh_multiplier**(level-1))
    
    @classmethod
    def add_exp(cls, player, exp):
        player.exp+=exp
        threshold = cls.get_thresholds(player.level)

        while player.exp >= threshold:
            excess = player.exp-threshold
            player.level_up()
            player.exp = excess
""" Stores all data unique to a player
May be useful to make this save-able. """

class Player:
    def __init__(self, name="player", level=1, exp=0, coins=0):
        self.name = name # should probably make this a user input
        self.level = level
        self.exp = exp
        self.coins = coins
    
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
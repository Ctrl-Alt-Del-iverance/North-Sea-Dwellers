from player import Player
from game import Game, Animal, GetAnimals
import random
import pygame

""" This is the main logic for the game. """

def main():
    game = Game()
    player = Player()
    animals = GetAnimals.generate_animals()
    
    while game.running:
        game.set_display()
        user_action = game.handle_events()
 
        # here we want to add control for the start button
        if game.state == "start" and user_action == "click_continue":
            game.state = "map"
            game.set
        elif game.state == "map" and user_action == "click_pin":
            # here we want to transfer to the screem of where the clicked pin is
            # game.state = "encounter"
            pass
        elif game.state == "encounter":
            encounter(animals, game, player)
            game.state = "map"
        game.clock.tick(30) # 30 frames per second

    pygame.quit()

def encounter(animals, game):
    """ Select animal to spawn. """
    random_chance = random.randint
    # get the animal if there is one
    # click the call button
    # if no animal, return
    # if rare, let it peak (common ones with no chance of running away, skip this stage)
    #   # click again
    #   # if animal.escapes()
    #   #   # return
    # spawn the animal
    # dialogue
    # if minigame()
    #   # player.exp += animal.get_exp()
    #   # check if level up
    #   #   # player.level_up()
    #   # player.shells += animal.get_shells()
    # return

    pass

if __name__ == "__main__":
    main()
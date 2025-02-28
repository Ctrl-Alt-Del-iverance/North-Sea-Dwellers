from player import Player
from game import Display, GetAnimals
import random
import pygame

""" This is the main logic for the game. """

def main():
    game = Display()
    player = Player()
    
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

def encounter(game, player):
    """ Select animal to spawn. """
    
    locations = ["seal beach", "puffin cave", "lighthouse", "deep ocean"]
    weights = [15, 35, 20, 15, 10, 5]
    rarities = [0, 1, 2, 3, 4, 5]

    # applies the probability of an animal spawning
    selected_rarity = random.choices(rarities, weights, 1)[0]
    animals = GetAnimals.generate_animals()
    candidates = []

    # sees which animals are eligible to spawn
    for animal in animals:
        if animal.rarity == selected_rarity:
            candidates.append(animal)
    
    # selects an animal of the rarity
    if candidates:
        spawned_animal = random.choice(candidates)
    else:
        # "there is no animal here"
        return
    
    # press the call button
    if spawned_animal.rarity == 1:
        # make animal appear
        # success = spawned_animal.minigame()
        pass
    
    # otherwise, the animal should "peek"
    # press call button again
    if spawned_animal.escapes(player.level):
        # "oh no it ran away! maybe leveling up will help..."
        return

    # otherwise, make animal appear
    # success = spawned_animal.minigame

    # if success:
    #   # player.exp += spawned_animal.get_exp()
    #   # check if level up
    #   #   # player.level_up()
    #   # player.shells += spawned_animal.get_shells()
    return


if __name__ == "__main__":
    main()
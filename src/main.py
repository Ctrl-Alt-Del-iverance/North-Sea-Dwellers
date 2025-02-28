from player import Player, LevelUpManager
from game import Display, AnimalManager
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
        if game.state == "start" and user_action == "continue":
            game.state = "map"
        elif game.state == "map" and user_action == "pin":
            game.state = "deep ocean"
        #elif game.state == "deep ocean":
            #encounter(game, player, game.state)
            #game.state = "map"
        game.clock.tick(30) # 30 frames per second

    pygame.quit()

def encounter(game, player, location):
    """ Select animal to spawn. """
    success = False
    
    weights = {"seal beach": [15, 40, 17, 13, 15, 0], 
                "puffin cave": [15, 30, 15, 10, 5, 25],
                "lighthouse": [15, 35, 25, 15, 10, 5],
                "deep ocean": [15, 35, 20, 15, 10, 5]}

    rarities = [0, 1, 2, 3, 4, 5]

    # applies the probability of an animal spawning
    selected_rarity = random.choices(rarities, weights[location], 1)[0]
    animals = AnimalManager.gets_animals()
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

    if success:
        # some messages here or something to celebrate
        LevelUpManager.add_exp(player, spawned_animal.get_exp())
        player.shells += spawned_animal.get_shells
    return


if __name__ == "__main__":
    main()
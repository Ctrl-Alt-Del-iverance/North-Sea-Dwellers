from player import Player, LevelUpManager
from game import Display, AnimalManager
import random
import pygame

""" This is the main logic for the game. """

def main():
    game = Display()
    player = Player()
    
    while game.running:
        if game.state != "other":
            game.set_display()
        user_action = game.handle_events()
 
        # here we want to add control for the start button
        if game.state == "start" and user_action == "continue":
            game.state = "map"
        elif game.state == "map" and user_action == "pin":
            game.state = "deep ocean"
        elif game.state == "deep ocean":
            encounter(game, player)
        game.clock.tick(30) # 30 frames per second

    pygame.quit()

def encounter(game, player):
    """ Select animal to spawn. """
    success = False
    
    weights = {"seal beach": [15, 40, 17, 13, 15, 0], 
                "puffin cave": [15, 30, 15, 10, 5, 25],
                "lighthouse": [15, 35, 25, 15, 10, 5],
                "deep ocean": [15, 35, 20, 15, 10, 5]}

    rarities = [0, 1, 2, 3, 4, 5]

    # applies the probability of an animal spawning
    selected_rarity = random.choices(rarities, weights[game.state])[0]
    animals = AnimalManager.get_animals()
    candidates = []

    # sees which animals are eligible to spawn
    for animal in animals:
        if animal.rarity == selected_rarity:
            candidates.append(animal)
    
    # selects an animal of the rarity
    if candidates:
        spawned_animal = random.choice(candidates)
    else:
        print("there is no animal here")
        game.state = "other"
        return
    
    print(spawned_animal.rarity)
    # press the call button

    if spawned_animal.rarity == 1:
        game.render_sprite(spawned_animal.sprite)
        # success = spawned_animal.minigame()
    
    # otherwise, the animal should "peek"
    # press call button again
    else:
        if spawned_animal.escapes(player.level):
            # "oh no it ran away! maybe leveling up will help..."
            print("ran away")
            game.state = "other"
            return
        
        print("spawning")
        game.render_sprite(spawned_animal.sprite)
        # success = spawned_animal.minigame

    if success:
        # some messages here or something to celebrate
        LevelUpManager.add_exp(player, spawned_animal.get_exp())
        player.shells += spawned_animal.get_shells
        game.state = "map"
    else:
        game.state = "other"


if __name__ == "__main__":
    main()
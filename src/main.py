from player import Player, LevelUpManager
from game import Display, AnimalManager
import random
import pygame

""" This is the main logic for the game. """

def main():
    game = Display()
    player = Player()
    prev_user_a = None

    while game.running:
        if game.state == "start":
            game.set_display()
        user_action = game.handle_events()
 
        # here we want to add control for the start button
        if user_action == "continue":
            game.state = "map"
        elif user_action == "pin":
            game.state = "deep ocean"
        # add other pins here
        elif user_action == "back":
            game.state = "map"
        elif user_action == "searching":
            encounter(game, player)

        if prev_user_a is not user_action:
            game.set_display()
        prev_user_a = user_action

        game.clock.tick(30) # 30 frames per second

    pygame.quit()

def encounter(game, player):
    """ Select animal to spawn. """
    success = False
    
    weights = {"seal beach": [15, 40, 17, 13, 0, 15], 
                "puffin cave": [15, 30, 15, 10, 25, 5],
                "lighthouse": [15, 35, 25, 15, 0, 10],
                "deep ocean": [10, 30, 20, 15, 10, 15]}

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
        print(spawned_animal.name)
        # press the call button

        if spawned_animal.rarity == 1:
            game.render_sprite(spawned_animal.sprite)
            # success = spawned_animal.minigame()       
        else: # animal is rare
            # otherwise, the animal should "peek"
            # press call button again
            if spawned_animal.escapes(player.level):
                # "oh no it ran away! maybe leveling up will help..."
                print("ran away")     
            else:
                print("spawning")
                game.render_sprite(spawned_animal.sprite)
                # success = spawned_animal.minigame
    else:
        print("there is no animal here")

    if success:
        # some messages here or something to celebrate
        LevelUpManager.add_exp(player, spawned_animal.get_exp())
        player.shells += spawned_animal.get_shells
        game.state = "map"
    game.state = "exploring"


if __name__ == "__main__":
    main()
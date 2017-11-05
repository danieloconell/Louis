"""Welcome to the falling environemt.

In which the aim is to catch falling objects.

"""

from random import randint
import pygame

# global variables for environemt
actions = ["left", "right", "stay"]
block = 25
screen_width = 28
screen_height = 14
n_actions = 2
observation = [0, 0, False]
interval = 1


def make(env):
    """Chose whether the environment is text or in pygame."""
    global type, display
    if env == "pygame":
        pygame.init()
        width = block * (screen_width + 2)
        height = block * (screen_height + 2)
        display = pygame.display.set_mode([width, height])
        display.fill((96, 96, 96))
        type = "pygame"
    elif env == "text":
        type = "text"
    else:
        print("Invalid environment type")


def reset():
    """Reset all the necessary variables for the environment."""
    global screen, screen_height, screen_width, object, player, actual_reward, done

    print("Resetting")

    # create the screen which is an empty array of spaces
    screen = [[" "] * screen_width for x in range(screen_height)]

    # create object
    object = []
    object.extend([randint(0, screen_width - 1), 0])

    # create player
    player = (screen_width / 2)

    # reset done and reward
    done = False
    actual_reward = 0


def action(action):
    """Action 0 move player left 1 move player right."""
    global old_player, player

    # if player is at one of the screen borders do not move
    if player == screen_width - 1:
        player = player
    elif action == "left":
        old_player = player
        player -= interval
    elif action == "right":
        old_player = player
        player += interval
    elif action == "stay":
        old_player = player - 1
        player = player
    else:
        print("Invalid action")


def update():
    """Make the object fall and update the player location."""
    global old_object, object, done, observation, actual_reward, reward
    old_object = []
    old_object.extend([object[0], object[1]])
    if object[1] == screen_height - 2:
        done = True
    else:
        object[1] += 1

    # make observation
    observation = []
    observation.extend([[object, player], actual_reward, done])

    # draw player and remove old player
    screen[screen_height - 1][int(player)] = "@"
    screen[screen_height - 1][int(old_player)] = " "

    # draw object and remove old object
    screen[object[1]][object[0]] = "0"
    screen[old_object[1]][old_object[0]] = " "


def render():
    """Render everything that needs to be drawn."""
    global object, old_object, old_player, player, screen, screen_height
    global screen_width, observation, done, type, display

    # update
    update()

    index = 0
    index_2 = 0

    if type == "text":
        print("#" * (screen_width + 2))
        for row in screen:
            for item in row:
                if index == screen_width:
                    print("#")
                    index = 0
                if index == 0:
                    print("#", end="")
                index += 1
                print(item, end="")
        print("#", end="\n")
        print("#" * (screen_width + 2))
    elif type == "pygame":
        for row in screen:
            index_2 += 1
            for item in row:
                if index == screen_width:
                    index = 0
                elif index == 0:
                    None
                index += 1
                if item == " ":
                    pygame.draw.rect(display, (236, 236, 236), (block * index, block * index_2, block, block))
                elif item == "0":
                    pygame.draw.rect(display, (96, 148, 188), (block * index, block * index_2, block, block))
                elif item == "@":
                    pygame.draw.rect(display, (229, 0, 27), (block * index, block * index_2, block, block))
        pygame.display.update()


def create_reward(action):
    """Return the reward based on an action."""
    global player, object, actual_reward

    reward = 0

    if player == object[0] and action == "stay":
        reward += 1
        return reward
    elif player == object[0] and action == "left":
        return reward
    elif player == object[0] and action == "right":
        return reward

    # if player move in direction of object, increase reward
    if action == "left":
        action = 0
        other_action = 1
        action_1_difference = object[0] - player + action
        action_2_difference = object[0] - player + other_action
    elif action == "right":
        action = 1
        other_action = 0
        action_1_difference = object[0] - player + action
        action_2_difference = object[0] - player + other_action
    elif action == "stay":
            reward = 0
            return reward

    # if player is at the location of the object
    if object[0] > player:
        if action_1_difference < action_2_difference:
            reward += 0
            return reward
        else:
            reward += 1
            return reward
    elif object[0] < player:
        if action_1_difference < action_2_difference:
            reward += 1
            return reward
        else:
            reward += 0
            return reward


def sample_action():
    """Make a random action based on the possible actions."""
    global n_actions

    # random action
    decision = randint(0, (n_actions - 1))
    action(decision)

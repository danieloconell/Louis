"""Welcome to the falling environemt.

In which the aim is to catch falling objects.

"""

from random import randint

# global variables for environemt
screen_width = 38
screen_height = 14
n_actions = 2
observation = []


def reset():
    """Reset all the necessary variables for the environment."""
    global screen, screen_height, screen_width, object, player, reward, done

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
    reward = 0


def action(action):
    """Action 0 move player left 1 move player right."""
    global old_player, player

    # if player is at one of the screen borders do not move
    if player == screen_width - 1:
        player = player
    elif action == 0:
        old_player = player
        player -= 1
    elif action == 1:
        old_player = player
        player += 1
    else:
        print("Invalid action")


def render():
    """Render everything that needs to be drawn."""
    global object, old_object, old_player, player, screen, screen_height
    global screen_width, observation, done, reward

    # gravity, make the object fall down one square at a time
    old_object = []
    old_object.extend([object[0], object[1]])
    if object[1] == screen_height - 1:
        print("Episode over")
        reset()
        done = True
    else:
        object[1] += 1

    # make observation
    observation = []
    observation.extend([[object, player], reward, done])

    # draw player and remove old player
    screen[screen_height - 1][int(player)] = "@"
    screen[screen_height - 1][int(old_player)] = " "

    # draw object and remove old object
    screen[object[1]][object[0]] = "0"
    screen[old_object[1]][old_object[0]] = " "

    # draw what is in the screen array
    index_1 = 0
    index_2 = 0

    print("#" * (screen_width + 2))
    for row in screen:
        index_1 += 1
        for item in row:
            if index_2 == 38:
                print("#")
                index_2 = 0
            if index_2 == 0:
                print("#", end="")
            index_2 += 1
            print(item, end="")
    print("#", end="\n")
    print("#" * (screen_width + 2))


def sample_action():
    """Make a random action based on the possible actions."""
    global n_actions

    # random action
    decision = randint(0, (n_actions - 1))
    action(decision)

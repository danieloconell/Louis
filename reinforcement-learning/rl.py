"""Basic reinforcement learning functions.
"""

from env import reward
import numpy as np
import env

actions = ["left", "right", "stay"]
gamma = 0.8 # make the agent explore a bit
table = np.zeros((28, 28, 3))


def all_zero(list):
    """Return true if all item in an array are 0."""
    for item in list:
            for x in item:
                if x != 0:
                    return False
    return True


def choose_action(state):
    """Choose action based on q table."""
    if np.random.uniform() > gamma or all_zero(state):
    #if all_zero(state):
        action = np.random.choice(actions)
        print("zero")
        return action
    else:
        action = np.argmax(state)
        action += 1
        index_1 = int(round(action / 3))
        index_2 = int(action - index_1 * 3)
        index_1 -= 1
        if index_1 == 0:
            action = "left"
        elif index_1 == 1:
            action = "right"
        else:
            action = "stay"
        return action

def q(state, action):
    """Update the q table."""
    print("[+] INFO object:", env.object[0], "player:", env.player)
    index = -1
    for item in actions:
        index += 1
        if item == action:
            action_n = index

    # q learning
    new_value = reward(action) + gamma * np.amax(table[env.object[0]])

    print(new_value, state, action)
    print(table[env.object[0]][int(state)])
    table[env.object[0]][int(state)][action_n] = new_value

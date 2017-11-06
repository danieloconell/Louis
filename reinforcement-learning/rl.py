"""Basic reinforcement learning functions.
"""

from env import reward
import pandas as pd
import numpy as np
import env

actions = ["left", "right", "stay"]
gamma = 0.8
table = np.zeros((14, 3, 28))


def all_zero(list):
    for item in list:
        if item != 0:
            return False
    return True


def choose_action(state):
    """Choose action based on q table."""
    if np.random.uniform() > gamma or all_zero(state):
        action = np.random.choice(actions)
        print("zero")
        print(action)
        return action
    else:
        action = max(state)
        print(action)
        return action

def q(state, action):
    """Update the q table."""
    index = -1
    for item in actions:
        index += 1
        if item == action:
            action_n = index

    # q learning
    new_value = reward(action) + gamma * max(table[action_n][env.object[0]][(state - 1)], table[action_n][env.object[0]][(state)], table[action_n][env.object[0]][(state + 1)])
    table[env.player][env.object[0]][state] = new_value
    print(new_value)
    np.save("q-table", table)

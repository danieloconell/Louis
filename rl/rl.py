"""Reinforcement learning functions.

These functions are used by the agent to solve the Falling environment.
"""

import numpy as np
import sys

from env import Falling
env = Falling()
env.reset()

np.random.seed(0)   # to make results reproducible
gamma = 0.8         # make the agent explore a bit


def choose_action(agent: int, square: list, train=False) -> str:
    """Choose action based on q table.
        Args:
            square: Of the square's location.
            train: Enable random actions to explore environment.
        Returns:
            The action with the highest q value.  If they are all the same it
            returns a random action
        """
    if np.random.uniform() > gamma and not train:
        action = np.random.choice(env.ACTIONS)
        return action
    else:
        # if all rewards are the same choose a random action
        if len(set(table[square[0] - 1][agent - 1])) == 1:
            action = np.random.choice(env.ACTIONS)
            return action

        else:
            action_index = np.argmax(table[square[0] - 1][agent - 1])
            action = env.ACTIONS[action_index]
            return action


def update_q(state: int, action: str, reward: int, square: list):
    """Update the q table.
    Args:
        state: The agent's current state in environment.
        action: The agent's action.
        reward: Reward for chosen action.
        square: The square's location in the environment.
    """
    # chosen action as a number
    action_n = env.ACTIONS.index(action)

    # max future reward based on action
    if action == "left":
        new_agent_pos = state - 1
    elif action == "right":
        new_agent_pos = state + 1
    elif action == "stay":
        new_agent_pos = state
    else:
        print("Invalid action")

    # calculate q reward for action
    new_value = reward + gamma * \
        np.max(table[square[0] - 1][new_agent_pos - 1])

    # update q table
    table[square[0] - 1][state - 1][action_n] = new_value


def save_q():
    """Locally save the q table."""
    np.save("q-table", table)


def load_q(new=False):
    """Load q table if one exists.
    Args:
        new: Should a new q table should be created.
    """
    global table
    file = "q-table.npy"
    if new:
        table = np.zeros((23, 23, 3))
    else:
        try:
            table = np.load(file)
        except FileNotFoundError:
            print("q-table.npy does not exist, have you trained it?")
            sys.exit(3)

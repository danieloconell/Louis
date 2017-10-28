"""This is the agen which currently takes random actions."""

import env

env.reset()
for _ in range(10000):
    env.sample_action()
    env.render()

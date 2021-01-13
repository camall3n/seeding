import pytest

from seeding import seeding


def test_seed_python():
    import random

    seeding.seed(0, random)
    a = random.random()
    seeding.seed(0, random)
    b = random.random()
    assert a == b


def test_seed_numpy():
    import numpy as np

    seeding.seed(0, np)
    a = np.random.random()
    seeding.seed(0, np)
    b = np.random.random()
    assert a == b


def test_seed_torch():
    import torch

    seeding.seed(0, torch)
    a = torch.rand(1).detach().item()
    seeding.seed(0, torch)
    b = torch.rand(1).detach().item()
    assert a == b


def test_seed_unknown():
    import os

    seeding.seed(0, os)  # Succeeds with warning


def test_seed_gym():
    import gym

    env_name = "CartPole-v0"
    env = gym.make(env_name)
    other_env = gym.make(env_name)
    seeding.seed(0, gym, env, other_env)

    env.reset()
    for _ in range(10):
        obs1, reward1, done1, info1 = env.step(env.action_space.sample())

    other_env.reset()
    for _ in range(10):
        obs2, reward2, done2, info2 = other_env.step(other_env.action_space.sample())

    assert (obs1 == obs2).all()
    assert reward1 == reward2
    assert done1 == done2
    assert info1 == info2


def test_seed_hash():
    with pytest.raises(RuntimeError):
        seeding.seed(0, hash)

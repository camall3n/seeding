import logging
from types import ModuleType

def seed(seed, *args, **kwargs):
    """
    Set random seed for the default RNGs in each of the subsequent positional args

    Optional kwargs:
        deterministic (bool): whether to ensure deterministic results on subsequent runs
            default = True

    Usage:
    >>> import random
    >>> import gym
    >>> import numpy as np
    >>> import torch
    >>> env = gym.make('Cartpole-v0')
    >>> other_env = gym.make('Cartpole-v0')
    >>> seed(0, random, gym, np, torch, env, other_env)
    """

    deterministic = ('deterministic' not in kwargs.items() or kwargs['deterministic'] == True)

    modules = []
    non_modules = []
    for arg in args:
        if isinstance(arg, ModuleType):
            modules.append(arg)
        else:
            non_modules.append(arg)

    for module in modules:
        module_name = module.__name__
        if module_name is 'random':
            module.seed(seed)
        elif module_name is 'numpy':
            # See https://numpy.org/doc/stable/reference/random/generated/numpy.random.seed.html?highlight=seed#numpy.random.seed
            # and also https://stackoverflow.com/questions/22994423/difference-between-np-random-seed-and-np-random-randomstate
            module.random.seed(seed)
        elif module_name is 'torch':
            # See https://pytorch.org/docs/stable/notes/randomness.html
            module.manual_seed(seed)
            if deterministic:
                module.backends.cudnn.benchmark = False
                module.set_deterministic(True)
        elif module_name is 'tensorflow':
            # See https://www.tensorflow.org/api_docs/python/tf/random/set_seed
            module.random.set_seed(seed)
        elif module_name is 'gym':
            # See the following:
            # - https://github.com/openai/gym/blob/master/gym/core.py
            # - https://github.com/openai/gym/issues/428
            # - https://harald.co/2019/07/30/reproducibility-issues-using-openai-gym/
            envs = [object_ for object_ in non_modules if isinstance(object_, module.core.Env)]
            non_modules = [object_ for object_ in non_modules if object_ not in envs]
            for env in envs:
                env.seed(seed)
                if deterministic:
                    env.action_space.seed(seed)
        else:
            logging.warning('Skipping random seeding of unknown module: {}'.format(module_name))

    for object_ in non_modules:
        if object_ is hash:
            # See https://stackoverflow.com/questions/30585108/disable-hash-randomization-from-within-python-program
            logging.error(
                'Cannot set PYTHONHASHSEED to "0" once python is running.\n'
                'Try running python with the environment variable PYTHONHASHSEED=0\n'
                'or using a different hashing function if determinism is required.'
            )
            raise RuntimeError
        else:
            logging.warning('Skipping random seeding of unknown object: {}'.format(object_))

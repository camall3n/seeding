# seeding
Lightweight python library for achieving deterministic random seeds

# Installation

Currently requires Python 3

```
pip install seeding
```

# Usage


## Basics
Seeding's core usage pattern is to call `seeding.seed`, supplying both a random seed and any modules for which you want to set the random seed.

```python
import random
import seeding

seeding.seed(0, random)
random.random()
# 0.8444218515250481
seeding.seed(0, random)
random.random()
# 0.8444218515250481
```

Seeding is compatible with `import X as Y` syntax and can seed multiple modules at the same time.

```python
import numpy as np
import random
import torch

import seeding

seeding.seed(0, random, np, torch)
```

## Other arguments

The `seeding.seed` function also takes in an optional keyword argument `deterministic`. By default, this argument is set to True, but it can be overridden if determinism is not required, which can potentially result in improved performance in some libraries (e.g. PyTorch).

```python
import seeding
import torch

seeding.seed(0, torch, deterministic=False)
```

## Seeding additional objects
For some libraries, like [OpenAI Gym](https://github.com/openai/gym/), seeding happens at an object level instead of a global level. To seed gym environments, pass both the gym module and any environments you want to seed.

```python
import gym
import seeding

env_name = "CartPole-v0"
env = gym.make(env_name)
other_env = gym.make(env_name)

seeding.seed(0, gym, env, other_env)
```

Note: the default behavior also seeds the env.action_space; to disable this behavior, use `deterministic=False` as described above.
import numpy as np

class RandomRuleGenerator:
    """
    An iterable to just generate a random int from 0 - 11 indicating
    which feature should be the next rule
    """
    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)

    def __iter__(self):
        return self

    def __next__(self): 
        """
        randomly generates integer from 0 - 11
        """
        return self.rng.integers(0, 12, 1)[0]
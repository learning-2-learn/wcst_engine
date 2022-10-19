import numpy as np

class RandomRuleGenerator:
    def __init__(self, seed=42):
        self.rng = np.random.default_rng(seed)

    def __iter__(self):
        return self

    def __next__(self): 
        """
        randomly generates np array of 4 x 3, each element being 0, 1, 2, or 3
        """
        return rng.integers(0, 12, 1)[0]
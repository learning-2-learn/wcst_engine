import numpy as np

class RandomCardGenerator:
    def __init__(self, seed=42):
        self.rng = np.random.default_rng(seed)

    def __iter__(self):
        return self

    def __next__(self): 
        """
        randomly generates np array of 4 x 3, each element being 0, 1, 2, or 3
        """
        colors = np.arange(0, 4).reshape(4, 1)
        self.rng.shuffle(colors)
        shapes = np.arange(4, 8).reshape(4, 1)
        self.rng.shuffle(shapes)
        patterns = np.arange(8, 12).reshape(4, 1)
        self.rng.shuffle(patterns)
        return np.hstack((colors, shapes, patterns))
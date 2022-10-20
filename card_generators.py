import numpy as np

class RandomCardGenerator:
    """
    An iterable to generate the next set of cards randomly
    """
    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)

    def __iter__(self):
        return self

    def __next__(self): 
        """
        randomly generates np array of 4 x 3, each element being an int from 0 - 11 
        indicating the feature idx. 
        """
        shapes = np.arange(0, 4).reshape(4, 1)
        self.rng.shuffle(shapes)
        colors = np.arange(4, 8).reshape(4, 1)
        self.rng.shuffle(colors)
        patterns = np.arange(8, 12).reshape(4, 1)
        self.rng.shuffle(patterns)
        return np.hstack((shapes, colors, patterns))
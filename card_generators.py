import numpy as np

class RandomCardGenerator:
    """
    An iterable to generate the next set of cards randomly
    """
    def __init__(self, seed, num_cards=4, num_dims=3):
        self.rng = np.random.default_rng(seed)
        self.num_cards = num_cards
        self.num_dims = num_dims

    def __iter__(self):
        return self

    def __next__(self): 
        """
        randomly generates np array of num_cards x num_dims, each element being an int from 0 - num_features
        indicating the feature idx. 
        """
        dim_cols = []
        for dim_idx in range(self.num_dims):
            dim_vals = np.arange(
                dim_idx * self.num_cards, 
                (dim_idx + 1) * self.num_cards
            ).reshape(self.num_cards, 1)
            self.rng.shuffle(dim_vals)
            dim_cols.append(dim_vals)
        return np.hstack(dim_cols)
    
# class RandomCardGeneratorOmitDim:
#     """
#     Randomly generates cards, but zeros out one feature dimension
#     """
#     def __init__(self, seed, num_cards=4, num_dims=3, omit_dim_idx=2):
#         self.rng = np.random.default_rng(seed)
#         self.num_cards = num_cards
#         self.num_dims = num_dims
#         self.omit_dim_idx = omit_dim_idx

#     def __iter__(self):
#         return self

#     def __next__(self): 
#         """
#         randomly generates np array of num_cards x num_dims, each element being an int from 0 - num_features
#         indicating the feature idx. 
#         """
#         dim_cols = []
#         for dim_idx in range(self.num_dims):
#             dim_vals = np.arange(
#                 dim_idx * self.num_cards, 
#                 (dim_idx + 1) * self.num_cards
#             ).reshape(self.num_cards, 1)
#             self.rng.shuffle(dim_vals)
#             dim_cols.append(dim_vals)
#         return np.hstack(dim_cols)

class RandomCardGeneratorNoDims:
    """
    Still gives back n cards with n features each, but 
    can be any features (no dimensional divide)
    """
    def __init__(self, seed, num_cards=4, num_dims=3):
        self.rng = np.random.default_rng(seed)
        self.num_cards = num_cards
        self.num_dims = num_dims

    def __iter__(self):
        return self

    def __next__(self): 
        """
        randomly generates np array of num_cards x num_dims, each element being an int from 0 - num_features
        indicating the feature idx. 
        """
        feats = np.arange(self.num_cards * self.num_dims)
        self.rng.shuffle(feats)
        cards = np.split(feats, self.num_cards)
        return np.vstack(cards)
    

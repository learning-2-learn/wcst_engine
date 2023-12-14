import gymnasium as gym
from gymnasium import spaces
from .wcst_session_gym import WcstSessionGym
import numpy as np


class NHotObservation(gym.ObservationWrapper, gym.utils.RecordConstructorArgs):
    """Wrapper for transforming WCST observations to n_hot representations per card
    """

    def __init__(self, wcst_env: WcstSessionGym):
        """Flattens the observations of an environment.

        Args:
            env: The environment to apply the wrapper
        """
        gym.utils.RecordConstructorArgs.__init__(self)
        self.num_cards = wcst_env.unwrapped.num_cards
        self.num_features = wcst_env.unwrapped.num_features
        gym.ObservationWrapper.__init__(self, wcst_env)
        self.observation_space = spaces.MultiBinary([self.num_cards, self.num_features])

    def observation(self, observation):
        """Converts a cards observation to a N-hot encoding of cards, 

        Args:
            observation: the cards observation, of [num_cards, num_dimensions], each element as 
            an index to a feature. 

        Returns:
            An num_dimensions-hot encoding of cards
        """
        n_hot = np.zeros((self.num_cards, self.num_features))
        for card_idx in range(self.num_cards):
            feature_idxs = observation[card_idx, :]
            n_hot[card_idx, feature_idxs] = 1
        return n_hot

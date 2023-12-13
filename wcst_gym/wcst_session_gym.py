import numpy as np
import gymnasium as gym
from gymnasium import spaces


class WcstSessionGym(gym.Env):
    # metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, wcst_session):
        self.session = wcst_session
        self.num_cards = wcst_session.card_generator.num_cards
        self.num_dims = wcst_session.card_generator.num_dims
        self.num_features = wcst_session.rule_generator.num_rules
        card_shapes = np.ones((self.num_cards, self.num_dims)) * self.num_features
        self.observation_space = spaces.MultiDiscrete(card_shapes)
        self.action_space = spaces.Discrete(self.num_cards)

    def _get_obs(self):
        return self.session.get_cards()

    def _get_info(self):
        """
        TODO: maybe add other stats in here as well? Which block, which how many trials in etc. 
        """
        return {"current_rule": self.session.current_rule}

    def reset(self, seed=None, options=None):
        self.session.start_new_session()
        return self._get_obs(), self._get_info()

    def step(self, action):
        _, reward = self.session.make_selection(action)
        obs = self._get_obs()
        info = self._get_info()
        # should return: observation, reward, terminated, truncated, info, done
        return obs, reward, False, False, info


    
    

import numpy as np

from block_switching_conditions import monkey_condition
from card_generators import RandomCardGenerator
from rule_generators import RandomRuleGenerator

class WcstSession:
    def __init__(
        reward_value,
        penalty_value, 
        card_generator=RandomCardGenerator,
        rule_generator=RandomRuleGenerator,
        block_switching_condition=monkey_condition,
        random_seed = 42,
        termination_length=None,
    ):
        self.reward_value = reward_value
        self.penalty_value = penalty_value
        self.block_switching_condition = block_switching_condition
        self.termination_length = termination_length
        self.card_generator = card_generator
        self.rng = random_seed
        self.start_session()
    
    def start_session():
        self.card_iterator = iter(self.card_generator)
        self.history = []
        self.current_rule = rng.random
        self.current_trial = 0
        self.current_cards = None
        self.current_selection = None


    def get_cards():
        self.current_trial += 1
        self.current_cards = next(self.card_generator)
        return self.current_cards

    def make_selection(selection):
        """
        returns tuple (outcome, reward)
        """
        self.current_selection = selection
        card = self.current_cards[selection]


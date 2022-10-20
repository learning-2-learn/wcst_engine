import numpy as np
import pandas as pd

from block_switching_conditions import monkey_condition
from card_generators import RandomCardGenerator
from rule_generators import RandomRuleGenerator
from constants import FEATURE_NAMES, DIM_NAMES


class WcstSession:
    """
    A configurable session for the WCST
    """
    def __init__(
        self,
        correct_value,
        incorrect_value, 
        card_generator=None,
        rule_generator=None,
        block_switching_condition=monkey_condition,
        random_seed=None,
    ):
        """
        Args:
            correct_value: how much reward given for correct trials
            incorrect_value: how much reward given for incorrect trials, should specify negative if negative reward
            card_generator: iterable to generate new set of cards per trial, defaults to a random generator
            rule_generator: iterable to generate new rule per block, defaults to a random generator
            block_switching_condition: function that specifies conditions needed to be satisfied 
                for block switching. Func takes in bool array of performance hist in block, outputs bool
            random seed: seed used to initialize random generators 
        """
        self.correct_value = correct_value
        self.incorrect_value = incorrect_value
        self.block_switching_condition = block_switching_condition

        self.card_generator = card_generator if card_generator else RandomCardGenerator(random_seed)
        self.rule_generator = rule_generator if rule_generator else RandomRuleGenerator(random_seed)
        
        self.start_new_session()
    
    def start_new_session(self):
        self.card_iterator = iter(self.card_generator)
        self.rule_iterator = iter(self.rule_generator)
        
        self.history = []
        self.block_perf = []
        self.current_rule = next(self.rule_iterator)
        self.current_trial = 0
        self.trial_in_block = 0
        self.current_block = 0
        self.trial_reward = 0
        self.total_rewards = 0
        self.current_cards = None
        self.current_selection = None
        self.generated_cards_for_trial = False
        self.is_correct = None



    def get_cards(self):
        if not self.generated_cards_for_trial:
            self.current_cards = next(self.card_generator)
            self.generated_cards_for_trial = True
        return self.current_cards

    def get_cards_text(self):
        return FEATURE_NAMES[self.get_cards()]


    def make_selection(self, selection):
        """
        returns tuple (outcome, reward)
        """
        if self.current_cards is None:
            raise ValueError("No current cards on screen, call get_cards() first")
        self.current_selection = selection
        card = self.current_cards[selection]
        is_correct = self.current_rule in card
        value = self.correct_value if is_correct else self.incorrect_value
        self.block_perf.append(is_correct)
        self.is_correct = is_correct
        self.trial_reward = value
        self.total_rewards += value

        self._log_trial()

        if self.block_switching_condition(np.array(self.block_perf)):
            self.block_perf = []
            self.current_block += 1
            self.current_rule = next(self.rule_iterator)
            self.trial_in_block = 0
        else:
            self.trial_in_block += 1
        
        self.current_cards = None
        self.generated_cards_for_trial = False
        self.current_trial += 1
        return (is_correct, value)


    def _log_trial(self):
        """
        TrialNumber, BlockNumber, TrialAfterRuleChange, Response, ItemChosen, CurrentRule, Reward, 
        Item<Idx><Dim>
        """
        row = {
            "TrialNumber": self.current_trial,
            "BlockNumber": self.current_block,
            "TrialAfterRuleChange": self.trial_in_block,
            "Response": "Correct" if self.is_correct else "Incorrect",
            "ItemChosen": self.current_selection,
            "CurrentRule": FEATURE_NAMES[self.current_rule],
            "Reward": self.trial_reward,
        }
        for card_idx, card in enumerate(FEATURE_NAMES[self.current_cards]):
            for dim_idx, dim in enumerate(DIM_NAMES):
                row[f"Item{card_idx}{dim}"] = card[dim_idx]
        self.history.append(row)


    def dump_history(self):
        return pd.DataFrame(self.history)


    def get_current_rule_text(self):
        return FEATURE_NAMES[self.current_rule]

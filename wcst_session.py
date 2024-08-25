import numpy as np
import pandas as pd

from block_switching_conditions import monkey_condition
from card_generators import RandomCardGenerator
from rule_generators import RandomRuleGeneratorMonkey
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
        prob_reward_matches=None,
        block_switching_condition=monkey_condition,
        enforce_min_block_len=True,
        random_seed=None,
        feature_names=FEATURE_NAMES,
        dim_names=DIM_NAMES,
        should_log_trials=True,
    ):
        """
        Args:
            correct_value: how much reward given for correct trials
            incorrect_value: how much reward given for incorrect trials, should specify negative if negative reward
            card_generator: iterable to generate new set of cards per trial, defaults to a random generator
            rule_generator: iterable to generate new rule per block, defaults to a random generator
            block_switching_condition: function that specifies conditions needed to be satisfied 
                for block switching. Func takes in bool array of performance hist in block, outputs bool
            enforce_min_block_len: bool indicating whether block switching can occur only if a minimum number of 
                trials have occured in that block. If False, it will count trials to criterion even with no trials in the block.
            random seed: seed used to initialize random generators 
        """
        self.correct_value = correct_value
        self.incorrect_value = incorrect_value
        self.block_switching_condition = block_switching_condition
        self.enforce_min_block_len = enforce_min_block_len
        self.prob_reward_matches = prob_reward_matches
        self.should_log_trials = should_log_trials

        self.card_generator = card_generator if card_generator else RandomCardGenerator(random_seed)
        self.rule_generator = rule_generator if rule_generator else RandomRuleGeneratorMonkey(random_seed)
        self.rng = np.random.default_rng(random_seed)

        self.feature_names=feature_names
        self.dim_names=dim_names

        # check num cards, num feature dims, num features, num_rules per card all match up, 
        if not (
            len(feature_names) == self.rule_generator.num_rules and 
            len(dim_names) == self.card_generator.num_dims and 
            self.rule_generator.num_rules == self.card_generator.num_dims * self.card_generator.num_cards
        ): 
            raise ValueError("Lengths of feature and dimensions in rule generator, card generators, and names do not match up")
        
        self.start_new_session()
    
    def start_new_session(self):
        """
        Starts a new session of WCST, wipes any history or tracking
        """
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
        """
        Get the cards to display for trial
        Returns: np array of num_cards x num_dimensions, each element
            is feature index corresponding to FEATURE_NAMES constant
        """
        if not self.generated_cards_for_trial:
            self.current_cards = next(self.card_generator)
            self.generated_cards_for_trial = True
        return self.current_cards

    def get_cards_text(self):
        return self.feature_names[self.get_cards()]


    def make_selection(self, selection):
        """
        Makes a selection of a card, logs information about the trial,
        checks whether to update the rule/block, moves on to next trial. 

        Args:
            selection: int of 0, 1, 2, 3. Index of card 
        Returns:
            (outcome, reward), where outcome is bool for Correct/Incorrect, reward is
            amount of reward received. 
        """
        if self.current_cards is None:
            raise ValueError("No current cards on screen, call get_cards() first")
        self.current_selection = selection
        card = self.current_cards[selection]
        is_correct = self.current_rule in card
        if self.prob_reward_matches is None: 
            value = self.correct_value if is_correct else self.incorrect_value
        else:
            # find associated probabilities for correct, incorrect, randomly make a choice
            # based on those probs. 
            if is_correct:
                probs = [self.prob_reward_matches, 1 - self.prob_reward_matches]
            else:
                probs = [1 - self.prob_reward_matches, self.prob_reward_matches]
            value = self.rng.choice([self.correct_value, self.incorrect_value], p=probs)
        self.block_perf.append(is_correct)
        self.is_correct = is_correct
        self.trial_reward = value
        self.total_rewards += value
        
        if self.should_log_trials:
            self._log_trial()

        if self.block_switching_condition(np.array(self.block_perf)):
            if self.enforce_min_block_len:
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
        Helper func to log trial information in history
        """
        row = {
            "TrialNumber": self.current_trial,
            "BlockNumber": self.current_block,
            "TrialAfterRuleChange": self.trial_in_block,
            "Response": "Correct" if self.is_correct else "Incorrect",
            "ItemChosen": self.current_selection,
            "CurrentRule": self.feature_names[self.current_rule],
            "Reward": self.trial_reward,
        }
        for card_idx, card in enumerate(self.feature_names[self.current_cards]):
            for dim_idx, dim in enumerate(self.dim_names):
                row[f"Item{card_idx}{dim}"] = card[dim_idx]
        self.history.append(row)


    def dump_history(self):
        """
        Creates a dataframe of current history in session, 
        """
        return pd.DataFrame(self.history)


    def get_current_rule_text(self):
        return self.feature_names[self.current_rule]

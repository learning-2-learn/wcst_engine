import numpy as np

class RandomRuleGeneratorMonkey:
    """
    An iterable to just generate a random int from 0 - 11 indicating
    which feature should be the next rule

    It follows statistics from the monkey version of the task,
    where there's 50 50 chance of an intra vs extra dimensional shift
    """
    def __init__(self, seed, num_rules=12, num_dims=3):
        self.rng = np.random.default_rng(seed)
        self.num_rules = num_rules
        self.num_dims = num_dims
        if not num_rules % num_dims == 0:
            raise ValueError(f"number of rules {num_rules} not divisible by number of dimensions {num_dims}")
        self.num_rules_per_dim = num_rules // num_dims

        self.rule = self.rng.integers(0, num_rules, 1)[0]
        self.dimension = self.rule // self.num_rules_per_dim


    def __iter__(self):
        return self

    def __next__(self): 
        """
        randomly generates integer from 0 - 11
        """
        shift_type = self.rng.choice([0,1])
        # If 0, intra dimensional shift
        # If 1, extra dimensional shift

        if shift_type==0:
            self.dimension = self.dimension
        else:
            dimensions = np.arange(self.num_dims)
            dimensions = dimensions[dimensions!=self.dimension]
            self.dimension = self.rng.choice(dimensions)

        features = np.arange(self.num_rules)
        features = features[features//self.num_rules_per_dim==self.dimension]
        features = features[features!=self.rule]
        self.rule = self.rng.choice(features)
        
        return self.rule
    

class RandomRuleGeneratorHuman:
    """
    An iterable to just generate a random int from 0 - 11 indicating
    which feature should be the next rule

    It follows statistics from the human version of the task
    """
    def __init__(self, seed, num_rules=12, num_dims=3):
        self.rng = np.random.default_rng(seed)
        self.rule = self.rng.integers(0, num_rules, 1)[0]
        self.num_rules=num_rules
        self.num_dims=num_dims

    def __iter__(self):
        return self

    def __next__(self): 
        """
        randomly generates integer from 0 - 11
        """
        features = np.arange(self.num_rules)
        features = features[features!=self.rule]
        self.rule = self.rng.choice(features)
        
        return self.rule
    
class ConstantRuleGenerator:
    """
    A rule generator which only ever stays on the same rule, that's specified on initialization
    """
    def __init__(self, num_rules, rule):
        self.num_rules = num_rules
        self.rule = rule

    def __iter__(self):
        return self
    
    def __next__(self):
        return self.rule
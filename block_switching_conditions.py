import numpy as np

def monkey_condition(block_perf_history):
    """
    Block switching condition for monkeys
    Returns true if last 8/8 or 16/20 trials are correct
    False otherwise

    Args: 
        block_perf_history: np array of boolean values
        indicating success of failure/trial in blocks
    """
    block_len = len(block_perf_history)
    if block_len < 8:
        return False
    if np.all(block_perf_history[-8:]):
        return True
    len_to_check = np.min([block_len, 20])
    if np.count_nonzero(block_perf_history[-len_to_check:]) >=16:
        return True
    return False

def human_condition(block_perf_history):
    """
    Block switching condition used for humans
    Returns true if last 5/5 or 8/10 trials are correct
    """
    block_len = len(block_perf_history)
    if block_len < 5:
        return False
    if np.all(block_perf_history[-5:]):
        return True
    len_to_check = np.min([block_len, 10])
    if np.count_nonzero(block_perf_history[-len_to_check:]) >=8:
        return True
    return False

def short_condition(block_perf_history):
    """
    Block switching condition that might be handy for testing
    Returns true if last 3/3 are correct
    """
    block_len = len(block_perf_history)
    if block_len < 3:
        return False
    if np.all(block_perf_history[-3:]):
        return True
    return False
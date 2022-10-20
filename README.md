# wcst_engine

## Goal 
A task engine to evaluate artificial learning agents and learning strategies on the WCST. Allow “users (agents that learn or implement specific strategies” to play the WCST using this engine. This will hopefully enable: 
- Studying how artificial learning agents develop their own strategies, and how they use “internal models” to solve the task 
- Studying how artificial agents implementing different specific strategies perform in different task contexts, enabling comparison to monkey/human strategy and performance. 

## Usage

```
from wcst_session import WcstSession
sess = WcstSession(correct_value=10, incorrect_value=-4, random_seed=42)

sess.get_cards_text()
"""
Output:
array([['TRIANGLE', 'YELLOW', 'ESCHER'],
       ['STAR', 'MAGENTA', 'SWIRL'],
       ['SQUARE', 'CYAN', 'RIPPLE'],
       ['CIRCLE', 'GREEN', 'POLKADOT']], dtype='<U8')
"""

sess.make_selection(2)
"""
Output: 
(True, 10)
"""
```

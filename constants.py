import numpy as np

FEATURE_NAMES = np.array([
    'CIRCLE', 'SQUARE', 'STAR', 'TRIANGLE', 
    'CYAN', 'GREEN', 'MAGENTA', 'YELLOW', 
    'ESCHER', 'POLKADOT', 'RIPPLE', 'SWIRL'
])

DIM_NAMES = ["Shape", "Color", "Pattern"]

# names for WCST with extended feature dimension
EXTENEDED_DIM_NAMES = ["Shape", "Color", "Pattern", "Outline"]
EXTENDED_DIM_FEATURE_NAMES = np.array([
    'CIRCLE', 'SQUARE', 'STAR', 'TRIANGLE', 
    'CYAN', 'GREEN', 'MAGENTA', 'YELLOW', 
    'ESCHER', 'POLKADOT', 'RIPPLE', 'SWIRL',
    'SOLID', 'DOTTED', 'DASHED', 'DASHDOT'
])
from matplotlib.colors import LinearSegmentedColormap

_WALES_BSR_CDICT = {
    "red": (
        (0.0, 0.8, 0.8),
        (0.1, 0.0, 0.0),
        (0.3, 0.0, 0.0),
        (0.6, 1.0, 1.0),
        (0.7, 1.0, 1.0),
        (1.0, 0.3, 0.3)
    ),
    "green": (
        (0.0, 0.9, 0.9),
        (0.1, 0.0, 0.0),
        (0.3, 0.8, 0.8),
        (0.6, 0.8, 0.8),
        (0.8, 0.0, 0.0),
        (1.0, 0.0, 0.0),
    ),
    "blue": (
        (0.0, 1.0, 1.0),
        (0.25, 0.0, 0.0),
        (1.0, 0.0, 0.0),
    ),
}

WALES_BSR = LinearSegmentedColormap('WALES_BSR', _WALES_BSR_CDICT)

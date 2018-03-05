from matplotlib.colors import LogNorm
from matplotlib.ticker import FixedLocator

WALES_BSR_NORM = LogNorm(vmin=1, vmax=100)
WALES_BSR_TICK_LOCATOR = FixedLocator([
    1, 1.2, 1.4, 1.6, 1.8, 2.0, 4.0, 6.0, 8.0, 10.0, 30.0, 50.0, 70.0, 90.0
])

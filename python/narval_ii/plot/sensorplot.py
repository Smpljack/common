from .colormaps import WALES_BSR
from .normalization import WALES_BSR_NORM, WALES_BSR_TICK_LOCATOR
from matplotlib.ticker import ScalarFormatter

import matplotlib.pyplot as plt

def wales_bsr_plot(time, height, bsr, ax=None):
    if ax is not None:
        return ax.pcolormesh(time, height, bsr, norm=WALES_BSR_NORM, cmap=WALES_BSR)
    else:
        return plt.pcolormesh(time, height, bsr, norm=WALES_BSR_NORM, cmap=WALES_BSR)

def wales_bsr_colorbar(mappable=None, cax=None):
    return plt.colorbar(mappable, cax=cax, label="BSR",
            format=ScalarFormatter(), ticks=WALES_BSR_TICK_LOCATOR)

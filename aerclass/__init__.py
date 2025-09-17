# __init__.py - Initialization for aerclass package

__version__ = "1.0.0"

# Import main submodules
from . import classify
from . import uncertainty
from . import utils
from . import plots

# ---- Import core functions for direct access ----
from .classify import (
    classify_methodI, classify_methodII, classify_methodIII,
    classify_methodIVA, classify_methodIVB,
    classify_methodV, classify_methodVI
)
from .plots import distribution_plot, barplot

# ---- Define public API ----
__all__ = [
    "classify_methodI", "classify_methodII", "classify_methodIII",
    "classify_methodIVA", "classify_methodIVB",
    "classify_methodV", "classify_methodVI",
    "distribution_plot", "barplot",
    "__version__"
]

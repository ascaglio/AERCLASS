# main.py - Entry point for running all AERCLASS classification methods

import os
import pandas as pd
import matplotlib.pyplot as plt

from aerclass.classify import (
    classify_methodI, classify_methodII, classify_methodIII,
    classify_methodIVA, classify_methodIVB, classify_methodV, classify_methodVI
)
from aerclass.plots import distribution_plot, barplot

# --- User-defined parameters ---
FILE = 'alta_floresta_daily.xlsx'
SITE = 'Alta Floresta'
OUTPUT_DIR = 'output'   # directory to save plots and data
SAVE_PLOTS = True
SAVE_DATA = True

AOD_ERROR = 0.01
SSA_ERROR = 0.03
RRI_ERROR = 0.04
FILTER_AOD = [False, 0.4]

# --- Ensure output directory exists ---
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Load data ---
data = pd.read_excel(FILE)

# --- Dictionary of methods and parameters ---
methods = {
    "Method I": (classify_methodI, {'aod_error': AOD_ERROR, 'filter_aod': FILTER_AOD}, 'aod440', 'eae440_870'),
    "Method II": (classify_methodII, {'aod_error': AOD_ERROR, 'filter_aod': FILTER_AOD}, 'arod', 'arod'),
    "Method III": (classify_methodIII, {'aod_error': AOD_ERROR, 'filter_aod': FILTER_AOD}, 'fmf500', 'fmf500'),
    "Method IVA": (classify_methodIVA, {'aod_error': AOD_ERROR, 'ssa_error': SSA_ERROR, 'filter_aod': FILTER_AOD}, 'ssa440', 'eae440_870'),
    "Method IVB": (classify_methodIVB, {'aod_error': AOD_ERROR, 'ssa_error': SSA_ERROR, 'filter_aod': FILTER_AOD}, 'ssa440', 'eae440_870'),
    "Method V": (classify_methodV, {'aod_error': AOD_ERROR, 'ssa_error': SSA_ERROR, 'filter_aod': FILTER_AOD}, 'aae', 'eae440_870'),
    "Method VI": (classify_methodVI, {'aod_error': AOD_ERROR, 'rri_error': RRI_ERROR, 'filter_aod': FILTER_AOD}, 'rri440', 'eae440_870'),
}

# --- Run and plot each method ---
for method_name, (func, kwargs, xvar, yvar) in methods.items():
    print(f"Running {method_name}...")
    outcome, df = func(data.copy(), **kwargs)

    # Create and save distribution plot
    dist_ax = distribution_plot(df, method_name, SITE, xvar=xvar, yvar=yvar)
    if SAVE_PLOTS:
        dist_fig = dist_ax.get_figure()
        dist_fig.savefig(os.path.join(OUTPUT_DIR, f"{method_name.replace(' ', '_')}_scatter.png"))

    # Create and save bar plot
    bar_ax = barplot(outcome, method_name, SITE)
    if SAVE_PLOTS:
        bar_fig = bar_ax.get_figure()
        bar_fig.savefig(os.path.join(OUTPUT_DIR, f"{method_name.replace(' ', '_')}_barplot.png"))

    # Save dataframes
    if SAVE_DATA:
        df.to_csv(os.path.join(OUTPUT_DIR, f"{method_name.replace(' ', '_')}_data.csv"), index=False)
        outcome.to_csv(os.path.join(OUTPUT_DIR, f"{method_name.replace(' ', '_')}_outcome.csv"), index=False)

    plt.show()
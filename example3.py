#RECORDAR CAMBIAR LOS VALORES SUBESTIMADOS PARA QUE NO SEAN NEGATIVOS

#Complete usage example of AERCLASS with all methods

import pandas as pd
import matplotlib.pyplot as plt

from aerclass.classify import (
    classify_methodI, classify_methodII, classify_methodIII,
    classify_methodIVA, classify_methodIVB, classify_methodV, classify_methodVI
)
from aerclass.plots import distribution_plot, barplot

# --------------------
# Load data
# --------------------
FILE = 'alta_floresta_daily.xlsx'
SITE = 'Alta Floresta'

data = pd.read_excel(FILE)

# --------------------
# Define general parameters
# --------------------
AOD_ERROR = 0.01
SSA_ERROR = 0.03
RRI_ERROR = 0.04
FILTER_AOD = [False, 0.4]

# --------------------
# Run all methods and generate plots
# --------------------
methods = {
    "Method I": (classify_methodI, {'aod_error': AOD_ERROR, 'filter_aod': FILTER_AOD}, 'aod440', 'eae440_870'),
    "Method II": (classify_methodII, {'aod_error': AOD_ERROR, 'filter_aod': FILTER_AOD}, 'aod440', 'arod'),
    "Method III": (classify_methodIII, {'aod_error': AOD_ERROR, 'filter_aod': FILTER_AOD}, 'aod500', 'fmf500'),
    "Method IVA": (classify_methodIVA, {'aod_error': AOD_ERROR, 'ssa_error': SSA_ERROR, 'filter_aod': FILTER_AOD}, 'eae440_870', 'ssa440'),
    "Method IVB": (classify_methodIVB, {'aod_error': AOD_ERROR, 'ssa_error': SSA_ERROR, 'filter_aod': FILTER_AOD}, 'eae440_870', 'ssa440'),
    "Method V": (classify_methodV, {'aod_error': AOD_ERROR, 'ssa_error': SSA_ERROR, 'filter_aod': FILTER_AOD}, 'eae440_870', 'aae'),
    "Method VI": (classify_methodVI, {'aod_error': AOD_ERROR, 'rri_error': RRI_ERROR, 'filter_aod': FILTER_AOD}, 'eae440_870', 'rri440'),
}


for method_name, (func, kwargs, xvar, yvar) in methods.items():
    print(f"\nRunning {method_name}...")
    #Generate output DataFrames
    outcome, df = func(data.copy(), **kwargs)

    # Scatter plot in classification space
    dist_ax = distribution_plot(df, method_name, SITE, xvar=xvar, yvar=yvar)

    # Bar plot of misclassification
    bar_ax = barplot(outcome, method_name, SITE)

    plt.show()

    # Save results
    df.to_csv(f'{method_name.replace(" ", "_").lower()}_classified_data.csv', index=False)
    outcome.to_csv(f'{method_name.replace(" ", "_").lower()}_summary.csv', index=False)
    print("Saved data and summary for", method_name)

print("\nAll methods completed.")

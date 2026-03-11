"""
run_aerclass.py - AERCLASS quick start example.

This script demonstrates the basic workflow of the AERCLASS package:
1. Load aerosol optical data
2. Apply classification schemes
3. Propagate measurement uncertainties
4. Estimate misclassification probabilities

Modify the input data path and parameters as needed.
"""

# --------------------------------------------------
# Import libraries and AERCLASS submodules
# --------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt

from aerclass import (
    classify_methodI, classify_methodII, classify_methodIII,
    classify_methodIVA, classify_methodIVB,
    classify_methodV, classify_methodVI,
    distribution_plot, barplot
)


def main():

    # --------------------
    # Load data
    # --------------------
    FILE = 'example/data/alta_floresta_daily.xlsx'
    SITE = 'Alta Floresta'

    data = pd.read_excel(FILE)

    # --------------------
    # Define general parameters
    # --------------------
    AOD_ERROR = 0.01
    SSA_ERROR = 0.03
    RRI_ERROR = 0.04
    FILTER_AOD = [False, 0.4]

    dpi = 300
    alpha = 0.4
    fontsize = 14

    # --------------------
    # Run all methods
    # --------------------
    methods = {
        "Method I": (classify_methodI, {'aod_error': AOD_ERROR, 'filter_aod': FILTER_AOD}, 'aod440', 'eae'),
        "Method II": (classify_methodII, {'aod_error': AOD_ERROR, 'filter_aod': FILTER_AOD}, 'aod440', 'arod'),
        "Method III": (classify_methodIII, {'aod_error': AOD_ERROR, 'filter_aod': FILTER_AOD}, 'aod500', 'fmf500'),
        "Method IVA": (classify_methodIVA, {'aod_error': AOD_ERROR, 'ssa_error': SSA_ERROR, 'filter_aod': FILTER_AOD}, 'eae', 'ssa440'),
        "Method IVB": (classify_methodIVB, {'aod_error': AOD_ERROR, 'ssa_error': SSA_ERROR, 'filter_aod': FILTER_AOD}, 'eae', 'ssa440'),
        "Method V": (classify_methodV, {'aod_error': AOD_ERROR, 'ssa_error': SSA_ERROR, 'filter_aod': FILTER_AOD}, 'eae', 'aae'),
        "Method VI": (classify_methodVI, {'aod_error': AOD_ERROR, 'rri_error': RRI_ERROR, 'filter_aod': FILTER_AOD}, 'eae', 'rri440'),
    }

    # --------------------
    # Generate plots and save results
    # --------------------
    for method_name, (func, kwargs, xvar, yvar) in methods.items():

        print(f"\nRunning {method_name}...")

        outcome, df = func(data.copy(), **kwargs)

        dist_ax = distribution_plot(
            df,
            method_name,
            SITE,
            xvar=xvar,
            yvar=yvar,
            dpi=dpi,
            alpha=alpha,
            fontsize=fontsize
        )

        bar_ax = barplot(
            outcome,
            method_name,
            SITE,
            dpi=dpi,
            fontsize=fontsize
        )

        plt.show()

        df.to_csv(
            f'{method_name.replace(" ", "_").lower()}_classified_data.csv',
            index=False
        )

        outcome.to_csv(
            f'{method_name.replace(" ", "_").lower()}_summary.csv',
            index=False
        )

        print("Saved data and summary for", method_name)

    print("\nAll methods completed.")


# --------------------------------------------------
# Run script
# --------------------------------------------------

if __name__ == "__main__":
    main()
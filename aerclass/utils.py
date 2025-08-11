# utils.py - Utility functions for AERCLASS

import pandas as pd
import numpy as np

def compute_missclasification(df, original_data, aerosol_types):
    """
    Computes the misclassification rate and aerosol percentages, and adds global metrics.
    """
    result = []
    total_points = len(df)
    misclassified_total = 0

    for key, label in aerosol_types.items():
        class_mask = df['class'] == key
        total = class_mask.sum()
        if total == 0:
            rate = 0.0
        else:
            mismatches = (
                (df['class_00'] != key) |
                (df['class_01'] != key) |
                (df['class_10'] != key) |
                (df['class_11'] != key)
            ) & class_mask
            misclassified = mismatches.sum()
            misclassified_total += misclassified
            rate = 100 * misclassified / total

        percent_in_data = 100 * total / total_points if total_points > 0 else 0
        result.append({
            'type': label,
            'misclassification_rate': round(rate, 2),
            'percent_of_total': round(percent_in_data, 2)
        })

    outcome_df = pd.DataFrame(result)

    # --- Global metrics ---
    mr_global = 100 * misclassified_total / total_points if total_points > 0 else 0

    # Add summary row
    outcome_df = pd.concat([
        outcome_df,
        pd.DataFrame([{
            'type': 'TOTAL',
            'misclassification_rate': round(mr_global, 2)
        }])
    ], ignore_index=True)

    return outcome_df

def calculate_eae(aod440, aod870):
    """Calculate extinction Ångstrom exponent from AODs at 440 and 870 nm."""
    return np.log(aod870 / aod440) / np.log(440 / 870)

def calculate_arod(aod1020, aod440):
    """Calculate Aerosol Relative Optical Depth (AROD)."""
    return aod1020 / aod440

def calculate_aae(aod440, aod870, ssa440, ssa870):
    """Calculate Absorption Ångstrom Exponent from AOD and SSA."""
    aaod_440 = (1 - ssa440) * aod440
    aaod_870 = (1 - ssa870) * aod870
    return -(np.log(aaod_870) - np.log(aaod_440)) / (np.log(870) - np.log(440))




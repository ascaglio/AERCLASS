# utils.py - Utility functions for AERCLASS

import pandas as pd
import numpy as np

AEROSOL_STYLES = {
    "M":  {"label": "M",  "color": "b"},
    "MUIBB":  {"label": "MUIBB",  "color": "m"},
    "BB": {"label": "BB", "color": "grey"},
    "MDM": {"label": "MDM", "color": "g"},
    "D": {"label": "D", "color": "yellow"},
    "SC": {"label":"SC", "color": "purple"},
    "UI": {"label":"UI", "color": "r"},
    "C": {"label":"C", "color": "brown"},
    "NC": {"label":"NC", "color": "white"},
    "StrAFP": {"label":"StrAFP", "color": "orange"},
    "MAFP": {"label":"MAFP", "color": "pink"},
    "SliAFP": {"label":"SliAFP", "color": "olive"},
    "WAFP": {"label":"WAFP", "color": "cyan"},
    "MAP": {"label":"MAP", "color": "rosybrown"},
    "MWAP": {"label":"MWAP", "color": "indianred"},
    "ACP": {"label":"ACP", "color": "chocolate"},
    "WACP": {"label":"WACP", "color": "teal"}
}

CLASS_NUMERIC_TO_CODE = {
    1: "M",
    2: "MUIBB",
    3: "BB",
    4: "MDM",
    5: "D",
    6: "SC",
    7: "UI",
    8: "C",
    9: "NC",
    10: "StrAFP",
    11: "MAFP",
    12: "SliAFP",
    13: "WAFP",
    14: "MAP",
    15: "MWAP",
    16: "ACP",
    17: "WACP"
}

METHOD_TO_CLASSES = {
    "Method I": [CLASS_NUMERIC_TO_CODE[i] for i in (1, 2, 3, 4)],
    "Method II": [CLASS_NUMERIC_TO_CODE[i] for i in (1, 5, 6, 7, 3, 8)],
    "Method III": [CLASS_NUMERIC_TO_CODE[i] for i in (1, 5, 8)],
    "Method IVA": [CLASS_NUMERIC_TO_CODE[i] for i in (5, 7, 3, 9)],
    "Method IVB": [CLASS_NUMERIC_TO_CODE[i] for i in range(10, 18)],
    "Method V": [CLASS_NUMERIC_TO_CODE[i] for i in (5, 7, 3, 9)],
    "Method VI": [CLASS_NUMERIC_TO_CODE[i] for i in (5, 7, 3, 9)]
}

def ensure_class_code(df):

    if "class_code" not in df.columns and "class" in df.columns:
        df["class_code"] = df["class"].map(CLASS_NUMERIC_TO_CODE)
    return df

def compute_missclasification(df, original_data, aerosol_types):
    """
    Computes the misclassification rate and aerosol percentages, and adds global metrics.
    """
    df = ensure_class_code(df)
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

    mr_global = 100 * misclassified_total / total_points if total_points > 0 else 0

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




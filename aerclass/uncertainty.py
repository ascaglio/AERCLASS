# uncertainty.py - Error propagation module for AERCLASS

import numpy as np
import pandas as pd

def propagate_uncertainties(method_id, df, aod_error=0.01, ssa_error=0.03, rri_error=0.04):
    if method_id == 1:
        return propagate_methodI(df, aod_error)
    elif method_id == 2:
        return propagate_methodII(df, aod_error)
    elif method_id == 3:
        return propagate_methodIII(df, aod_error)
    elif method_id in [4, 5]:
        return propagate_methodIV(df, aod_error, ssa_error)
    elif method_id == 6:
        return propagate_methodV(df, aod_error, ssa_error)
    elif method_id == 7:
        return propagate_methodVI(df, aod_error, rri_error)
    else:
        raise ValueError("Unsupported method_id")


def propagate_methodI(df, aod_error):
    # EAE = ln(AOD870/AOD440)/ln(440/870)
    d_eae_d_aod440 = -1 / (df['aod440'] * np.log(440/870))
    d_eae_d_aod870 = 1 / (df['aod870'] * np.log(440/870))
    eae_error = np.sqrt((d_eae_d_aod440 * aod_error)**2 + (d_eae_d_aod870 * aod_error)**2)
    df['eae_sub'] = np.maximum(df['eae440_870'] - eae_error,0)
    df['eae_sob'] = df['eae440_870'] + eae_error
    df['aod_sub'] = np.maximum(df['aod440'] - aod_error,0)
    df['aod_sob'] = df['aod440'] + aod_error
    return df


def propagate_methodII(df, aod_error):
    # AROD = AOD1020 / AOD440
    d_arod_d_1020 = 1 / df['aod440']
    d_arod_d_440 = -df['aod1020'] / (df['aod440']**2)
    arod_error = np.sqrt((d_arod_d_1020 * aod_error)**2 + (d_arod_d_440 * aod_error)**2)
    df['arod_sub'] = df['arod'] - arod_error
    df['arod_sob'] = df['arod'] + arod_error
    return df


def propagate_methodIII(df, aod_error):
    df['fmf500_sub'] = df['fmf500'] - df['rmse_fmf']
    df['fmf500_sob'] = df['fmf500'] + df['rmse_fmf']
    return df


def propagate_methodIV(df, aod_error, ssa_error):
    return propagate_methodI(df, aod_error).assign(
        ssa_sub=df['ssa440'] - ssa_error,
        ssa_sob=df['ssa440'] + ssa_error
    )


def propagate_methodV(df, aod_error, ssa_error):
    # AAOD = (1 - SSA) * AOD
    aaod_440 = (1 - df['ssa440']) * df['aod440']
    aaod_870 = (1 - df['ssa870']) * df['aod870']
    df['aae'] = -(np.log(aaod_870) - np.log(aaod_440)) / (np.log(870) - np.log(440))

    # Propagation
    daaod440 = np.sqrt((aod_error)**2 + (ssa_error * df['aod440'])**2)
    daaod870 = np.sqrt((aod_error)**2 + (ssa_error * df['aod870'])**2)
    aae_error = np.sqrt((1/aaod_440)**2 * daaod440**2 + (1/aaod_870)**2 * daaod870**2) / np.abs(np.log(870) - np.log(440))
    df['aae_sub'] = df['aae'] - aae_error
    df['aae_sob'] = df['aae'] + aae_error

    return propagate_methodI(df, aod_error).assign(
        ssa_sub=df['ssa440'] - ssa_error,
        ssa_sob=df['ssa440'] + ssa_error
    )


def propagate_methodVI(df, aod_error, rri_error):
    return propagate_methodI(df, aod_error).assign(
        rri_sub=df['rri440'] - rri_error,
        rri_sob=df['rri440'] + rri_error
    )

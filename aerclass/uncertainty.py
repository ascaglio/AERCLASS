# uncertainty.py - Error propagation module for AERCLASS

import numpy as np

# Monte Carlo
def propagate_with_montecarlo(func, inputs, errors, n_iter=5000):
    """Propaga incertidumbres usando simulaciones Monte Carlo."""
    samples = []
    for _ in range(n_iter):
        perturbed = [np.random.normal(xi, σxi) for xi, σxi in zip(inputs, errors)]
        samples.append(func(*perturbed))
    return np.std(samples)

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
    d_eae_d_aod440 = -1 / (df['aod440'] * np.log(440/870))
    d_eae_d_aod870 = 1 / (df['aod870'] * np.log(440/870))
    eae_error_partials = np.sqrt((d_eae_d_aod440 * aod_error)**2 + (d_eae_d_aod870 * aod_error)**2)
    eae_error_mc = [
        propagate_with_montecarlo(
            lambda a440, a870: np.log(a870 / a440) / np.log(440/870),
            [a440, a870], [aod_error, aod_error]
        )
        for a440, a870 in zip(df['aod440'], df['aod870'])
    ]
    
    eae_error = np.maximum(eae_error_partials, eae_error_mc)    

    df['eae_sub'] = np.maximum(df['eae'] - eae_error,0)
    df['eae_sob'] = df['eae'] + eae_error
    df['aod440_sub'] = np.maximum(df['aod440'] - aod_error,0)
    df['aod440_sob'] = df['aod440'] + aod_error
    return df


def propagate_methodII(df, aod_error):
    d_arod_d_1020 = 1 / df['aod440']
    d_arod_d_440 = -df['aod1020'] / (df['aod440']**2)
    arod_error_partials = np.sqrt((d_arod_d_1020 * aod_error)**2 + (d_arod_d_440 * aod_error)**2)
    
    arod_error_mc = [
        propagate_with_montecarlo(
            lambda a1020, a440: a1020 / a440,
            [a1020, a440], [aod_error, aod_error]
        )
        for a1020, a440 in zip(df['aod1020'], df['aod440'])
    ]

    arod_error = np.maximum(arod_error_partials, arod_error_mc)    
    df['arod_sub'] = np.maximum(df['arod'] - arod_error, 0)
    df['arod_sob'] = df['arod'] + arod_error

    return propagate_methodI(df, aod_error)

def propagate_methodIII(df, aod_error):
    df['fmf500_sub'] = np.maximum(df['fmf500'] - df['rmse_fmf'],0)
    df['fmf500_sob'] = df['fmf500'] + df['rmse_fmf']
    df['aod500_sub'] = np.maximum(df['aod500'] - aod_error,0)
    df['aod500_sob'] = df['aod500'] + aod_error
    return df


def propagate_methodIV(df, aod_error, ssa_error):    
    df['ssa440_sub'] = np.maximum(df['ssa440'] - ssa_error,0)
    df['ssa440_sob'] = df['ssa440'] + ssa_error
    return propagate_methodI(df, aod_error)    


def propagate_methodV(df, aod_error, ssa_error):
    aaod_440 = (1 - df['ssa440']) * df['aod440']
    aaod_870 = (1 - df['ssa870']) * df['aod870']
    df['aae'] = -(np.log(aaod_870) - np.log(aaod_440)) / (np.log(870) - np.log(440))

    daaod440 = np.sqrt((aod_error)**2 + (ssa_error * df['aod440'])**2)
    daaod870 = np.sqrt((aod_error)**2 + (ssa_error * df['aod870'])**2)
    aae_error_partials = np.sqrt((1/aaod_440)**2 * daaod440**2 + (1/aaod_870)**2 * daaod870**2) / np.abs(np.log(870) - np.log(440))
    aae_error_mc = [
        propagate_with_montecarlo(
            lambda a440, a870, s440, s870: -(np.log((1-s870)*a870) - np.log((1-s440)*a440)) / (np.log(870) - np.log(440)),
            [a440, a870, s440, s870],
            [aod_error, aod_error, ssa_error, ssa_error]
        )
        for a440, a870, s440, s870 in zip(df['aod440'], df['aod870'], df['ssa440'], df['ssa870'])
    ]

    aae_error = np.maximum(aae_error_partials, aae_error_mc)

    df['aae_sub'] = np.maximum(df['aae'] - aae_error, 0)
    df['aae_sob'] = df['aae'] + aae_error

    return propagate_methodI(df, aod_error)
    
def propagate_methodVI(df, aod_error, rri_error):
    df['rri440_sub'] = np.maximum(df['rri440'] - rri_error,0)
    df['rri440_sob'] = df['rri440'] + rri_error
    return propagate_methodI(df, aod_error)

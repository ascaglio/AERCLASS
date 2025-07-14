# Classification methods for AERCLASS

import numpy as np
from aerclass.uncertainty import propagate_uncertainties
from aerclass.utils import compute_missclasification, calculate_eae, calculate_arod, calculate_aae


def compute_dist(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def run_classification(df, func, xcol, ycol, method_id, aerosol_types,
                       aod_error=0.01, ssa_error=0.03, rri_error=0.04):
    df = propagate_uncertainties(method_id, df, aod_error, ssa_error, rri_error)
    df['class'] = [func(x, y) for x, y in zip(df[xcol], df[ycol])]
    df['class_00'] = [func(x, y) for x, y in zip(df[f'{xcol}_sub'], df[f'{ycol}_sub'])]
    df['class_01'] = [func(x, y) for x, y in zip(df[f'{xcol}_sub'], df[f'{ycol}_sob'])]
    df['class_10'] = [func(x, y) for x, y in zip(df[f'{xcol}_sob'], df[f'{ycol}_sub'])]
    df['class_11'] = [func(x, y) for x, y in zip(df[f'{xcol}_sob'], df[f'{ycol}_sob'])]
    return compute_missclasification(df, df.copy(), aerosol_types), df


# --------------------------
# Method I - EAE vs AOD (Cúneo et al., 2022)
# --------------------------
def classification_functionI(aod, eae):
    if aod <= 0.08 and eae <= 1.13:
        return 1
    elif aod <= 0.08 and eae > 1.13:
        return 2
    elif aod > 0.08 and eae > 1.13:
        return 3
    else:
        return 4

def classify_methodI(data, aod_error=0.01, filter_aod=[False, 0.4]):
    aerosol_types = {1: 'M', 2: 'MUIBB', 3: 'BB', 4: 'MDM'}
    if 'eae440_870' not in data.columns:
        data['eae440_870'] = calculate_eae(data['aod440'], data['aod870'])
    df = data[['aod440', 'aod870', 'eae440_870']].dropna().reset_index(drop=True)
    if filter_aod[0]:
        df = df[df['aod440'] >= filter_aod[1]]
    return run_classification(df, classification_functionI, 'aod440', 'eae440_870',
                              method_id=1, aerosol_types=aerosol_types,
                              aod_error=aod_error)


# --------------------------
# Method II - AROD vs AOD (Chen et al., 2016)
# --------------------------
def classification_functionII(arod, _):
    if arod < 0.3:
        return 1
    elif 0.3 <= arod < 0.5:
        return 2
    elif 0.5 <= arod < 0.8:
        return 3
    elif 0.8 <= arod < 1.0:
        return 4
    elif 1.0 <= arod < 1.2:
        return 5
    else:
        return 6

def classify_methodII(data, aod_error=0.01, filter_aod=[False, 0.4]):
    aerosol_types = {1: 'M', 2: 'D', 3: 'SC', 4: 'UI', 5: 'BB', 6: 'C'}
    data['arod'] = calculate_arod(data['aod1020'], data['aod440'])
    df = data[['aod440', 'aod1020', 'arod']].dropna().reset_index(drop=True)
    if filter_aod[0]:
        df = df[df['aod440'] >= filter_aod[1]]
    return run_classification(df, classification_functionII, 'arod', 'arod',
                              method_id=2, aerosol_types=aerosol_types,
                              aod_error=aod_error)


# --------------------------
# Method III - FMF vs AOD (Barnaba & Gobby, 2004)
# --------------------------
def classification_functionIII(fmf, _):
    if fmf <= 0.2:
        return 1
    elif 0.2 < fmf <= 0.6:
        return 2
    else:
        return 3

def classify_methodIII(data, aod_error=0.01, filter_aod=[False, 0.4]):
    aerosol_types = {1: 'M', 2: 'D', 3: 'C'}
    df = data[['aod440', 'aod500', 'fmf500', 'rmse_fmf']].dropna().reset_index(drop=True)
    if filter_aod[0]:
        df = df[df['aod440'] >= filter_aod[1]]
    return run_classification(df, classification_functionIII, 'fmf500', 'fmf500',
                              method_id=3, aerosol_types=aerosol_types,
                              aod_error=aod_error)


# --------------------------
# Method IVA - SSA vs EAE (Liu & Yi, 2022)
# --------------------------
def classification_functionIVA(ssa, eae):
    if 0.88 <= ssa <= 0.96 and 0.1 <= eae <= 0.4:
        return 1
    elif 0.82 <= ssa <= 0.96 and 0.9 <= eae <= 1.7:
        return 2
    elif 0.82 <= ssa <= 0.96 and 1.7 < eae <= 2.2:
        return 3
    else:
        return 4

def classify_methodIVA(data, aod_error=0.01, ssa_error=0.03, filter_aod=[False, 0.4]):
    aerosol_types = {1: 'D', 2: 'UI', 3: 'BB', 4: 'NC'}
    if 'eae440_870' not in data.columns:
        data['eae440_870'] = calculate_eae(data['aod440'], data['aod870'])
    df = data[['aod440', 'aod870', 'eae440_870', 'ssa440']].dropna().reset_index(drop=True)
    if filter_aod[0]:
        df = df[df['aod440'] >= filter_aod[1]]
    return run_classification(df, classification_functionIVA, 'ssa440', 'eae440_870',
                              method_id=4, aerosol_types=aerosol_types,
                              aod_error=aod_error, ssa_error=ssa_error)


# --------------------------
# Method IVB - SSA vs EAE (Zheng et al., 2021)
# --------------------------
def classification_functionIVB(ssa, eae):
    if ssa >= 0.95 and eae >= 1.3:
        return 1
    elif 0.9 <= ssa < 0.95 and eae >= 1.3:
        return 2
    elif 0.85 <= ssa < 0.9 and eae >= 1.3:
        return 3
    elif ssa < 0.85 and eae >= 1.3:
        return 4
    elif ssa >= 0.85 and 0.6 <= eae < 1.3:
        return 5
    elif ssa < 0.85 and 0.6 <= eae < 1.3:
        return 6
    elif ssa >= 0.85 and eae < 0.6:
        return 7
    else:
        return 8

def classify_methodIVB(data, aod_error=0.01, ssa_error=0.03, filter_aod=[False, 0.4]):
    aerosol_types = {1: 'StrAFP', 2: 'MAFP', 3: 'SliAFP', 4: 'WAFP', 5: 'MAP', 6: 'MWAP', 7: 'ACP', 8: 'WACP'}
    if 'eae440_870' not in data.columns:
        data['eae440_870'] = calculate_eae(data['aod440'], data['aod870'])
    df = data[['aod440', 'aod870', 'eae440_870', 'ssa440']].dropna().reset_index(drop=True)
    if filter_aod[0]:
        df = df[df['aod440'] >= filter_aod[1]]
    return run_classification(df, classification_functionIVB, 'ssa440', 'eae440_870',
                              method_id=5, aerosol_types=aerosol_types,
                              aod_error=aod_error, ssa_error=ssa_error)


# --------------------------
# Method V - AAE vs EAE (Liu & Yi, 2022)
# --------------------------
def classification_functionV(aae, eae):
    if 0.6 <= aae <= 1.0 and 0.1 <= eae <= 0.4:
        return 1
    elif 1.1 <= aae <= 1.6 and 0.9 <= eae <= 1.7:
        return 2
    elif 1.6 < aae <= 2.2 and 1.7 < eae <= 2.2:
        return 3
    else:
        return 4

def classify_methodV(data, aod_error=0.01, ssa_error=0.03, filter_aod=[False, 0.4]):
    aerosol_types = {1: 'D', 2: 'UI', 3: 'BB', 4: 'NC'}
    if 'eae440_870' not in data.columns:
        data['eae440_870'] = calculate_eae(data['aod440'], data['aod870'])
    data['aae'] = calculate_aae(data['aod440'], data['aod870'], data['ssa440'], data['ssa870'])
    df = data[['aod440', 'aod870', 'eae440_870', 'ssa440', 'ssa870', 'aae']].dropna().reset_index(drop=True)
    if filter_aod[0]:
        df = df[df['aod440'] >= filter_aod[1]]
    return run_classification(df, classification_functionV, 'aae', 'eae440_870',
                              method_id=6, aerosol_types=aerosol_types,
                              aod_error=aod_error, ssa_error=ssa_error)


# --------------------------
# Method VI - RRI vs EAE (Liu & Yi, 2022)
# --------------------------
def classification_functionVI(rri, eae):
    if 1.4 <= rri <= 1.6 and 0.1 <= eae <= 0.4:
        return 1
    elif 1.4 <= rri <= 1.6 and 0.9 <= eae <= 1.7:
        return 2
    elif 1.4 <= rri <= 1.6 and 1.7 < eae <= 2.2:
        return 3
    else:
        return 4

def classify_methodVI(data, aod_error=0.01, rri_error=0.04, filter_aod=[False, 0.4]):
    aerosol_types = {1: 'D', 2: 'UI', 3: 'BB', 4: 'NC'}
    if 'eae440_870' not in data.columns:
        data['eae440_870'] = calculate_eae(data['aod440'], data['aod870'])
    df = data[['aod440', 'aod870', 'eae440_870', 'rri440']].dropna().reset_index(drop=True)
    if filter_aod[0]:
        df = df[df['aod440'] >= filter_aod[1]]
    return run_classification(df, classification_functionVI, 'rri440', 'eae440_870',
                              method_id=7, aerosol_types=aerosol_types,
                              aod_error=aod_error, rri_error=rri_error)

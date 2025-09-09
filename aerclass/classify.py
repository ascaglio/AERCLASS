# Classification methods for AERCLASS

import numpy as np
from aerclass.uncertainty import propagate_uncertainties
from aerclass.utils import (compute_missclasification, calculate_eae,
                            calculate_arod, calculate_aae, ensure_class_code, 
                            CLASS_NUMERIC_TO_CODE, METHOD_TO_CLASSES)


def compute_dist(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def run_classification(df, func, xcol, ycol, method_id,
                       aod_error=0.01, ssa_error=0.03, rri_error=0.04):
    df = propagate_uncertainties(method_id, df, aod_error, ssa_error, rri_error)
    df['class'] = [func(x, y) for x, y in zip(df[xcol], df[ycol])]
    df['class_00'] = [func(x, y) for x, y in zip(df[f'{xcol}_sub'], df[f'{ycol}_sub'])]
    df['class_01'] = [func(x, y) for x, y in zip(df[f'{xcol}_sub'], df[f'{ycol}_sob'])]
    df['class_10'] = [func(x, y) for x, y in zip(df[f'{xcol}_sob'], df[f'{ycol}_sub'])]
    df['class_11'] = [func(x, y) for x, y in zip(df[f'{xcol}_sob'], df[f'{ycol}_sob'])]
    df = ensure_class_code(df)
    return compute_missclasification(df, df.copy(), CLASS_NUMERIC_TO_CODE), df


# --------------------------
# Method I - EAE vs AOD (Cúneo et al., 2022)
# --------------------------
def classification_functionI(aod, eae):
    if aod <= 0.08 and eae <= 1.13:
        return 1 #M
    elif aod <= 0.08 and eae > 1.13:
        return 2 #MUIBB
    elif aod > 0.08 and eae > 1.13:
        return 3 #BB
    else:
        return 4 #MDM

def classify_methodI(data, aod_error=0.01, filter_aod=[False, 0.4]):
    if 'eae' not in data.columns:
        data['eae'] = calculate_eae(data['aod440'], data['aod870'])
    df = data[['aod440', 'aod870', 'eae']].dropna().reset_index(drop=True)
    if filter_aod[0]:
        df = df[df['aod440'] >= filter_aod[1]]
    outcome, df = run_classification(df, classification_functionI, 'aod440', 'eae',
                              method_id=1,
                              aod_error=aod_error)
    allowed_classes = METHOD_TO_CLASSES['Method I']
    outcome = outcome[outcome['type'].isin(allowed_classes) | (outcome["type"] == "TOTAL")]
    
    return outcome, df

# --------------------------
# Method II - AROD vs AOD (Chen et al., 2016)
# --------------------------
def classification_functionII(aod, arod):
    if aod <= 0.15 and arod > 0.31:
        return 1 #M
    elif aod > 0.15 and arod >= 0.81:
        return 5 #D
    elif aod > 0.5 and 0.39 < arod < 0.81:
        return 6 #SC
    elif aod > 0.5 and 0.25 <= arod <= 0.39:
        return 7 #UI
    elif aod > 0.5 and arod < 0.25:
        return 3 #BB
    else:
        return 8 #C

def classify_methodII(data, aod_error=0.01, filter_aod=[False, 0.4]):
    data['arod'] = calculate_arod(data['aod1020'], data['aod440'])
    df = data[['aod440','aod870', 'aod1020', 'arod', 'eae']].dropna().reset_index(drop=True)
    if filter_aod[0]:
        df = df[df['aod440'] >= filter_aod[1]]
    outcome, df = run_classification(df, classification_functionII, 'aod440', 'arod',
                              method_id=2,
                              aod_error=aod_error)
    allowed_classes = METHOD_TO_CLASSES['Method II']
    outcome = outcome[outcome['type'].isin(allowed_classes) | (outcome["type"] == "TOTAL")]
    
    return outcome, df


# --------------------------
# Method III - FMF vs AOD (Barnaba & Gobby, 2004)
# --------------------------
def classification_functionIII(aod, fmf):
    if aod < 0.3 and fmf < 0.8:
        return 1 #M 
    elif aod >= 0.3 and fmf < 0.7:
        return 5 #D 
    else:
        return 8 #C 

def classify_methodIII(data, aod_error=0.01, filter_aod=[False, 0.4]):
    df = data[['aod440', 'aod500', 'fmf500', 'rmse_fmf']].dropna().reset_index(drop=True)
    if filter_aod[0]:
        df = df[df['aod440'] >= filter_aod[1]]
    outcome, df = run_classification(df, classification_functionIII, 'aod500', 'fmf500',
                              method_id=3, 
                              aod_error=aod_error)
    allowed_classes = METHOD_TO_CLASSES['Method III']
    outcome = outcome[outcome['type'].isin(allowed_classes) | (outcome["type"] == "TOTAL")]
    
    return outcome, df


# --------------------------
# Method IVA - SSA vs EAE (Liu & Yi, 2022)
# --------------------------
def classification_functionIVA(ssa, eae):
    UI_cen, BB_cen = [1.3, 0.925], [1.3, 0.865]
    dist1, dist2 = compute_dist([eae, ssa], UI_cen), compute_dist([eae, ssa], BB_cen)
    if 0.88 <= ssa <= 0.96 and 0.1 <= eae <= 0.4:
        return 5  # D
    if 0.82 <= ssa <= 0.96 and 0.9 <= eae <= 1.7:
        return 7 if dist1 < dist2 else 3 #UI or BB
    return 9 #NC    

def classify_methodIVA(data, aod_error=0.01, ssa_error=0.03, filter_aod=[False, 0.4]):
    if 'eae' not in data.columns:
        data['eae'] = calculate_eae(data['aod440'], data['aod870'])
    df = data[['aod440', 'aod870', 'eae', 'ssa440']].dropna().reset_index(drop=True)
    if filter_aod[0]:
        df = df[df['aod440'] >= filter_aod[1]]
    outcome, df = run_classification(df, classification_functionIVA, 'ssa440', 'eae',
                              method_id=4, 
                              aod_error=aod_error, ssa_error=ssa_error)
    allowed_classes = METHOD_TO_CLASSES['Method IVA']
    outcome = outcome[outcome['type'].isin(allowed_classes) | (outcome["type"] == "TOTAL")]
 
    return outcome, df



# --------------------------
# Method IVB - SSA vs EAE (Zheng et al., 2021)
# --------------------------
def classification_functionIVB(ssa, eae):
    if ssa <= 0.85 and eae > 1.2:
        return 10 #StrAFP
    elif 0.85 < ssa < 0.9 and eae > 1.2:
        return 11 #MAFP
    elif 0.9 <= ssa < 0.95 and eae > 1.2:
        return 12 #SliAFP
    elif ssa >= 0.95 and eae > 1.2:
        return 13 #WAFP
    elif ssa < 0.95 and 0.6 < eae <= 1.2:
        return 14 #MAP
    elif ssa >= 0.95 and 0.6 < eae <= 1.2:
        return 15 #MWAP
    elif ssa < 0.95 and eae <= 0.6:
        return 16 #ACP
    if ssa >= 0.95 and eae <= 0.6:
        return 17 #WACP

def classify_methodIVB(data, aod_error=0.01, ssa_error=0.03, filter_aod=[False, 0.4]):
    if 'eae' not in data.columns:
        data['eae'] = calculate_eae(data['aod440'], data['aod870'])
    df = data[['aod440', 'aod870', 'eae', 'ssa440']].dropna().reset_index(drop=True)
    if filter_aod[0]:
        df = df[df['aod440'] >= filter_aod[1]]
    outcome, df = run_classification(df, classification_functionIVB, 'ssa440', 'eae',
                              method_id=5, 
                              aod_error=aod_error, ssa_error=ssa_error)
    allowed_classes = METHOD_TO_CLASSES['Method IVB']
    outcome = outcome[outcome['type'].isin(allowed_classes) | (outcome["type"] == "TOTAL")]
 
    return outcome, df



# --------------------------
# Method V - AAE vs EAE (Liu & Yi, 2022)
# --------------------------
def classification_functionV(aae, eae):
    UI_cen, BB_cen = [1.3, 0.925], [1.3, 0.865]
    dist1, dist2 = compute_dist([eae, aae], UI_cen), compute_dist([eae, aae], BB_cen)
    if 1 <= aae <= 3 and 0.01 <= eae <= 0.4:
        return 5 #D
    if 0.6 <= aae <= 2.3 and 0.8 <= eae <= 1.7:
        return 7 if dist1 < dist2 else 3 #UI or BB
    return 9 #NC

def classify_methodV(data, aod_error=0.01, ssa_error=0.03, filter_aod=[False, 0.4]):
    if 'eae' not in data.columns:
        data['eae'] = calculate_eae(data['aod440'], data['aod870'])
    data['aae'] = calculate_aae(data['aod440'], data['aod870'], data['ssa440'], data['ssa870'])
    df = data[['aod440', 'aod870', 'eae', 'ssa440', 'ssa870', 'aae']].dropna().reset_index(drop=True)
    if filter_aod[0]:
        df = df[df['aod440'] >= filter_aod[1]]
    outcome, df = run_classification(df, classification_functionV, 'aae', 'eae',
                              method_id=6,
                              aod_error=aod_error, ssa_error=ssa_error)
    allowed_classes = METHOD_TO_CLASSES['Method V']
    outcome = outcome[outcome['type'].isin(allowed_classes) | (outcome["type"] == "TOTAL")]
 
    return outcome, df



# --------------------------
# Method VI - RRI vs EAE (Liu & Yi, 2022)
# --------------------------
def classification_functionVI(rri, eae):
    if 1.44 <= rri <= 1.59 and 0.01 <= eae <= 0.41:
        return 5 #D
    elif 1.35 <= rri < 1.43 and 0.7 <= eae <= 1.74:
        return 7 #UI
    elif 1.43 <= rri <= 1.57 and 1 <= eae <= 1.5:
        return 3 #BB
    else:
        return 9 #NC

def classify_methodVI(data, aod_error=0.01, rri_error=0.04, filter_aod=[False, 0.4]):
    if 'eae' not in data.columns:
        data['eae'] = calculate_eae(data['aod440'], data['aod870'])
    df = data[['aod440', 'aod870', 'eae', 'rri440']].dropna().reset_index(drop=True)
    if filter_aod[0]:
        df = df[df['aod440'] >= filter_aod[1]]
    outcome, df = run_classification(df, classification_functionVI, 'rri440', 'eae',
                              method_id=7, 
                              aod_error=aod_error, rri_error=rri_error)
    allowed_classes = METHOD_TO_CLASSES['Method VI']
    outcome = outcome[outcome['type'].isin(allowed_classes) | (outcome["type"] == "TOTAL")]
 
    return outcome, df


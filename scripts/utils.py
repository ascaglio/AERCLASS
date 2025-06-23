 # utils.py

import numpy as np 
import pandas as pd 
import math

def excel_import(FILE):
    data = pd.read_excel(FILE) 
    return data

def propagate_uncertainties(method, df, aod_error, ssa_error, rri_error):
    LOG_RATIO = np.log(440 / 870)  # Precompute the constant log ratio
    LOG_DIFF = math.log10(870) - math.log10(440)
    aod_sob, aod_sub = df['aod440'] + aod_error, np.maximum(df['aod440'] - aod_error, 0)
    if 'eae' in df.columns:
        eae_error = np.abs(((1 / (df['aod870'] * LOG_RATIO)) + 
                    (1 / (df['aod440'] * LOG_RATIO))) * aod_error)
        eae_sob, eae_sub = df['eae'] + eae_error, np.maximum(df['eae'] - eae_error, 0)
    if method == 1:
        df['eae_error'] = eae_error
        df['eae_sob'], df['eae_sub'] = eae_sob, eae_sub
        df['aod_sob'], df['aod_sub'] = aod_sob, aod_sub
    elif method == 2:
        df['arod'] = df['aod1020']/df['aod440']
        arod_error = (aod_error / df['aod440']) + (aod_error * df['aod1020'] / df['aod440'] * df['aod440'])
        df['arod_sob'], df['arod_sub'] = df['arod'] + arod_error, np.maximum(df['arod'] - arod_error, 0)
        df['aod_sob'], df['aod_sub'] = aod_sob, aod_sub
    elif method == 3:
        df['fmf_sob'], df['fmf_sub'] = df['fmf500'] + df['rmse_fmf'], np.maximum(df['fmf500'] - df['rmse_fmf'], 0)
        df['aod500_sob'], df['aod500_sub'] = df['aod500'] + aod_error, np.maximum(df['aod500'] - aod_error, 0)
    elif method == 4:
        df['eae'] = eae_error
        df['eae_sob'], df['eae_sub'] = eae_sob, eae_sub
        df['ssa_sob'], df['ssa_sub'] = df['ssa440'] + ssa_error, np.maximum(df['ssa440'] - ssa_error, 0)
    elif method == 5:
        df['eae_error'] = eae_error
        df['eae_sob'], df['eae_sub'] = eae_sob, eae_sub
        df['aaod870'] = (1 - df['ssa870']) * df['aod870']    
        df['aaod440'] = (1 - df['ssa440']) * df['aod440']    
        df['aaod870'] = (1 - df['ssa870']) * df['aod870']
        df['aaod440'] = (1 - df['ssa440']) * df['aod440']
        df['aae'] = -((np.log10(df['aaod870']) - np.log10(df['aaod440'])) / LOG_DIFF)
        df['aaod870_error'], df['aaod440_error'] = df['aod870'] * ssa_error + abs(1 - df['ssa870']) * aod_error, df['aod440'] * ssa_error + abs(1 -
                                         df['ssa440']) * aod_error
        df['aae_error'] = (df['aaod870_error'] / (df['aaod870'] * LOG_DIFF)) + df['aaod440_error'] / (df['aaod440'] * LOG_DIFF)
        df['aae_sob'], df['aae_sub'] = df['aae'] + df['aae_error'], np.maximum(df['aae'] - df['aae_error'], 0)        
    elif method == 6:
        df['eae_error'] = eae_error
        df['eae_sob'], df['eae_sub'] = eae_sob, eae_sub
        df['rri_sob'], df['rri_sub'] = df['rri440'] + rri_error, np.maximum(df['rri440'] - rri_error, 0)
    return df

def compute_missclasification(df, data, aerosol_types):
# Identify misclassified cases
    df['misclassified'] = ~((df['class'] == df['class_00']) & (df['class'] 
                                                           == df['class_01']) &
                         (df['class'] == df['class_10']) & (df['class'] 
                                                            == df['class_11']))

# Count misclassifications per aerosol type
    classification_counts = df['class'].value_counts()
    misclassification_counts = df[df['misclassified']]['class'].value_counts()

# Compute classification metrics
    total_points = len(data)
    total_data = len(df)
    misclassification_rate = round(df['misclassified'].sum() * 100 / total_data, 1)
    availability = round(total_data * 100 / total_points, 1)

    output_data = []
    for i in range(1, len(aerosol_types)+1):
        count = classification_counts.get(i, 0)
        misclassified_count = misclassification_counts.get(i, 0)
        percentage = round(count * 100 / total_data, 1) if count else 0
        misclassification_percentage = round(misclassified_count * 100 / count, 1) if count else 0
        output_data.append((aerosol_types[i], percentage, misclassification_percentage))
    outcome = pd.DataFrame(output_data, columns=['Aerosol Type', '% in Classification', 'Misclassification Rate'])
    outcome.loc[len(outcome)] = ['Data Availability', availability, '']
    outcome.loc[len(outcome)] = ['Total Misclassification Rate', misclassification_rate, '']
    return outcome








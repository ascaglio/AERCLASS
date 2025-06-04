# classification method III, FMF VS AOD (Barnaba and Gobby, 2004)

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from .utils import compute_missclasification, propagate_uncertainties


# Define classification function

def classification_functionIII(aod,fmf):
    if aod < 0.3 and fmf < 0.8:
        return 1  # M
    elif aod >= 0.3 and fmf < 0.7:
        return 2  # D
    else:
        return 3  # C
    
def classify_methodIII(data, aod_error, filter_aod):
    aerosol_types = {1: 'M', 2: 'D', 3: 'C'}
    df = data[['aod440', 'aod500', 'fmf500', 'rmse_fmf']].dropna().reset_index(drop=True)
    if filter_aod[0] == True:
        df = df[df['aod440'] >= filter_aod[1]]
    df3= propagate_uncertainties(3, df, aod_error, 0, 0)      # Uncertainties propagation (if AOD, SSA or RRI are not used, then set them with 0)
    sub1 = df3['aod500_sub']
    sub2 = df3['fmf_sub']
    sob1 = df3['aod500_sob']
    sob2 = df3['fmf_sob']
    df3['class'] = [classification_functionIII(a, e) for a, e in zip(df3['aod500'], df3['fmf500'])]
    df3['class_00'] = [classification_functionIII(a, e) for a, e in zip(sub1, sub2)]
    df3['class_01'] = [classification_functionIII(a, e) for a, e in zip(sub1, sob2)]
    df3['class_10'] = [classification_functionIII(a, e) for a, e in zip(sob1, sub2)]
    df3['class_11'] = [classification_functionIII(a, e) for a, e in zip(sob1, sob2)]
    outcomeIII = compute_missclasification(df3, data, aerosol_types)
    return outcomeIII, df3

def distribution_plotIII(df, site, resolution, transparency, font_size):
    fig1, ax1 = plt.subplots(dpi=300)
    ax1.add_patch(patches.Rectangle((0, 0), 0.3, 0.8, edgecolor='blue', facecolor='blue', alpha=0.2, label='M'))
    ax1.add_patch(patches.Rectangle((0.3, 0), 3.4, 0.7, edgecolor='yellow', facecolor='yellow', alpha=0.4, label='D'))
    ax1.add_patch(patches.Polygon([[0, 0.8], [0, 1], [3, 1], [3, 0.7], [0.3, 0.7], [0.3, 0.8]], edgecolor='g', facecolor='g', alpha=0.2, label='C'))
    ax1.scatter(df['aod500'], df['fmf500'], color='white', edgecolor='k', alpha=transparency)
    ax1.legend(loc='upper right', bbox_to_anchor=(1.25, 1.2))
    ax1.set_xlabel(r'$AOD_{500}$', fontsize=font_size)
    ax1.set_ylabel(r'$FMF_{500}$', fontsize=font_size)
    ax1.set_title(f'{site} - FMF vs AOD (Barnaba and Gobby, 2004)', fontsize=font_size)
    plt.xlim(0, df['aod500'].max() + 0.1)
    plt.ylim(0, df['fmf500'].max() + 0.1)
    return ax1

def barplotIII(outcome,site, resolution, font_size):
    aerosol_types = {1: 'M', 2: 'D', 3: 'C'}
    fig2, ax2 = plt.subplots(dpi=resolution, layout='constrained')
    x = np.arange(len(aerosol_types))  # Label positions
    width = 0.3
    ax2.bar(x - width / 2, outcome['% in Classification'][:-2], width, label='% in Classification')
    ax2.bar(x + width / 2, outcome['Misclassification Rate'][:-2], width, label='Misclassification Rate')
    ax2.set_xticks(x, list(aerosol_types.values()), fontsize=font_size)
    ax2.set_ylabel('%', fontsize=font_size)
    ax2.set_title(f'{site} - Aerosol Classification: FMF vs AOD (Barnaba and Gobby, 2004)')
    ax2.legend()
    return ax2
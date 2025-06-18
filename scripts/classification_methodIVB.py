# classification method IVA,  SSA VS EAE (Zheng et al., 2021)

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from .utils import compute_missclasification, propagate_uncertainties


# Define classification function

def classification_functionIVB(ssa,eae):
    if ssa <= 0.85 and eae > 1.2:
             return 1  # StrAFP
    elif 0.85 <ssa< 0.9 and eae > 1.2:
             return 2  # MAFP
    elif 0.9 <= ssa < 0.95 and eae > 1.2:
             return 3  # SliAFP
    elif ssa >= 0.95 and eae > 1.2:
             return 4  # WAFP
    elif ssa < 0.95 and 0.6 < eae <= 1.2:
             return 5  # MAP
    elif ssa >= 0.95 and 0.6 < eae <= 1.2:
             return 6  # MWAP
    elif ssa < 0.95 and eae <= 0.6:
             return 7  # ACP
    if ssa >= 0.95 and eae <= 0.6:
             return 8  # WACP

def classify_methodIVB(data, aod_error, ssa_error, filter_aod):
    aerosol_types = {1: 'StrAFP', 2: 'MAFP', 3: 'SliAFP', 4: 'WAFP', 5: 'MAP', 6: 'MWAP', 7: 'ACP', 8: 'WACP'}
    if 'eae' not in data.columns:
        data['eae'] = np.log(data['aod870']/data['aod440'])/np.log(440/870)
    df = data[['aod440', 'aod870', 'eae', 'ssa440']].dropna().reset_index(drop=True)
    if filter_aod[0] == True:
        df = df[df['aod440'] >= filter_aod[1]]
    df4B= propagate_uncertainties(4, df, aod_error, ssa_error, 0)      # Uncertainties propagation (if AOD, SSA or RRI are not used, then set them with 0)
    sub1 = df4B['ssa_sub']
    sub2 = df4B['eae_sub']
    sob1 = df4B['ssa_sob']
    sob2 = df4B['eae_sob']
    df4B['class'] = [classification_functionIVB(a, e) for a, e in zip(df4B['ssa440'], df4B['eae'])]
    df4B['class_00'] = [classification_functionIVB(a, e) for a, e in zip(sub1, sub2)]
    df4B['class_01'] = [classification_functionIVB(a, e) for a, e in zip(sub1, sob2)]
    df4B['class_10'] = [classification_functionIVB(a, e) for a, e in zip(sob1, sub2)]
    df4B['class_11'] = [classification_functionIVB(a, e) for a, e in zip(sob1, sob2)]
    outcomeIVB = compute_missclasification(df4B, data, aerosol_types)
    return outcomeIVB, df4B

def distribution_plotIVB(df, site, resolution, transparency, font_size):
    fig1, ax1 = plt.subplots(dpi=300)
    patches_data = [
    (1.2, 0, max(df['eae'])-1.1, 0.87, 'k', 'StrAFP'),
    (1.2, 0.85, max(df['eae'])-1.1, 0.05, 'm', 'MAFP'),
    (1.2, 0.9, max(df['eae'])-1.1, 0.05, 'orange', 'SliAFP'),
    (1.2, 0.95, max(df['eae'])-1.1, max(df['ssa440'])-0.85, 'r', 'WAFP'),
    (0.6, 0, 0.6, 0.95, 'blueviolet', 'MAP'),
    (0.6, 0.95, 0.6, max(df['ssa440'])-0.85, 'darkolivegreen', 'MWAP'),
    (0, 0, 0.6, 0.95, 'yellow', 'ACP'),
    (0, 0.95, 0.6, max(df['ssa440'])-0.85, 'blue', 'WACP'),]
    for x, y, w, h, color, label in patches_data:
        ax1.add_patch(patches.Rectangle((x, y), w, h, linewidth=3, edgecolor=color, facecolor=color, alpha=0.2, label=label))
    ax1.scatter(df['eae'], df['ssa440'], color='white', edgecolor='k', alpha=0.7)
    ax1.legend(loc='upper right', bbox_to_anchor=(1.25, 1.2))
    ax1.set_xlabel(r'$EAE_{440/870}$', fontsize=14)
    ax1.set_ylabel(r'$SSA_{440}$', fontsize=14)
    ax1.set_title(f'{site} - SSA vs EAE (Zheng et al., 2020)', fontsize=14)
    plt.xlim(0, df['eae'].max() + 0.1)
    plt.ylim(0, df['ssa440'].max() + 0.1)
    return ax1

def barplotIVB(outcome,site, resolution, font_size):
    aerosol_types = {1: 'StrAFP', 2: 'MAFP', 3: 'SliAFP', 4: 'WAFP', 5: 'MAP', 6: 'MWAP', 7: 'ACP', 8: 'WACP'}
    fig2, ax2 = plt.subplots(dpi=resolution, layout='constrained')
    x = np.arange(len(aerosol_types))  # Label positions
    width = 0.3
    ax2.bar(x - width / 2, outcome['% in Classification'][:-2], width, label='% in Classification')
    ax2.bar(x + width / 2, outcome['Misclassification Rate'][:-2], width, label='Misclassification Rate')
    ax2.set_xticks(x, list(aerosol_types.values()), fontsize=font_size)
    ax2.set_ylabel('%', fontsize=font_size)
    ax2.set_title(f'{site} - Aerosol Classification: SSA vs EAE (Zheng et al., 2020)')
    ax2.legend()
    return ax2
# classification method IVA, SSA VS EAE (Liu and Yi, 2022)

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from .utils import compute_missclasification, propagate_uncertainties


# Define classification function

def classification_functionIVA(ssa,eae,dist1,dist2):
    if 0.88 <= ssa <= 0.96 and 0.1 <= eae <= 0.4:
        return 1  # D
    if 0.82 <= ssa <= 0.96 and 0.9 <= eae <= 1.7:
        return 2 if dist1 < dist2 else 3 # UI or BB
    return 4  # NC

def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def classify_methodIVA(data, aod_error, ssa_error):
    aerosol_types = {1: 'D', 2: 'UI', 3: 'BB', 4: 'NC'}
    df = data[['aod440', 'aod870', 'eae440_870', 'ssa440']].dropna().reset_index(drop=True)
    df4A= propagate_uncertainties(4, df, aod_error, ssa_error, 0)      # Uncertainties propagation (if AOD, SSA or RRI are not used, then set them with 0)
    sub1 = df4A['ssa_sub']
    sub2 = df4A['eae_sub']
    sob1 = df4A['ssa_sob']
    sob2 = df4A['eae_sob']
    UI_cen, BB_cen = [1.3, 0.925], [1.3, 0.865]
    dist1, dist2 = distance([df4A['eae440_870'], df4A['ssa440']], UI_cen), distance([df4A['eae440_870'], df4A['ssa440']], BB_cen)
    df4A['class'] = [classification_functionIVA(a, e, f, g) for a, e, f, g in zip(df4A['ssa440'], df4A['eae440_870'], dist1, dist2)]
    df4A['class_00'] = [classification_functionIVA(a, e, f, g) for a, e, f, g in zip(sub1, sub2, dist1, dist2)]
    df4A['class_01'] = [classification_functionIVA(a, e, f, g) for a, e, f, g in zip(sub1, sob2, dist1, dist2)]
    df4A['class_10'] = [classification_functionIVA(a, e, f, g) for a, e, f, g in zip(sob1, sub2, dist1, dist2)]
    df4A['class_11'] = [classification_functionIVA(a, e, f, g) for a, e, f, g in zip(sob1, sob2, dist1, dist2)]
    outcomeIVA = compute_missclasification(df4A, data, aerosol_types)
    return outcomeIVA, df4A

def distribution_plotIVA(df, site, resolution, transparency, font_size):
    fig1, ax1 = plt.subplots(dpi=300)
    patches_data = [
    (0.1, 0.88, 0.3, 0.08, 'yellow', 'D'),
    (0.9, 0.89, 0.8, 0.07, 'r', 'UI'),
    (0.9, 0.82, 0.8, 0.09, 'k', 'BB'),
    (0.1, 0.1, 0.01, 0.01, 'white', 'NC'),]
    for x, y, w, h, color, label in patches_data:
        ax1.add_patch(patches.Rectangle((x, y), w, h, linewidth=3, edgecolor=color, facecolor=color, alpha=0.2, label=label))
    ax1.scatter(df['eae440_870'], df['ssa440'], color='white', edgecolor='k', alpha=0.7)
    ax1.legend(loc='upper right', bbox_to_anchor=(1.25, 1.2))
    ax1.set_xlabel(r'$EAE_{440/870}$', fontsize=14)
    ax1.set_ylabel(r'$SSA_{440}$', fontsize=14)
    ax1.set_title(f'{site} - SSA vs EAE (Liu and Yi, 2022)', fontsize=14)
    plt.xlim(0, df['eae440_870'].max() + 0.1)
    plt.ylim(0, df['ssa440'].max() + 0.1)
    return ax1

def barplotIVA(outcome,site, resolution, font_size):
    aerosol_types = {1: 'D', 2: 'UI', 3: 'BB', 4: 'NC'}
    fig2, ax2 = plt.subplots(dpi=resolution, layout='constrained')
    x = np.arange(len(aerosol_types))  # Label positions
    width = 0.3
    ax2.bar(x - width / 2, outcome['% in Classification'][:-2], width, label='% in Classification')
    ax2.bar(x + width / 2, outcome['Misclassification Rate'][:-2], width, label='Misclassification Rate')
    ax2.set_xticks(x, list(aerosol_types.values()), fontsize=font_size)
    ax2.set_ylabel('%', fontsize=font_size)
    ax2.set_title(f'{site} - Aerosol Classification: SSA vs EAE (Liu and Yi, 2022)')
    ax2.legend()
    return ax2
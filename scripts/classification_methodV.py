# classification method V,  AAE VS EAE (Liu and Yi, 2022)

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from .utils import compute_missclasification, propagate_uncertainties


def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Define classification function

def classification_functionV(aae,eae,dist1,dist2):   
    if 1 <= aae <= 3 and 0.01 <= eae <= 0.4:
        return 1  # D
    if 0.6 <= aae <= 2.3 and 0.8 <= eae <= 1.7:
            return 2 if dist1 < dist2 else 3 #UI or BB
    return 4  # NC

def classify_methodV(data, aod_error, ssa_error, filter_aod):
    aerosol_types = {1: 'D', 2: 'UI', 3: 'BB', 4: 'NC'}
    if 'eae440_870' not in data.columns:
        data['eae440_870'] = np.log(data['aod870']/data['aod440'])/np.log(440/870)
    df = data[['aod440', 'aod870', 'ssa440', 'ssa870', 'eae440_870']].dropna().reset_index(drop=True)
    if filter_aod[0] == True:
        df = df[df['aod440'] >= filter_aod[1]]
    df5= propagate_uncertainties(5, df, aod_error, ssa_error, 0)      # Uncertainties propagation (if AOD, SSA or RRI are not used, then set them with 0)
    sub1 = df5['aae_sub']
    sub2 = df5['eae_sub']
    sob1 = df5['aae_sob']
    sob2 = df5['eae_sob']
    UI_cen, BB_cen = [1.3, 0.925], [1.3, 0.865]
    dist1, dist2 = distance([df5['eae440_870'], df5['aae']], UI_cen), distance([df5['eae440_870'], df5['aae']], BB_cen)
    df5['class'] = [classification_functionV(a, e, f, g) for a, e, f, g in zip(df5['aae'], df5['eae440_870'], dist1, dist2)]
    df5['class_00'] = [classification_functionV(a, e, f, g) for a, e, f, g in zip(sub1, sub2, dist1, dist2)]
    df5['class_01'] = [classification_functionV(a, e, f, g) for a, e, f, g in zip(sub1, sob2, dist1, dist2)]
    df5['class_10'] = [classification_functionV(a, e, f, g) for a, e, f, g in zip(sob1, sub2, dist1, dist2)]
    df5['class_11'] = [classification_functionV(a, e, f, g) for a, e, f, g in zip(sob1, sob2, dist1, dist2)]
    outcomeV = compute_missclasification(df5, data, aerosol_types)
    return outcomeV, df5

def distribution_plotV(df, site, resolution, transparency, font_size):
    fig1, ax1 = plt.subplots(dpi=300)
    patches_data = [
    (0.01, 1, 0.39, 2, 'yellow', 'D'),
    (0.8, 0.6, 0.8, 0.7, 'r', 'UI'),
    (0.8, 1.1, 0.9, 1.2, 'k', 'BB'),
    (0.1, 0.1, 0.01, 0.01, 'white', 'NC'),]
    for x, y, w, h, color, label in patches_data:
        ax1.add_patch(patches.Rectangle((x, y), w, h, linewidth=3, edgecolor=color, facecolor=color, alpha=0.2, label=label))
    ax1.scatter(df['eae440_870'], df['aae'], color='white', edgecolor='k', alpha=0.7)
    ax1.legend(loc='upper right', bbox_to_anchor=(1.25, 1.2))
    ax1.set_xlabel(r'$EAE_{440/870}$', fontsize=14)
    ax1.set_ylabel(r'$AAE_{870/440}$', fontsize=14)
    ax1.set_title(f'{site} - AAE vs EAE (Liu and Yi, 2022)', fontsize=14)
    plt.xlim(0, df['eae440_870'].max() + 0.1)
    plt.ylim(0, df['aae'].max() + 0.1)
    return ax1

def barplotV(outcome,site, resolution, font_size):
    aerosol_types = {1: 'D', 2: 'UI', 3: 'BB', 4: 'NC'}
    fig2, ax2 = plt.subplots(dpi=resolution, layout='constrained')
    x = np.arange(len(aerosol_types))  # Label positions
    width = 0.3
    ax2.bar(x - width / 2, outcome['% in Classification'][:-2], width, label='% in Classification')
    ax2.bar(x + width / 2, outcome['Misclassification Rate'][:-2], width, label='Misclassification Rate')
    ax2.set_xticks(x, list(aerosol_types.values()), fontsize=font_size)
    ax2.set_ylabel('%', fontsize=font_size)
    ax2.set_title(f'{site} - Aerosol Classification: AAE vs EAE (Liu and Yi, 2022)')
    ax2.legend()
    return ax2
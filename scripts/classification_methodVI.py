# classification method VI,  RRI VS EAE (Liu and Yi, 2022)

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from .utils import compute_missclasification, propagate_uncertainties

# Define classification function

def classification_functionVI(rri, eae):
    if 1.44 <= rri <= 1.59 and 0.01 <= eae <= 0.41:
        return 1  # D
    elif 1.35 <= rri < 1.43 and 0.7 <= eae <= 1.74:
        return 2  # UI
    elif 1.43 <= rri <= 1.57 and 1 <= eae <= 1.5:
        return 3  # BB
    else:
        return 4  # NC

def classify_methodVI(data, aod_error, rri_error, filter_aod):
    aerosol_types = {1: 'D', 2: 'UI', 3: 'BB', 4: 'NC'}
    if 'eae' not in data.columns:
        data['eae'] = np.log(data['aod870']/data['aod440'])/np.log(440/870)
    df = data[['aod440', 'aod870', 'eae', 'rri440']].dropna().reset_index(drop=True)
    if filter_aod[0] == True:
        df = df[df['aod440'] >= filter_aod[1]]
    df6 = propagate_uncertainties(6, df, aod_error, 0, rri_error)      # Uncertainties propagation (if AOD, SSA or RRI are not used, then set them with 0)
    sub1 = df6['rri_sub']
    sub2 = df6['eae_sub']
    sob1 = df6['rri_sob']
    sob2 = df6['eae_sob']
    df6['class'] = [classification_functionVI(a, e) for a, e in zip(df6['rri440'], df6['eae'])]
    df6['class_00'] = [classification_functionVI(a, e) for a, e in zip(sub1, sub2)]
    df6['class_01'] = [classification_functionVI(a, e) for a, e in zip(sub1, sob2)]
    df6['class_10'] = [classification_functionVI(a, e) for a, e in zip(sob1, sub2)]
    df6['class_11'] = [classification_functionVI(a, e) for a, e in zip(sob1, sob2)]
    outcomeVI = compute_missclasification(df6, data, aerosol_types)
    return outcomeVI, df6

def distribution_plotVI(df, site, resolution, transparency, font_size):
    fig1, ax1 = plt.subplots(dpi=300)
    patches_data = [
    (0.01, 1.44, 0.4, 0.15, 'yellow', 'D'),
    (0.7, 1.35, 1.04, 0.08, 'r', 'UI'),
    (1, 1.43, 0.5, 0.14, 'k', 'BB'),
    (0.1, 0.1, 0.01, 0.01, 'white', 'NC'),]
    for x, y, w, h, color, label in patches_data:
        ax1.add_patch(patches.Rectangle((x, y), w, h, linewidth=3, edgecolor=color, facecolor=color, alpha=0.2, label=label))
    ax1.scatter(df['eae'], df['rri440'], color='white', edgecolor='k', alpha=0.7)
    ax1.legend(loc='upper right', bbox_to_anchor=(1.25, 1.2))
    ax1.set_xlabel(r'$EAE_{870/440}$', fontsize=14)
    ax1.set_ylabel(r'$RRI_{440}$', fontsize=14)
    ax1.set_title(f'{site} - RRI vs EAE (Liu and Yi, 2022)', fontsize=14)
    plt.xlim(0, df['eae'].max() + 0.1)
    plt.ylim(0, df['rri440'].max() + 0.1)
    return ax1

def barplotVI(outcome,site, resolution, font_size):
    aerosol_types = {1: 'D', 2: 'UI', 3: 'BB', 4: 'NC'}
    fig2, ax2 = plt.subplots(dpi=resolution, layout='constrained')
    x = np.arange(len(aerosol_types))  # Label positions
    width = 0.3
    ax2.bar(x - width / 2, outcome['% in Classification'][:-2], width, label='% in Classification')
    ax2.bar(x + width / 2, outcome['Misclassification Rate'][:-2], width, label='Misclassification Rate')
    ax2.set_xticks(x, list(aerosol_types.values()), fontsize=font_size)
    ax2.set_ylabel('%', fontsize=font_size)
    ax2.set_title(f'{site} - Aerosol Classification: RRI vs EAE (Liu and Yi, 2022)')
    ax2.legend()
    return ax2

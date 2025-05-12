# classification method I, EAE VS AOD (Cuneo et al. 2022)

import matplotlib.pyplot as plt
import matplotlib.patches as patches 
import numpy as np 
from .utils import compute_missclasification, propagate_uncertainties


# Define classification function

def classification_functionI(aod,eae):
    if aod <= 0.08 and eae <= 1.13:
        return 1  # M
    elif aod <= 0.08 and eae > 1.13:
        return 2  # MUIBB
    elif aod > 0.08 and eae > 1.13:
        return 3  # BB
    else:
        return 4  # MDM
    
def classify_methodI(data, aod_error):
    aerosol_types = {1: 'M', 2: 'MUIBB', 3: 'BB', 4: 'MDM'}
    df = data[['aod440', 'aod870', 'eae440_870']].dropna().reset_index(drop=True)
    df1= propagate_uncertainties(1, df, aod_error, 0, 0)      # Uncertainties propagation (if AOD, SSA or RRI are not used, then set them with 0)
    sub1 = df['aod_sub']
    sub2 = df['eae_sub']
    sob1 = df['aod_sob']
    sob2 = df['eae_sob']
    df1['class'] = [classification_functionI(a, e) for a, e in zip(df1['aod440'], df1['eae440_870'])]
    df1['class_00'] = [classification_functionI(a, e) for a, e in zip(sub1, sub2)]
    df1['class_01'] = [classification_functionI(a, e) for a, e in zip(sub1, sob2)]
    df1['class_10'] = [classification_functionI(a, e) for a, e in zip(sob1, sub2)]
    df1['class_11'] = [classification_functionI(a, e) for a, e in zip(sob1, sob2)]
    outcomeI = compute_missclasification(df1, data, aerosol_types)
    return outcomeI, df1

def distribution_plotI(df, site, resolution, transparency, font_size):
    fig1, ax1 = plt.subplots(dpi=300)
    patches_data = [
        (0, 0, 0.08, 1.13, 'blue', 'M'),
        (0.08, 0, 3.62, 1.13, 'grey', 'MDM'),
        (0, 1.13, 0.08, 1.87, 'brown', 'MUIBB'),
        (0.08, 1.13, 3.62, 1.87, 'black', 'BB'),
    ]
    for x, y, w, h, color, label in patches_data:
        ax1.add_patch(patches.Rectangle((x, y), w, h, linewidth=3, edgecolor=color, facecolor=color, alpha=0.2, label=label))
    ax1.scatter(df['aod440'], df['eae440_870'], color='white', edgecolor='k', alpha=transparency)
    ax1.legend(loc='upper right', bbox_to_anchor=(1.25, 1.2))
    ax1.set_xlabel(r'$AOD_{440}$', fontsize=font_size)
    ax1.set_ylabel(r'$EAE_{870/440}$', fontsize=font_size)
    ax1.set_title(f'{site} - EAE vs AOD (Cúneo et al., 2022)', fontsize=font_size)
    plt.xlim(0, df['aod440'].max() + 0.1)
    plt.ylim(0, df['eae440_870'].max() + 0.1)
    return ax1

def barplotI(outcome,site, resolution, font_size):
    aerosol_types = {1: 'M', 2: 'MUIBB', 3: 'BB', 4: 'MDM'}
    fig2, ax2 = plt.subplots(dpi=resolution, layout='constrained')
    x = np.arange(len(aerosol_types))  # Label positions
    width = 0.3
    ax2.bar(x - width / 2, outcome['% in Classification'][:-2], width, label='% in Classification')
    ax2.bar(x + width / 2, outcome['Misclassification Rate'][:-2], width, label='Misclassification Rate')
    ax2.set_xticks(x, list(aerosol_types.values()), fontsize=font_size)
    ax2.set_ylabel('%', fontsize=font_size)
    ax2.set_title(f'{site} - Aerosol Classification: EAE vs AOD (Cúneo et al., 2022)')
    ax2.legend()
    return ax2
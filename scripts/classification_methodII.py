#classification method II, AROD vs AOD (Chen et al., 2016)

# Libraries
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from .utils import compute_missclasification, propagate_uncertainties


# Define classification function
def classification_functionII(aod,arod):
    if aod <= 0.15 and arod > 0.31:
        return 1 #M
    elif aod > 0.15 and arod >= 0.81:
        return 2 #D
    elif aod > 0.5 and 0.39 < arod < 0.81:
        return 3 #SC
    elif aod > 0.5 and 0.25 <= arod <= 0.39:
        return 4 #UI
    elif aod > 0.5 and arod < 0.25:
        return 5 #BB
    else:
        return 6 #C
    
def classify_methodII(data, aod_error):
    aerosol_types = {1: 'M', 2: 'D', 3: 'SC', 4: 'UI', 5: 'BB', 6: 'C'}
    df = data[['aod440', 'aod870', 'aod1020', 'eae440_870']].dropna().reset_index(drop=True)
    df2= propagate_uncertainties(2, df, aod_error, 0, 0)      # Uncertainties propagation (if AOD, SSA or RRI are not used, then set them with 0)
    sub1 = df2['aod_sub']
    sub2 = df2['arod_sub']
    sob1 = df2['aod_sob']
    sob2 = df2['arod_sob']
    df2['class'] = [classification_functionII(a, e) for a, e in zip(df2['aod440'], df2['arod'])]
    df2['class_00'] = [classification_functionII(a, e) for a, e in zip(sub1, sub2)]
    df2['class_01'] = [classification_functionII(a, e) for a, e in zip(sub1, sob2)]
    df2['class_10'] = [classification_functionII(a, e) for a, e in zip(sob1, sub2)]
    df2['class_11'] = [classification_functionII(a, e) for a, e in zip(sob1, sob2)]
    outcomeII = compute_missclasification(df2, data, aerosol_types)
    return outcomeII, df2

def distribution_plotII(df, site, resolution, transparency, font_size):
    fig1, ax1 = plt.subplots(dpi=300)
    patches_data = [
    (0, 0.31, 0.15, 0.69, 'blue', 'M'),
    (0.15, 0.81, 3.55, 0.19, 'yellow', 'D'),
    (0.5, 0.39, 3.2, 0.42, 'orange', 'SC'),
    (0.5, 0.25, 3.2, 0.14, 'r', 'UI'),
    (0.5, 0, 3.2, 0.25, 'k', 'BB'),]
    path = [[0, 0], [0, .31], [.15, .31],[.15,.81],[.5,.81],[.5,0]]
    for x, y, w, h, color, label in patches_data:
        ax1.add_patch(patches.Rectangle((x, y), w, h, linewidth=3, edgecolor=color, facecolor=color, alpha=0.2, label=label))
    ax1.add_patch(patches.Polygon(path, linewidth=5, edgecolor = 'g', facecolor = 'g', fill = True,alpha=0.2,label='C'))
    ax1.scatter(df['aod440'], df['arod'], color='white', edgecolor='k', alpha=transparency)
    ax1.legend(loc='upper right', bbox_to_anchor=(1.25, 1.2))
    ax1.set_xlabel(r'$AOD_{440}$', fontsize=14)
    ax1.set_ylabel(r'$AROD_{1020/440}$', fontsize=14)
    ax1.set_xlim(0, df['aod440'].max() + 0.1)
    ax1.set_ylim(0, df['arod'].max())
    ax1.set_title(f'{site} - AROD vs AOD (Chen et al., 2016)', fontsize=14)
    return ax1

def barplotII(outcome,site, resolution, font_size):
    aerosol_types = {1: 'M', 2: 'D', 3: 'SC', 4: 'UI', 5: 'BB', 6: 'C'}
    fig2, ax2 = plt.subplots(dpi=resolution, layout='constrained')
    x = np.arange(len(aerosol_types))  # Label positions
    width = 0.3
    ax2.bar(x - width / 2, outcome['% in Classification'][:-2], width, label='% in Classification')
    ax2.bar(x + width / 2, outcome['Misclassification Rate'][:-2], width, label='Misclassification Rate')
    ax2.set_xticks(x, list(aerosol_types.values()), fontsize=font_size)
    ax2.set_ylabel('%', fontsize=font_size)
    ax2.set_title(f'{site} - Aerosol Classification: AOD vs AROD (Chen et al., 2016)')
    ax2.legend()
    return ax2
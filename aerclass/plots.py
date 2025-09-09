# plots.py - Centralized plotting functions for AERCLASS

import matplotlib.pyplot as plt
import seaborn as sns
from aerclass.utils import CLASS_NUMERIC_TO_CODE, METHOD_TO_CLASSES, AEROSOL_STYLES


def distribution_plot(df, method_name, site, xvar, yvar, dpi=300, alpha=0.8, fontsize=14, classvar='class_code'):
    """
    Generates a scatter plot showing classified data points in a 2D feature space.
    """
    
    allowed_classes = METHOD_TO_CLASSES.get(method_name, [])
    plot_df = df[df[classvar].isin(allowed_classes)]
    palette = {code: AEROSOL_STYLES[code]['color'] for code in allowed_classes}
    
    plt.figure(dpi=dpi)
    ax = sns.scatterplot(data=plot_df, x=xvar, y=yvar,
                         hue=classvar, palette=palette,
                         alpha=alpha, edgecolor='k')
    ax.set_title(f"{method_name} - {site}", fontsize=fontsize)
    ax.set_xlabel(xvar, fontsize=fontsize)
    ax.set_ylabel(yvar, fontsize=fontsize)
    ax.legend(title='Class', fontsize=fontsize*0.8, title_fontsize=fontsize*0.9, loc='best')
    plt.xticks(fontsize=fontsize*0.8)
    plt.yticks(fontsize=fontsize*0.8)
    plt.tight_layout()
    return ax

def barplot(outcome_df, method_name, site, dpi=300, fontsize=14):
    """
    Generates a bar plot of misclassification rates per aerosol type.

    """
    allowed_classes = METHOD_TO_CLASSES.get(method_name, [])
    plot_df = outcome_df[outcome_df['type'].isin(allowed_classes)]
    palette = {code: AEROSOL_STYLES[code]['color'] for code in allowed_classes}

    plt.figure(dpi=dpi)
    ax = sns.barplot(
        x='type', y='misclassification_rate',
        data=plot_df, palette=palette, edgecolor='k'
    )
    ax.set_title(f"Misclassification Rates - {method_name} - {site}", fontsize=fontsize)
    ax.set_xlabel('Aerosol Type', fontsize=fontsize)
    ax.set_ylabel('Misclassification Rate (%)', fontsize=fontsize)
    plt.xticks(rotation=45, ha='right', fontsize=fontsize*0.8)
    plt.yticks(fontsize=fontsize*0.8)
    plt.tight_layout()
    return ax

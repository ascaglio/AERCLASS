# plots.py - Centralized plotting functions for AERCLASS

import matplotlib.pyplot as plt
import seaborn as sns


def distribution_plot(df, method_name, site, xvar, yvar, classvar='class', dpi=300, alpha=0.7, fontsize=14):
    """
    Generates a scatter plot showing classified data points in a 2D feature space.
    """
    plt.figure(dpi=dpi)
    ax = sns.scatterplot(data=df, x=xvar, y=yvar, hue=classvar, palette='tab10', alpha=alpha, edgecolor=None)
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
    plt.figure(dpi=dpi)
    ax = sns.barplot(x='type', y='misclassification_rate', data=outcome_df, palette='Set2')
    ax.set_title(f"Misclassification Rates - {method_name} - {site}", fontsize=fontsize)
    ax.set_xlabel('Aerosol Type', fontsize=fontsize)
    ax.set_ylabel('Misclassification Rate (%)', fontsize=fontsize)
    plt.xticks(rotation=45, ha='right', fontsize=fontsize*0.8)
    plt.yticks(fontsize=fontsize*0.8)
    plt.tight_layout()
    return ax

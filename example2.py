# example.py - Minimal usage example of AERCLASS using Method I

# Import necessary modules
import pandas as pd
import matplotlib.pyplot as plt

# Import classification and plotting functions
from aerclass.classify import classify_methodI
from aerclass.plots import distribution_plot, barplot

# --------------------
# STEP 1: Load aerosol data
# --------------------
# Input file must contain AOD at 440 and 870 nm, or EAE will be auto-calculated.
FILE = 'alta_floresta_daily.xlsx'
SITE = 'Alta Floresta'

data = pd.read_excel(FILE)

# --------------------
# STEP 2: Define parameters
# --------------------
# AOD error is set to 0.01 by default, based on AERONET uncertainty (Giles et al., 2019)
AOD_ERROR = 0.01
FILTER_AOD = [True, 0.4]  # exclude values with AOD < 0.4 (optional)

# --------------------
# STEP 3: Run classification (Method I: EAE vs AOD)
# --------------------
outcome, df = classify_methodI(data, aod_error=AOD_ERROR, filter_aod=FILTER_AOD)

# --------------------
# STEP 4: Visualize results
# --------------------
# Distribution plot: classified data points in AOD vs EAE space
dist_ax = distribution_plot(df, 'Method I', SITE, xvar='aod440', yvar='eae440_870')

# Bar plot: misclassification rate per aerosol type
bar_ax = barplot(outcome, 'Method I', SITE)

# Show plots
plt.show()

# --------------------
# STEP 5: Save results (optional)
# --------------------
df.to_csv('methodI_classified_data.csv', index=False)
outcome.to_csv('methodI_misclassification_summary.csv', index=False)
print("Results saved.")

# IMPORT LIBRARIES
from aerclass.classification_methodI import * 
from aerclass.classification_methodII import * 
from aerclass.classification_methodIII import * 
from aerclass.classification_methodIVA import * 
from aerclass.classification_methodIVB import * 
from aerclass.classification_methodV import * 
from aerclass.classification_methodVI import * 
import pandas as pd

# SET DATA AND PARAMETERS
FILE = "solarvillage_daily.xlsx"   # Set file path and name (e.g. '...alta_floresta_daily.xlsx')
aod_error = 0.01                    # Set AOD error (0.01 by default)
ssa_error = 0.03                    # Set SSA error (0.03 by default)    
rri_error = 0.04                    # Set RRI error (0.04 by default)
SITE = 'Solar Village'              # Set site name
data = pd.read_excel(FILE)          # Organize data into a dataframe

# CALL TO CLASSIFICATION METHODS
outcomeI, dfI = classify_methodI(data, aod_error)                      # Outcome from classification method I
outcomeII, dfII = classify_methodII(data, aod_error)                   # Outcome from classification method II
outcomeIII, dfIII = classify_methodIII(data, aod_error)                # Outcome from classification method III
outcomeIVA, dfIVA = classify_methodIVA(data, aod_error, ssa_error)     # Outcome from classification method IV
outcomeIVB, dfIVB = classify_methodIVB(data, aod_error, ssa_error)     # Outcome from classification method V
outcomeV, dfV = classify_methodV(data, aod_error, ssa_error)           # Outcome from classification method VI
outcomeVI, dfVI = classify_methodVI(data, aod_error, rri_error)        # Outcome from classification method VII

# PLOTS
distI = distribution_plotI(dfI,SITE,300,0.7,14)            # Plot of distribution with the classification method I
barI = barplotI(outcomeI,SITE,300,14)                      # Barplot of percentages with the classification method I
distII = distribution_plotII(dfII,SITE,300,0.7,14)         # Plot of distribution with the classification method II
barII = barplotII(outcomeII,SITE,300,14)                   # Barplot of percentages with the classification method II
distIII = distribution_plotIII(dfIII,SITE,300,0.7,14)      # Plot of distribution with the classification method III
barIII = barplotIII(outcomeIII,SITE,300,14)                # Barplot of percentages with the classification method III
distIVA = distribution_plotIVA(dfIVA,SITE,300,0.7,14)      # Plot of distribution with the classification method IVA
barIVA = barplotIVA(outcomeIVA,SITE,300,14)                # Barplot of percentages with the classification method IVA
distIVB = distribution_plotIVB(dfIVB,SITE,300,0.7,14)      # Plot of distribution with the classification method IVB
barIVB = barplotIVB(outcomeIVB,SITE,300,14)                # Barplot of percentages with the classification method IVB
distV = distribution_plotV(dfV,SITE,300,0.7,14)            # Plot of distribution with the classification method V
barV = barplotV(outcomeV,SITE,300,14)                      # Barplot of percentages with the classification method V
distVI = distribution_plotVI(dfVI,SITE,300,0.7,14)         # Plot of distribution with the classification method VI
barVI = barplotVI(outcomeVI,SITE,300,14)                   # Barplot of percentages with the classification method VI

outcomeI.to_excel(f'{SITE}_MI.xlsx', index=False)
outcomeII.to_excel(f'{SITE}_MII.xlsx', index=False)
outcomeIII.to_excel(f'{SITE}_MIII.xlsx', index=False)
outcomeIVA.to_excel(f'{SITE}_MIVA.xlsx', index=False)
outcomeIVB.to_excel(f'{SITE}_MIVB.xlsx', index=False)
outcomeV.to_excel(f'{SITE}_MV.xlsx', index=False)
outcomeVI.to_excel(f'{SITE}_MVI.xlsx', index=False)



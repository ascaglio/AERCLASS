# IMPORT LIBRARIES
from scripts.classification_methodI import * 
from scripts.classification_methodII import * 
from scripts.classification_methodIII import * 
from scripts.classification_methodIVA import * 
from scripts.classification_methodIVB import * 
from scripts.classification_methodV import * 
from scripts.classification_methodVI import * 
import pandas as pd
from openpyxl import load_workbook
from openpyxl import Workbook
import numpy as np


# SET DATA AND PARAMETERS
FILE = "solarvillage_daily.xlsx"   # Set file path and name (e.g. '...alta_floresta_daily.xlsx')
aod_error = 0.01                    # Set AOD error (0.01 by default)
ssa_error = 0.03                    # Set SSA error (0.03 by default)    
rri_error = 0.04                    # Set RRI error (0.04 by default)
SITE = 'Solar Village'              # Set site name
data = pd.read_excel(FILE)          # Organize data into a dataframe
filter_aod = [False,0.4]             # Exclude aod<0.4 if filter_aod[0] = True 

methodIb = pd.DataFrame(columns= ['M','MUIBB','BB','MDM','TMR'])
methodIIb = pd.DataFrame(columns= ['M', 'D','SC','UI','BB','C','TMR'])
methodIIIb = pd.DataFrame(columns= ['M','D','C','TMR'])
methodIVAb = pd.DataFrame(columns= ['D','UI','BB','NC','TMR'])
methodIVBb = pd.DataFrame(columns= ['StrAFP', 'MAFP', 'SliAFP', 'WAFP', 'MAP', 'MWAP', 'ACP', 'WACP','TMR'])
methodVb = pd.DataFrame(columns= ['D','UI','BB','NC','TMR'])
methodVIb = pd.DataFrame(columns= ['D','UI','BB','NC','TMR'])
indice = 0
lista = []

for i in range(0,45,5):
    ssa_error = i/1000
    # CALL TO CLASSIFICATION METHODS
    outcomeIb, dfI = classify_methodI(data, aod_error, filter_aod)                      # Outcome from classification method I
    outcomeIIb, dfII = classify_methodII(data, aod_error, filter_aod)                   # Outcome from classification method II
    outcomeIIIb, dfIII = classify_methodIII(data, aod_error, filter_aod)                # Outcome from classification method III
    outcomeIVAb, dfIVA = classify_methodIVA(data, aod_error, ssa_error, filter_aod)     # Outcome from classification method IV
    outcomeIVBb, dfIVB = classify_methodIVB(data, aod_error, ssa_error, filter_aod)     # Outcome from classification method V
    outcomeVb, dfV = classify_methodV(data, aod_error, ssa_error, filter_aod)           # Outcome from classification method VI
    outcomeVIb, dfVI = classify_methodVI(data, aod_error, rri_error, filter_aod)        # Outcome from classification method VII
    outcomeIb['Misclassification Rate'][len(outcomeIb)-2] =outcomeIb['% in Classification'][len(outcomeIb)-1]
    methodIb.loc[indice] = outcomeIb['Misclassification Rate'][0:len(outcomeIb)-1].tolist()
    outcomeIIb['Misclassification Rate'][len(outcomeIIb)-2] =outcomeIIb['% in Classification'][len(outcomeIIb)-1]
    methodIIb.loc[indice] = outcomeIIb['Misclassification Rate'][0:len(outcomeIIb)-1].tolist()
    outcomeIIIb['Misclassification Rate'][len(outcomeIIIb)-2] =outcomeIIIb['% in Classification'][len(outcomeIIIb)-1]
    methodIIIb.loc[indice] = outcomeIIIb['Misclassification Rate'][0:len(outcomeIIIb)-1].tolist()
    outcomeIVAb['Misclassification Rate'][len(outcomeIVAb)-2] =outcomeIVAb['% in Classification'][len(outcomeIVAb)-1]
    methodIVAb.loc[indice] = outcomeIVAb['Misclassification Rate'][0:len(outcomeIVAb)-1].tolist()
    outcomeIVBb['Misclassification Rate'][len(outcomeIVBb)-2] =outcomeIVBb['% in Classification'][len(outcomeIVBb)-1]
    methodIVBb.loc[indice] = outcomeIVBb['Misclassification Rate'][0:len(outcomeIVBb)-1].tolist()
    outcomeVb['Misclassification Rate'][len(outcomeVb)-2] =outcomeVb['% in Classification'][len(outcomeVb)-1]
    methodVb.loc[indice] = outcomeVb['Misclassification Rate'][0:len(outcomeVb)-1].tolist()
    outcomeVIb['Misclassification Rate'][len(outcomeVIb)-2] =outcomeVIb['% in Classification'][len(outcomeVIb)-1]
    methodVIb.loc[indice] = outcomeVIb['Misclassification Rate'][0:len(outcomeVIb)-1].tolist()
    lista.append(aod_error)
    indice = indice + 1

methodIb['ssa_error'] = lista
methodIIb['ssa_error'] = lista
methodIIIb['ssa_error'] = lista
methodIVAb['ssa_error'] = lista
methodIVBb['ssa_error'] = lista
methodVb['ssa_error'] = lista
methodVIb['ssa_error'] = lista
methodIb.drop(0, axis=0, inplace=True)
methodIIb.drop(0, axis=0, inplace=True)
methodIIIb.drop(0, axis=0, inplace=True)
methodIVAb.drop(0, axis=0, inplace=True)
methodIVBb.drop(0, axis=0, inplace=True)
methodVb.drop(0, axis=0, inplace=True)
methodVIb.drop(0, axis=0, inplace=True)

methodI_mean = (methodI + methodIb)/2
methodI_rmse = abs((methodI - methodIb)/2)
methodII_mean = (methodII + methodIIb)/2
methodII_rmse = abs((methodII - methodIIb)/2)
methodIII_mean = (methodIII + methodIIIb)/2
methodIII_rmse = abs((methodIII - methodIIIb)/2)
methodIVA_mean = (methodIVA + methodIVBb)/2
methodIVA_rmse = abs((methodIVA - methodIVAb)/2)
methodIVB_mean = (methodIVB + methodIVBb)/2
methodIVB_rmse = abs((methodIVB - methodIVBb)/2)
methodV_mean = (methodV + methodVb)/2
methodV_rmse = abs((methodV - methodVb)/2)
methodVI_mean = (methodVI + methodVIb)/2
methodVI_rmse = abs((methodVI - methodVIb)/2)


fig3, ax3 = plt.subplots(dpi=300, layout='constrained')
labels = ['M','MUIBB','BB','MDM']
plt.plot(methodI['aod_error'],methodI_mean['M'])
plt.plot(methodI['aod_error'],methodI_mean['MUIBB'])
plt.plot(methodI['aod_error'],methodI_mean['BB'])
plt.plot(methodI['aod_error'],methodI_mean['MDM'])
plt.fill_between(methodI['aod_error'],methodI_mean['M']+methodI_rmse['M'],methodI['M']-methodI_rmse['M'],alpha=0.3)
plt.fill_between(methodI['aod_error'],methodI_mean['MUIBB']+methodI_rmse['MUIBB'],methodI['MUIBB']-methodI_rmse['MUIBB'],alpha=0.3)
plt.fill_between(methodI['aod_error'],methodI_mean['BB']+methodI_rmse['BB'],methodI['BB']-methodI_rmse['BB'],alpha=0.3)
plt.fill_between(methodI['aod_error'],methodI_mean['MDM']+methodI_rmse['MDM'],methodI['MDM']-methodI_rmse['MDM'],alpha=0.3)
plt.legend(labels)
plt.ylim([0,101])
plt.xlabel('AOD error')
plt.ylabel('Mean MR(%)')

fig4,ax4 = plt.subplots(dpi=300, layout = 'constrained')
plt.plot(methodI['aod_error'],methodI['TMR'],linewidth=4)
plt.plot(methodII['aod_error'],methodII_mean['TMR'],linewidth=4)
plt.plot(methodIII['aod_error'],methodIII_mean['TMR'],linewidth=4)
plt.plot(methodIVA['aod_error'],methodIVA_mean['TMR'],linewidth=4)
plt.plot(methodIVB['aod_error'],methodIVB_mean['TMR'],linewidth=4)
plt.plot(methodV['aod_error'],methodV_mean['TMR'],linewidth=4)
plt.plot(methodVI['aod_error'],methodVI_mean['TMR'],linewidth=4)
plt.fill_between(methodI['aod_error'],methodI['TMR']+methodI_rmse['TMR'],methodI['TMR']-methodI_rmse['TMR'],alpha=0.3)
plt.fill_between(methodII_mean['aod_error'],methodII_mean['TMR']+methodII_rmse['TMR'],methodII['TMR']-methodII_rmse['TMR'],alpha=0.3)
plt.fill_between(methodIII_mean['aod_error'],methodIII_mean['TMR']+methodIII_rmse['TMR'],methodIII_mean['TMR']-methodIII_rmse['TMR'],alpha=0.3)
plt.fill_between(methodIVA_mean['aod_error'],methodIVA_mean['TMR']+methodIVA_rmse['TMR'],methodIVA_mean['TMR']-methodIVA_rmse['TMR'],alpha=0.3)
plt.fill_between(methodIVB_mean['aod_error'],methodIVB_mean['TMR']+methodIVB_rmse['TMR'],methodIVB_mean['TMR']-methodIVB_rmse['TMR'],alpha=0.3)
plt.fill_between(methodV_mean['aod_error'],methodV_mean['TMR']+methodV_rmse['TMR'],methodV_mean['TMR']-methodV_rmse['TMR'],alpha=0.3)
plt.fill_between(methodVI_mean['aod_error'],methodVI_mean['TMR']+methodVI_rmse['TMR'],methodVI_mean['TMR']-methodVI_rmse['TMR'],alpha=0.3)
labels = ['Method I', 'Method II', 'Method III', 'Method IVA', 'Method IVB', 'Method V', 'Method VI']
plt.ylim([0,101])
plt.legend(labels)

'''
j = 0
iteracion = []
libro = Workbook()
libro.save(f'{SITE}_MI.xlsx')
libro.save(f'{SITE}_MII.xlsx')
libro.save(f'{SITE}_MIII.xlsx')
libro.save(f'{SITE}_MIVA.xlsx')
libro.save(f'{SITE}_MIVB.xlsx')
libro.save(f'{SITE}_MV.xlsx')
libro.save(f'{SITE}_MVI.xlsx')
    with pd.ExcelWriter(f'{SITE}_MI.xlsx', engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
        outcomeI.to_excel(writer, sheet_name=f'aod_{aod_error}', index=False)
    with pd.ExcelWriter(f'{SITE}_MII.xlsx', engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
        outcomeII.to_excel(writer, sheet_name=f'aod_{aod_error}', index=False)
    with pd.ExcelWriter(f'{SITE}_MII.xlsx', engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
        outcomeIII.to_excel(writer, sheet_name=f'aod_{aod_error}', index=False)        
    with pd.ExcelWriter(f'{SITE}_MIVA.xlsx', engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
        outcomeIVA.to_excel(writer, sheet_name=f'aod_{aod_error}', index=False)    
    with pd.ExcelWriter(f'{SITE}_MIVB.xlsx', engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
        outcomeIVB.to_excel(writer, sheet_name=f'aod_{aod_error}', index=False)
    with pd.ExcelWriter(f'{SITE}_MV.xlsx', engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
        outcomeV.to_excel(writer, sheet_name=f'aod_{aod_error}', index=False)
    with pd.ExcelWriter(f'{SITE}_MVI.xlsx', engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
        outcomeVI.to_excel(writer, sheet_name=f'aod_{aod_error}', index=False)

'''

'''
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
    '''


    
    
    
'''    
outcomeI.to_excel(f'{SITE}_MI.xlsx', index=False)
outcomeII.to_excel(f'{SITE}_MII.xlsx', index=False)
outcomeIII.to_excel(f'{SITE}_MIII.xlsx', index=False)
outcomeIVA.to_excel(f'{SITE}_MIVA.xlsx', index=False)
outcomeIVB.to_excel(f'{SITE}_MIVB.xlsx', index=False)
outcomeV.to_excel(f'{SITE}_MV.xlsx', index=False)
outcomeVI.to_excel(f'{SITE}_MVI.xlsx', index=False)
'''


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


# SET DATA AND PARAMETERS
FILE = "alta_floresta_daily.xlsx"   # Set file path and name (e.g. '...alta_floresta_daily.xlsx')
aod_error = 0.01                    # Set AOD error (0.01 by default)
ssa_error = 0.03                    # Set SSA error (0.03 by default)    
rri_error = 0.04                    # Set RRI error (0.04 by default)
SITE = 'Alta Floresta'              # Set site name
data = pd.read_excel(FILE)          # Organize data into a dataframe
filter_aod = [False,0.4]             # Exclude aod<0.4 if filter_aod[0] = True 

methodI = pd.DataFrame(columns= ['M','MUIBB','BB','MDM','TMR'])
methodII = pd.DataFrame(columns= ['M', 'D','SC','UI','BB','C','TMR'])
methodIII = pd.DataFrame(columns= ['M','D','C','TMR'])
methodIVA = pd.DataFrame(columns= ['D','UI','BB','NC','TMR'])
methodIVB = pd.DataFrame(columns= ['StrAFP', 'MAFP', 'SliAFP', 'WAFP', 'MAP', 'MWAP', 'ACP', 'WACP','TMR'])
methodV = pd.DataFrame(columns= ['D','UI','BB','NC','TMR'])
methodVI = pd.DataFrame(columns= ['D','UI','BB','NC','TMR'])
indice = 0
lista = []

for i in range(0,45,5):
    aod_error = i/1000
    # CALL TO CLASSIFICATION METHODS
    outcomeI, dfI = classify_methodI(data, aod_error, filter_aod)                      # Outcome from classification method I
    outcomeII, dfII = classify_methodII(data, aod_error, filter_aod)                   # Outcome from classification method II
    outcomeIII, dfIII = classify_methodIII(data, aod_error, filter_aod)                # Outcome from classification method III
    outcomeIVA, dfIVA = classify_methodIVA(data, aod_error, ssa_error, filter_aod)     # Outcome from classification method IV
    outcomeIVB, dfIVB = classify_methodIVB(data, aod_error, ssa_error, filter_aod)     # Outcome from classification method V
    outcomeV, dfV = classify_methodV(data, aod_error, ssa_error, filter_aod)           # Outcome from classification method VI
    outcomeVI, dfVI = classify_methodVI(data, aod_error, rri_error, filter_aod)        # Outcome from classification method VII
    outcomeI['Misclassification Rate'][len(outcomeI)-2] =outcomeI['% in Classification'][len(outcomeI)-1]
    methodI.loc[indice] = outcomeI['Misclassification Rate'][0:len(outcomeI)-1].tolist()
    outcomeII['Misclassification Rate'][len(outcomeII)-2] =outcomeII['% in Classification'][len(outcomeII)-1]
    methodII.loc[indice] = outcomeII['Misclassification Rate'][0:len(outcomeII)-1].tolist()
    outcomeIII['Misclassification Rate'][len(outcomeIII)-2] =outcomeIII['% in Classification'][len(outcomeIII)-1]
    methodIII.loc[indice] = outcomeIII['Misclassification Rate'][0:len(outcomeIII)-1].tolist()
    outcomeIVA['Misclassification Rate'][len(outcomeIVA)-2] =outcomeIVA['% in Classification'][len(outcomeIVA)-1]
    methodIVA.loc[indice] = outcomeIVA['Misclassification Rate'][0:len(outcomeIVA)-1].tolist()
    outcomeIVB['Misclassification Rate'][len(outcomeIVB)-2] =outcomeIVB['% in Classification'][len(outcomeIVB)-1]
    methodIVB.loc[indice] = outcomeIVB['Misclassification Rate'][0:len(outcomeIVB)-1].tolist()
    outcomeV['Misclassification Rate'][len(outcomeV)-2] =outcomeV['% in Classification'][len(outcomeV)-1]
    methodV.loc[indice] = outcomeV['Misclassification Rate'][0:len(outcomeV)-1].tolist()
    outcomeVI['Misclassification Rate'][len(outcomeVI)-2] =outcomeVI['% in Classification'][len(outcomeVI)-1]
    methodVI.loc[indice] = outcomeVI['Misclassification Rate'][0:len(outcomeVI)-1].tolist()
    lista.append(aod_error)
    indice = indice + 1

methodI['aod_error'] = lista
methodII['aod_error'] = lista
methodIII['aod_error'] = lista
methodIVA['aod_error'] = lista
methodIVB['aod_error'] = lista
methodV['aod_error'] = lista
methodVI['aod_error'] = lista
methodI.drop(0, axis=0, inplace=True)
methodII.drop(0, axis=0, inplace=True)
methodIII.drop(0, axis=0, inplace=True)
methodIVA.drop(0, axis=0, inplace=True)
methodIVB.drop(0, axis=0, inplace=True)
methodV.drop(0, axis=0, inplace=True)
methodVI.drop(0, axis=0, inplace=True)

labels = ['M','MUIBB','BB','MDM','TMR']
plt.plot(methodI['aod_error'],methodI['M'])
plt.scatter(methodI['aod_error'],methodI['M'])
plt.plot(methodI['aod_error'],methodI['MUIBB'])
plt.scatter(methodI['aod_error'],methodI['MUIBB'])
plt.plot(methodI['aod_error'],methodI['BB'])
plt.scatter(methodI['aod_error'],methodI['BB'])
plt.plot(methodI['aod_error'],methodI['MDM'])
plt.plot(methodI['aod_error'],methodI['TMR'],color='k',linewidth=4)
plt.legend(labels)
plt.xlabel('AOD error')
plt.ylabel('MR(%)')



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


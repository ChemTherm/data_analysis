import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta


### Read GC Data fom Excel ####

molar_volume_stp = 22.414

# Molare Massen der Gase in g/mol
molar_masses = {
    'H2': 2.016,      'O2': 32.00,          'N2': 28.02,            'CO': 28.01,       'Methan': 16.04,       'Ethan': 30.07,
    'Ethen': 28.05,   'Ethin': 26.04,       'Propan': 44.10,        'Propen': 42.08,   'n-Butan': 58.12,      'Isobutan': 58.12,
    '1-Buten': 56.11, 'Cis-2-Buten': 56.11, 'Trans-2-Buten': 56.11, 'Isobuten': 56.11, '1,3-Butadien': 54.09, 'Benzol': 78.11
}

# Funktion zur Umrechnung von Volumenprozent in Massenprozent für alle Gase im DataFrame
def convert_df_volumetric_to_mass_percent(df):
    # Berechnung der Dichten unter Standardbedingungen für jedes Gas
    densities_stp = {gas: molar_masses[gas] / molar_volume_stp for gas in molar_masses}
    # Iteriere über jede Zeile des DataFrames
    for index, row in df.iterrows():
        total_density_stp = sum(densities_stp[gas] * row[gas] / 100 for gas in df.columns[2:len(columns_names)])  # Gesamtdichte des Gases unter Standardbedingungen     
        if total_density_stp == 0:
                   continue    
        # Konvertierung der Volumenprozente in Massenprozente für jedes Gas
        for gas in df.columns[2:len(columns_names)]:  # Spalten 2 bis zum Ende, um 'time' zu überspringen
            mass_percent  = (densities_stp[gas] * row[gas] / 100) / total_density_stp * 100
            df.at[index, f'w_{gas}'] = mass_percent
    return df


data_GC = pd.read_excel("UNISTUTT.xls", header=8)

columns_names = ['time','time2','H2', 'O2', 'N2', 'CO', 'Methan', 'Ethan', 'Ethen', 'Ethin',
               'Propan', 'Propen', 'n-Butan', 'Isobutan', '1-Buten', 'Cis-2-Buten',
               'Trans-2-Buten', 'Isobuten', '1,3-Butadien', 'Benzol']

for i in range(len(columns_names)):
    data_GC.rename(columns={data_GC.columns[i]: columns_names[i]}, inplace=True)

data_GC = pd.DataFrame(data_GC)
data_GC['Summe'] = data_GC.iloc[:, 2:len(columns_names)].sum(axis=1)
data_GC = convert_df_volumetric_to_mass_percent(data_GC)


# Read GC Data from DATA intermediate.txt




# Summe über alle Spalten für jede Zeile berechnen (Spalten 2 bis Ende)
""" for col in data_GC.columns[2:len(columns_names)]:
    data_GC[col] = data_GC[col].astype(float) """


print(data_GC.iloc[91])
 
# Ausgabe des Ergebnisses
output_file = 'ergebnisse.xlsx'
data_GC.to_excel(output_file, index=False)

cm2zoll = 0.393701
sns.set_style('whitegrid') # Verwende den "darkgrid"-Stil von Seaborn
sns.set_palette('colorblind') # Verwende eine farbenblinde Farbpalette
plt.rcParams.update({'font.size': 14}) # Setze die Schriftgröße auf 14
plt.rcParams['font.family'] = 'Garamond' 

fig, ax = plt.subplots(figsize=(25*cm2zoll, 9*cm2zoll)) # Erstelle eine Figur mit 8 x 6 Zoll
ax.plot(data_GC['time'], data_GC['Ethen'], '.')
ax.plot(data_GC['time'], data_GC['Summe'], '.')
# plt.xlim([0, 1550])
#plt.ylim([700, 1020]) 
plt.xlabel('Datum')
plt.tight_layout()
#plt.savefig(filename +"_Temperaturverlauf.png",format = 'png') 
plt.show() 




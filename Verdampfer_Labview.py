import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

filename = "Verdampfer_Labview_results/VX-001/VX-001_Messung1_03042023_Anlage.txt"
filename = "Verdampfer_Labview_results/VX-001/VX-001_Messung2_04042023_Anlage.txt"
filename = "Verdampfer_Labview_results/VX-001/VX-001_Messung1_05042023_Anlage.txt"
filename = "Verdampfer_Labview_results/VX-001/VX-001_Messung2_06042023_Anlage.txt"
#filename = "Verdampfer_Labview_results/VX-001/VX-001_Messung3_06042023_Anlage.txt"

with open(filename, 'r') as file:
    headers = file.readline().strip().split('\t') # Lese die Überschriften aus der ersten Zeile
    data = {}
    for header in headers:
        data[header] = [] # Erstelle eine leere Liste für jede Überschrift

    for line in file:
        values = line.strip().split('\t')
        for i in range(len(headers)):
            value = float(values[i].replace(',', '.'))
            data[headers[i]].append(value) # Füge den Wert zur entsprechenden Liste hinzu
# Werte umrechnen
data['Druck1'] = [ value*1000 / 10 *4 for value in data['Druck1']]
data['Druck2'] = [ value*1000 / 10 *9 for value in data['Druck2']]

# Nach Abschnitten aufteilen
prev_value = None
change_indices = []
for i, value in enumerate(data['Zeile']):
    if prev_value is not None and value != prev_value:
        change_indices.append(i)
    prev_value = value


x = data['t_mess']
y = data['Druck1']

sns.set_style('whitegrid') # Verwende den "darkgrid"-Stil von Seaborn
sns.set_palette('colorblind') # Verwende eine farbenblinde Farbpalette
plt.rcParams.update({'font.size': 14}) # Setze die Schriftgröße auf 14
plt.rcParams['font.family'] = 'Garamond' 
fig, ax = plt.subplots(figsize=(8, 6)) # Erstelle eine Figur mit 8 x 6 Zoll

ax.plot(x, y,'-', linewidth = 2)

plt.xlabel('Zeit / s')
plt.ylabel('Druck1 / mbar')
#plt.show()

x_vars = []
y_vars = []
T_vars = []
mean_Abschnitte = []
std_Abschnitte = []
var_Abschnitte = []
for i in range(len(change_indices)-1):
    bereich = int((change_indices[i+1]-change_indices[i])/2) # Letzte 50%
    bereich = int((change_indices[i+1]-change_indices[i])) # Alle
    x = data['t_mess'][change_indices[i+1]-bereich:change_indices[i+1]]
    y = data['Druck1'][change_indices[i+1]-bereich:change_indices[i+1]]
    T = data['T_Verdampfer'][change_indices[i+1]-bereich:change_indices[i+1]]
    mean_Abschnitte.append(np.mean(y))
    std_Abschnitte.append(np.std(y))
    var_Abschnitte.append(np.var(y))
    x_vars.append(x)
    y_vars.append(y)
    T_vars.append(T)

# Plote alle neuen x- und y-Variablen
fig2, ax2 = plt.subplots(figsize=(8, 6))
fig3, ax3 = plt.subplots(figsize=(8, 6))
for i in range(len(x_vars)):
    ax2.plot(x_vars[i], y_vars[i]-mean_Abschnitte[i], label=f'Bereich {i+1}')
    ax3.plot(x_vars[i], T_vars[i], label=f'Bereich {i+1}')
#ax.legend()
ax2.set_xlabel('Zeit [s]')
ax2.set_ylabel('Druck [Pa]')
for i in range(len(mean_Abschnitte)):
    x_position = float(1/len(mean_Abschnitte) * float(i+1))
    print(x_position)
    ax2.text(x_position, 0.95, f'MW: {mean_Abschnitte[i]:.2f}', ha='right', va='top', transform=ax.transAxes)
    ax2.text(x_position, 0.9, f'std: {std_Abschnitte[i]:.2f}', ha='right', va='top', transform=ax.transAxes)
    ax2.text(x_position, 0.85, f'var: {var_Abschnitte[i]:.2f}', ha='right', va='top', transform=ax.transAxes)


plt.show()
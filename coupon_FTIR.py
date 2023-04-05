import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

with open("Coupon_FTIR_results/20230403_Decoking_SteamTreatment_28_16_run1.prn", 'r') as FTIR_file:
    headers = FTIR_file.readline().strip().split('\t') # Lese die Überschriften aus der ersten Zeile
    data = {}
    for header in headers:
        data[header] = [] # Erstelle eine leere Liste für jede Überschrift

    for line in FTIR_file:
        values = line.strip().split('\t')
        for i in range(len(headers)):
            if '.' in values[i]:
                try:
                    date = datetime.strptime(values[i], '%d.%m.%Y') # Versuche, das Datum zu parsen
                    data[headers[i]].append(date.date()) # Füge das Datum als date-Objekt hinzu
                except ValueError:
                    data[headers[i]].append(np.nan) # Wenn das Datum ungültig ist, füge nan hinzu
            elif  ':' in values[i]:
                try:
                    time = datetime.strptime(values[i], '%H:%M:%S,%f').time() # Versuche, die Uhrzeit zu parsen
                    data[headers[i]].append(time) # Füge die Uhrzeit als time-Objekt hinzu
                except ValueError:
                    data[headers[i]].append(np.nan) # Wenn die Uhrzeit ungültig ist, füge nan hinzu
            

            elif values[i] == 'N/A':
                data[headers[i]].append(np.nan) # Ersetze 'N/A' durch nan
            else:
                value = float(values[i].replace(',', '.'))
                data[headers[i]].append(value) # Füge den Wert zur entsprechenden Liste hinzu
times = data['Time']
first_time = times[0]
dt_run1 = 550
time_diffs = [datetime.combine(datetime.min, t) - datetime.combine(datetime.min, first_time) for t in times]
time_diff_seconds = [(td.total_seconds() + td.microseconds / 1000000 - dt_run1) for td in time_diffs] # Konvertiere timedelta-Objekte in Sekunden
data['runTime'] = time_diff_seconds

# Hier ist ein Beispiel, wie man eine Spalte gegen eine andere aufträgt
x1 = data['runTime']
y1_1 = data['CO% (1) 191C (2of3)']
y1_2 = data['CO (500) 191C (1of3)']
y_CO2_1 = data['CO2% (20) 191C (1of2) R4']

with open("Coupon_FTIR_results/20230403_Decoking_SteamTreatment_28_16_run2.prn", 'r') as FTIR_file:
    headers = FTIR_file.readline().strip().split('\t') # Lese die Überschriften aus der ersten Zeile
    data = {}
    for header in headers:
        data[header] = [] # Erstelle eine leere Liste für jede Überschrift

    for line in FTIR_file:
        values = line.strip().split('\t')
        for i in range(len(headers)):
            if '.' in values[i]:
                try:
                    date = datetime.strptime(values[i], '%d.%m.%Y') # Versuche, das Datum zu parsen
                    data[headers[i]].append(date.date()) # Füge das Datum als date-Objekt hinzu
                except ValueError:
                    data[headers[i]].append(np.nan) # Wenn das Datum ungültig ist, füge nan hinzu
            elif  ':' in values[i]:
                try:
                    time = datetime.strptime(values[i], '%H:%M:%S,%f').time() # Versuche, die Uhrzeit zu parsen
                    data[headers[i]].append(time) # Füge die Uhrzeit als time-Objekt hinzu
                except ValueError:
                    data[headers[i]].append(np.nan) # Wenn die Uhrzeit ungültig ist, füge nan hinzu
            

            elif values[i] == 'N/A':
                data[headers[i]].append(np.nan) # Ersetze 'N/A' durch nan
            else:
                value = float(values[i].replace(',', '.'))
                data[headers[i]].append(value) # Füge den Wert zur entsprechenden Liste hinzu
times = data['Time']
first_time = times[0]
time_diffs = [datetime.combine(datetime.min, t) - datetime.combine(datetime.min, first_time) for t in times]
time_diff_seconds = [(td.total_seconds() + td.microseconds / 1000000) for td in time_diffs] # Konvertiere timedelta-Objekte in Sekunden
data['runTime'] = time_diff_seconds
x2 = data['runTime']
y2_1 = data['CO% (1) 191C (2of3)']
y2_2 = data['CO (500) 191C (1of3)']
y_CO2_2 = data['CO2% (20) 191C (1of2) R4']





sns.set_style('whitegrid') # Verwende den "darkgrid"-Stil von Seaborn
sns.set_palette('colorblind') # Verwende eine farbenblinde Farbpalette
plt.rcParams.update({'font.size': 14}) # Setze die Schriftgröße auf 14
plt.rcParams['font.family'] = 'Garamond' 
fig, ax = plt.subplots(figsize=(8, 6)) # Erstelle eine Figur mit 8 x 6 Zoll
ax.plot(x1, y1_1, x2, y2_1,'-', linewidth = 2)
plt.xlim([0, 4000])
plt.xlabel('Zeit / s')
plt.ylabel('Konzentration')
fig2, ax2 = plt.subplots(figsize=(8, 6)) # Erstelle eine Figur mit 8 x 6 Zoll
ax2.plot(x1, y1_2, x2, y2_2,'-', linewidth = 2)
plt.xlim([0, 4000])
plt.xlabel('Zeit / s')
plt.ylabel('Konzentration')
fig3, ax3 = plt.subplots(figsize=(8, 6)) # Erstelle eine Figur mit 8 x 6 Zoll
ax3.plot(x1, y_CO2_1, x2, y_CO2_2,'-', linewidth = 2)
plt.xlim([0, 4000])
plt.ylim([0,20])
plt.xlabel('Zeit / s')
plt.ylabel('Konzentration')
plt.show()
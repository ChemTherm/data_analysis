import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

filename = "Verdampfer_Labview_results/VX-001/VX-001_Messung1_05042023_Anlage.txt"

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
data['Druck2'] = [ value*1000 / 10 *10 for value in data['Druck2']]



root = tk.Tk()


fig, ax = plt.subplots(1,1,1)
x = data['t_mess']
y = data['Druck2']
ax.plot(x, y,'-', linewidth = 2)
canvas_plot = FigureCanvasTkAgg(fig, root)
canvas_plot.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

root.mainloop()
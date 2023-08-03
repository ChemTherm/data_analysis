import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from datetime import datetime, timedelta


def read_intermediate(file_path):
    table1_lines = []
    table2_lines = []
    table3_lines = []
    skip_lines = True

    with open(file_path, 'r') as f:
        reading_table1 = False
        reading_table2 = False
        reading_table3 = False
        for line in f:
            if "Method: UNI STUTTGART.M last changed 03.08.2023" in line:
                skip_lines = False
            elif skip_lines:
                if line.startswith('Creation Date:'):
                    creation_date = line.strip().split(": ")[1]
                continue
            line = line.strip()
            
            if not line:
                continue  # Ignore empty lines

            if line.startswith('Signal:'):
                if line == 'Signal: FID2B':
                    reading_table1 = True
                    reading_table2 = False
                    reading_table3 = False
                elif line == 'Signal: TCD1A':
                    reading_table1 = False
                    reading_table2 = True
                    reading_table3 = False
             
            if line.startswith('RetTime'):
                    reading_table1 = False
                    reading_table2 = False
                    reading_table3 = True
            elif line.startswith('-----'): # Zeile überspringen
                continue 
            elif reading_table1:
                table1_lines.append(line)
            elif reading_table2:
                table2_lines.append(line)
            elif reading_table3:
                table3_lines.append(line)

    return table1_lines, table2_lines, table3_lines, creation_date

def parse_table3_lines(table3_lines):
    data_dict = {}
    headers = ['RetTime', 'Type', 'CalibPeakType', 'Signalname', 'Amount', 'Compound']

    for header in headers:
        data_dict[header] = []

    for line in table3_lines:
        # Trenne die Werte in der Zeile durch Leerzeichen oder Tabulatoren
        values = line.split()

        # Füge die Werte in das entsprechende Dictionary ein
        for i, header in enumerate(headers):
            if i == 5:  # Spalte "Compound"
                if values[1] == 'Unknown':
                    data_dict[header].append('Unknown')
                else:
                    data_dict[header].append(values[i+2])
            else:
                if i < len(values):
                    data_dict[header].append(values[i])
                else:
                    data_dict[header].append('')

    return data_dict

def extract_creation_date_and_ethen_rettime(file_path):
    table1_lines, table2_lines, table3_lines, creation_date_str   = read_intermediate(file_path)
    table3_data_dict = parse_table3_lines(table3_lines)

    ethen_rettime = None
    for compound, rettime in zip(table3_data_dict['Compound'], table3_data_dict['RetTime']):
        if compound.strip() == 'Ethen':
            ethen_rettime = rettime
            break
        if compound.strip() == 'Unknown':
            ret_time = float(rettime)
            if 2.9 <= ret_time <= 3.1:
                ethen_rettime = ret_time                
                break

    date_str = file_path.split(os.path.sep)[-2]

    creation_date_str = f"{date_str[:8]}_{date_str[9:13]}"
    creation_date = datetime.strptime(creation_date_str, '%Y%m%d_%H%M')

    return creation_date, ethen_rettime
    
def read_txt_files_in_subfolders(folder_path):
    txt_file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('intermediate.txt'):
                txt_file_paths.append(os.path.join(root, file))
    return txt_file_paths


if __name__ == "__main__":

    folder_path = 'D:/ChemTherm/ChemTherm - Coupon-Projekt/Experimente/GC_Data/'
    txt_files = read_txt_files_in_subfolders(folder_path)
    creation_date, ethen_rettime = extract_creation_date_and_ethen_rettime("D:/ChemTherm/ChemTherm - Coupon-Projekt/Experimente/GC_Data/20230712/20230712_1359_P01.D/intermediate.txt")
    
    data_dict = {}
    for txt_file in txt_files:
        print(txt_file)
        creation_date, ethen_rettime = extract_creation_date_and_ethen_rettime(txt_file)
        data_dict[txt_file] = { 'Date':creation_date, 'Ethen':ethen_rettime  }



"""     print("Tabelle 1:")
    for line in table1_lines:
        print(line)

    print("\nTabelle 2:")
    for line in table2_lines:
        print(line)

    print("\nTabelle 3:")
    for line in table3_lines:
        print(line) """

  # Ausgabe des Dictionarys
"""     print("Tabelle 3 als Dictionary:")
    for header, values in table3_data_dict.items():
        print(f"{header}: {values}")  """

        

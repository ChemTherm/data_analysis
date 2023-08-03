from googlesearch import search
from urllib.parse import urlparse
import pandas as pd

def parse_google_search_result(search_result_string):
    # Finde die Start- und Endpositionen der URL und extrahiere sie
    url_start = search_result_string.find("url=") + 4
    url_end = search_result_string.find(",", url_start)
    url = search_result_string[url_start:url_end]

    # Finde die Start- und Endpositionen des Titels und extrahiere ihn
    title_start = search_result_string.find("title=") + 6
    title_end = search_result_string.find(",", title_start)
    title = search_result_string[title_start:title_end]

    # Finde die Start- und Endpositionen der Beschreibung und extrahiere sie
    description_start = search_result_string.find("description=") + 12
    description_end = search_result_string.rfind(")")
    description = search_result_string[description_start:description_end]

    return {
        'url': url.strip("\"'"),
        'title': title.strip("\"'"),
        'description': description.strip("\"'")
    }

def read_search_queries_from_excel(file_path, sheet_name):
    # Lese die Daten aus der Excel-Datei in ein DataFrame ein
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df

def create_excel_file(file_path):
    # Erzeuge ein leeres DataFrame mit den gewünschten Spaltennamen
    df = pd.DataFrame(columns=['Suchbegriffe', 'Priorität', '1.Ergebnis', '2.Ergebnis', '3.Ergebnis','Nr. ChemTherm','Nr. ICVT','Nr. Parteq','Nr. Brokhorst','Nr. Wagner'])

    # Speichere das DataFrame in einer Excel-Datei
    df.to_excel(file_path, index=False)

def get_domain_name(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme +"://" + parsed_url.hostname

def write_results_to_excel(file_path, df):

    for idx, row in df.iterrows():
        query = row['Suchbegriffe']
        results = search(query, num_results=50, advanced=True)
        result_dict = [parse_google_search_result(str(url)) for url in results]
        df.at[idx, '1.Ergebnis'] = get_domain_name(result_dict[0]['url'])
        df.at[idx, '2.Ergebnis'] = get_domain_name(result_dict[1]['url'])
        df.at[idx, '3.Ergebnis'] = get_domain_name(result_dict[2]['url'])
        for result in result_dict:
            if "chem-therm.de" in result['url']:
                df.at[idx, 'Nr. ChemTherm'] = idx
            if "icvt.uni-stuttgart.de" in result['url']:
                df.at[idx, 'Nr. ICVT'] = idx
            if "parteq.net" in result['url']:
                df.at[idx, 'Nr. Parteq'] = idx
            if "bronkhorst.com" in result['url']:
                df.at[idx, 'Nr. Brokhorst'] = idx
            if "wagner-msr.de" in result['url']:
                df.at[idx, 'Nr. Wagner'] = idx


    df.to_excel(file_path, index=False)


if __name__ == "__main__":
    # Pfad zur Excel-Datei
    file_path = 'Google Suchanfragen_Test.xlsx'
    sheet_name = 'Sheet1'

    # Lese die Suchanfragen aus der Excel-Datei
    df = read_search_queries_from_excel(file_path, sheet_name)

     # Schreibe die Ergebnisse in die Excel-Datei
    write_results_to_excel('Google SuchErgebnisse.xlsx', df)


import pandas as pd
import requests
from bs4 import BeautifulSoup

# 1. Leer el CSV con las URLs de las compañías
df_urls = pd.read_csv('orgs_paginas.csv')  # Asegúrate de que el CSV tenga una columna 'url'

# Lista para almacenar los resultados de cada URL
resultados = []

# Encabezados para la petición (para simular un navegador real)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# 2. Iterar sobre cada URL y realizar el scraping
for index, row in df_urls.iterrows():
    url = row['url']  # Ajusta el nombre de la columna según tu CSV
    print("Procesando URL:", url)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar todos los <p> con style="text-align: left;"
        p_tags = soup.find_all('p', style="text-align: left;")
        fechas_y_lugares = []
        
        for p in p_tags:
            # Extraer el contenido del <p> separando con saltos de línea
            contenido = p.get_text(separator="\n", strip=True)
            lineas = contenido.splitlines()
            # Filtrar líneas que contienen fechas y lugares
            for linea in lineas:
                if linea.strip() == "2025":
                    continue
                if linea.strip().startswith("–"):
                    fechas_y_lugares.append(linea.strip())
                    
        # Unir las líneas en un solo string
        info = "\n".join(fechas_y_lugares)
    except Exception as e:
        info = f"Error al procesar: {str(e)}"
    
    resultados.append({
        'url': url,
        'fechas_y_lugares': info
    })

# 3. Crear un DataFrame con los resultados
df_resultados = pd.DataFrame(resultados)

# 4. Guardar el DataFrame en un archivo Excel
excel_file = "resultados.xlsx"
df_resultados.to_excel(excel_file, index=False)
print(f"Los resultados se han guardado en '{excel_file}'.")

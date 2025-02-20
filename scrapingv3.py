import pandas as pd
import requests
from bs4 import BeautifulSoup

# 1. Leer el CSV
df_urls = pd.read_csv('orgs_paginas.csv', engine='python', on_bad_lines='skip')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

resultados = []

for index, row in df_urls.iterrows():
    
    url = row['pagina_eventos']

    # Verificar que no sea NaN ni "NULL"
    if pd.isna(url) or str(url).strip() == 'NULL':
        continue  

    print(f"Procesando URL: {url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

      
        p_tags = soup.find_all('p', style="text-align: left;")

        fechas_y_lugares = []
        for p in p_tags:
            contenido = p.get_text(separator="\n", strip=True)
            lineas = contenido.splitlines()
            for linea in lineas:
                
                if linea.strip() == "2025":
                    continue
                if linea.strip().startswith("–"):
                    fechas_y_lugares.append(linea.strip())

        
        info = "\n".join(fechas_y_lugares)

    except Exception as e:
        info = f"Error al procesar {url}: {str(e)}"

    
    resultados.append({
        'id': row['id'],
        'nombre_comercial': row['nombre_comercial'],
        'url_eventos': url,
        'fechas_y_lugares': info
    })

# 2. Crear un DataFrame con los resultados
df_resultados = pd.DataFrame(resultados)

# 3. Guardar el DataFrame en un archivo Excel
excel_file = "resultados.xlsx"
df_resultados.to_excel(excel_file, index=False)
print(f"Los resultados se han guardado en '{excel_file}'.")

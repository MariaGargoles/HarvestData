
import requests
from bs4 import BeautifulSoup
import json


with open("../data/compañias.json", "r", encoding="utf-8") as f:
    data = json.load(f)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

results = []

for compania in data["compañias"]:
    
    nombre = compania["nombre"]
    url = compania["url"]

    # Filtrar URLs no válidas
    if not url or url.startswith("/") or "NO" in url.upper() or "MANTENIMIENTO" in url.upper():
        print(f"URL no válida o en mantenimiento: {nombre} - {url}")
        continue  

    print(f"Procesando URL: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        
        p_tags = soup.find_all('p')

        dates_and_places = []
        for p in p_tags:
            content = p.get_text(separator="\n", strip=True)
            lineas = content.splitlines()
            for linea in lineas:
                if "2025" in linea or any(word in linea.lower() for word in ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                                                                             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]):
                    dates_and_places.append(linea.strip())

        info = "\n".join(dates_and_places) if dates_and_places else "No se encontraron fechas."

    except Exception as e:
        info = f"Error al procesar {url}: {str(e)}"

    results.append({
        'nombre_comercial': nombre,
        'url_eventos': url,
        'dates_and_places': info
    })


json_file = "resultsv3.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print(f"Los resultados se han guardado en '{json_file}'.")

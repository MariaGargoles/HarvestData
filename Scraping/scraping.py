
import openai
import os
import requests
import json
from bs4 import BeautifulSoup

openai.api_key = os.environ.get("OPENAI_API_KEY")

def obtain_html(url: str) -> str:
    """
    Función que obtiene el HTML de una URL.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error al obtener {url}: {e}")
        return None

def obtain_data(html: str) -> dict:
    """
    Usa OpenAI para obtener datos de un HTML.
    """
    prompt = ("Analiza el siguiente HTML y extrae información sobre eventos:\n\n"
        f"{html}\n\n"
        "Si hay eventos, devuélvelos en el siguiente formato JSON:\n"
        "{\n"
        "  \"events\": [\n"
        "    {\"nombre\": \"Nombre del evento\", \"fecha\": \"Fecha\", \"lugar\": \"Lugar\"}\n"
        "  ]\n"
        "}\n\n"
        "Si no hay eventos pero hay enlaces a páginas con eventos, devuélvelos en este formato:\n"
        "{\n"
        "  \"links\": [\"https://ejemplo.com/eventos\", \"https://ejemplo.com/agenda\"]\n"
        "}\n\n"
        "Si no hay información relevante, devuelve un JSON vacío {}."
    )
    try:
        response = openai.Completion.create(
            model="gpt-4o",
            messages=[{"role":"user", "content": prompt}],
            max_tokens=500
        )
        return json.loads(response["choices"][0]["message"]["content"])
    except Exception as e:
        print(f"Error al analizar el HTML con OpenAI: {e}")
        return {}
    
    
    
def search_url(compania_url):
    """
    Busca eventos en la página de la compañía o enlaces a más eventos.
    """
    html = obtain_html(compania_url)
    if not html:
        print(f"No se pudo obtener el HTML de {compania_url}")
        return

    parsed_content = obtain_data(html)

    if "events" in parsed_content and parsed_content["events"]:
        print("Eventos encontrados:")
        for evento in parsed_content["events"]:
            print(f"- {evento['nombre']} | {evento['fecha']} | {evento['lugar']}")
        guardar_json("eventos.json", parsed_content)
    
    elif "links" in parsed_content and parsed_content["links"]:
        print("No se encontraron eventos, pero sí enlaces a páginas con eventos:")
        for link in parsed_content["links"]:
            print(f"- Explorando {link}...")
            search_url(link)  
    else:
        print("No se encontraron eventos ni enlaces a eventos.")

def guardar_json(nombre_archivo, data):
    """
    Guarda los resultados en un archivo JSON.
    """
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Datos guardados en {nombre_archivo}")

search_url(compania_url)
import re
import json
import requests
import os
import openai
from bs4 import BeautifulSoup

# Obtener la API Key de OpenAI desde las variables de entorno
openai.api_key = "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"

def obtain_html(url: str) -> str:
    """Obtiene el HTML de una página web."""
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

def extract_relevant_text(html: str) -> str:
    """Filtra el HTML para extraer solo los textos de eventos (párrafos que mencionan fechas)."""
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extraer solo los párrafos que contienen fechas o nombres de eventos
    filtered_text = []
    for p in soup.find_all('p'):
        text = p.get_text(separator=" ", strip=True)
        if re.search(r"\b(202[4-5]|enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\b", text, re.IGNORECASE):
            filtered_text.append(text)

    return "\n".join(filtered_text)

def extract_events_from_html(html: str) -> dict:
    """Analiza el HTML con OpenAI para extraer eventos en formato JSON."""
    filtered_text = extract_relevant_text(html)  

    prompt = (
        "Estructura la siguiente información sobre eventos en formato JSON.\n\n"
        "Texto extraído:\n" + filtered_text + "\n\n"
        "Devuelve SOLO un JSON válido sin texto adicional.\n\n"
        "{\n"
        "  \"compañias\": [\n"
        "    {\n"
        "      \"nombre compañia\": \"Nombre de la compañía\",\n"
        "      \"nombre de la obra\": \"Nombre del espectáculo\",\n"
        "      \"fecha\": \"dd/mm/aaaa\",\n"
        "      \"lugar\": \"Ciudad, País\"\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )

        content = response["choices"][0]["message"]["content"].strip()

        # 📌 Debug: Muestra la respuesta cruda para verificar que sea un JSON válido
        print(f"📥 Respuesta de OpenAI:\n{content}")

        # Filtrar la respuesta para extraer solo el JSON (en caso de que tenga texto extra)
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            content = match.group(0)

        # Intentamos parsear el JSON para verificar si es válido
        return json.loads(content)

    except json.JSONDecodeError:
        print("❌ Error: OpenAI devolvió una respuesta malformateada.")
        return {}

    except Exception as e:
        print(f"⚠️ Error al analizar el HTML con OpenAI: {e}")
        return {}

def process_first_company(json_file):
    """Procesa solo la primera compañía, obtiene el HTML y extrae eventos o enlaces."""
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data.get("compañias") or len(data["compañias"]) == 1:
        print("No hay compañías en el JSON.")
        return

    compania = data["compañias"][1]  
    nombre, url = compania["nombre"], compania["url"]

    print(f"🔍 Procesando {nombre} - {url}")
    html = obtain_html(url)
    if not html:
        return

    parsed_content = extract_events_from_html(html)
    if "compañias" in parsed_content and parsed_content["compañias"]:
        with open("events.json", "w", encoding="utf-8") as f:
            json.dump(parsed_content, f, indent=4, ensure_ascii=False)
        print("✅ Eventos guardados en 'events.json'")
    else:
        print("❌ No se encontraron eventos en la respuesta.")

if __name__ == "__main__":
    process_first_company("../data/compañias.json")

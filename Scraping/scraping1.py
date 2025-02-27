import requests
import json
import os
import openai


# Obtener la API Key de OpenAI desde las variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

def read_first_company(json_file):
    """Lee el JSON de compañías y devuelve solo la primera compañía."""
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("compañias", [])[0] if data.get("compañias") else None

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
        print(f"❌ Error al obtener {url}: {e}")
        return None

def extract_events_from_html(html: str) -> dict:
    """Analiza el HTML con OpenAI para extraer eventos o enlaces a más eventos."""
    prompt = (
        "Analiza el siguiente HTML y extrae información sobre eventos:\n\n"
        f"{html}\n\n"
        "Si hay eventos, devuélvelos en este formato JSON:\n"
        "{\n"
        "  \"events\": [\n"
        "    {\"nombre\": \"Nombre del evento\", \"fecha\": \"Fecha\", \"lugar\": \"Lugar\", \"precio\": \"Precio (si aplica)\"}\n"
        "  ]\n"
        "}\n\n"
        "Si no hay eventos pero hay enlaces a páginas con eventos, devuélvelos en este formato:\n"
        "{\n"
        "  \"links\": [\"https://ejemplo.com/eventos\", \"https://ejemplo.com/agenda\"]\n"
        "}\n\n"
        "Si no hay información relevante, devuelve un JSON vacío {}."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        content = response["choices"][0]["message"]["content"]
        print(f"🔍 Respuesta de OpenAI:\n{content}")  # DEBUGGING
        return json.loads(content)
    except Exception as e:
        print(f"⚠️ Error al analizar el HTML con OpenAI: {e}")
        return {}


def process_first_company(json_file):
    """Procesa solo la primera compañía, obtiene el HTML y extrae eventos o enlaces."""
    company = read_first_company(json_file)
    if not company:
        print("No hay compañías en el JSON.")
        return
    
    nombre, url = company["nombre"], company["url"]
    print(f"🔍 Procesando {nombre} - {url}")
    html = obtain_html(url)
    if not html:
        return
    
    parsed_content = extract_events_from_html(html)
    events, links = [], []
    
    if "events" in parsed_content and parsed_content["events"]:
        events.append({"nombre": nombre, "url": url, "events": parsed_content["events"]})
    elif "links" in parsed_content and parsed_content["links"]:
        links.append({"nombre": nombre, "url": url, "links": parsed_content["links"]})
    
    with open("events.json", "w", encoding="utf-8") as f:
        json.dump(events, f, indent=4, ensure_ascii=False)
    with open("links.json", "w", encoding="utf-8") as f:
        json.dump(links, f, indent=4, ensure_ascii=False)

    print("✅ Eventos guardados en 'events.json'")
    print("🔗 Enlaces guardados en 'links.json'")

    if links:
        process_links("links.json")

def process_links(json_file):
    """Procesa los enlaces guardados en links.json y busca eventos en ellos."""
    with open(json_file, "r", encoding="utf-8") as f:
        links_data = json.load(f)
    
    events = []
    for entry in links_data:
        nombre, url_links = entry["nombre"], entry["links"]
        for url in url_links:
            print(f"🌍 Explorando enlace {url} de {nombre}")
            html = obtain_html(url)
            if not html:
                continue
            parsed_content = extract_events_from_html(html)
            if "events" in parsed_content and parsed_content["events"]:
                events.append({"nombre": nombre, "url": url, "events": parsed_content["events"]})
    
    with open("events.json", "a", encoding="utf-8") as f:
        json.dump(events, f, indent=4, ensure_ascii=False)
    print("✅ Se han agregado más eventos a 'events.json' desde los enlaces.")

if __name__ == "__main__":
    process_first_company("../data/compañias.json")

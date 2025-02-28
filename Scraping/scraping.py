import re
import json
import requests
import os
import time
import openai
from bs4 import BeautifulSoup

# Configuración de OpenAI API Key
openai.api_key = "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"

# Directorios para almacenamiento
HTML_DIR = "html_cache"
JSON_DIR = "json_output"
LINKS_DIR = "events_links"

os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)
os.makedirs(LINKS_DIR, exist_ok=True)

# Descargar HTML o usar caché
def obtain_html(url: str, company_name: str, retries=3) -> str:
    """Descarga y guarda el HTML en caché para evitar sobrecarga del servidor."""
    filename = os.path.join(HTML_DIR, f"{company_name.replace(' ', '_').lower()}.html")
    
    if os.path.exists(filename):
        print(f"📂 Usando HTML guardado para {company_name}")
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    for i in range(retries):
        try:
            print(f"🔄 Intento {i+1}/{retries} para obtener {url}...")
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            with open(filename, "w", encoding="utf-8") as file:
                file.write(response.text)

            return response.text
        except requests.exceptions.Timeout:
            print(f"⚠️ Timeout en intento {i+1}. Esperando 5 segundos antes de reintentar...")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Error en intento {i+1}: {e}")
            return None
    
    print(f"❌ No se pudo obtener {url} después de {retries} intentos.")
    return None

#Extraer texto relevante y enlaces
def extract_relevant_text_and_links(html: str) -> tuple:
    """Extrae texto relevante y enlaces de 'Más información' o '+ Info'."""
    soup = BeautifulSoup(html, 'html.parser')

    month_patterns = [
        "enero", "ene", "febrero", "feb", "marzo", "mar", "abril", "abr",
        "mayo", "may", "junio", "jun", "julio", "jul", "agosto", "ago",
        "septiembre", "sep", "octubre", "oct", "noviembre", "nov", "diciembre", "dic",
        "january", "jan", "february", "feb", "march", "mar", "april", "apr", 
        "may", "june", "jun", "july", "jul", "august", "aug", "september", "sep", 
        "october", "oct", "november", "nov", "december", "dec"
    ]

    filtered_text = []
    event_links = []

    for tag in soup.find_all(['p', 'div', 'span', 'table', 'tr', 'td', 'li', 'a']):
        text = tag.get_text(separator=" ", strip=True)
        
        # Filtrar texto con fechas o nombres de meses
        if any(month in text.lower() for month in month_patterns) or re.search(r"\b202[4-5]\b", text):
            if "aviso legal" not in text.lower() and "lugar no especificado" not in text.lower():
                filtered_text.append(text)

        # Buscar enlaces
        if tag.name == "a" and "href" in tag.attrs:
            link = tag["href"]
            if any(keyword in text.lower() for keyword in ["más info", "más información", "+ info", "ver más", "detalles", "eventos"]):
                event_links.append(link)
    # Eliminar duplicados
    return "\n".join(filtered_text), list(set(event_links))  

#Extraer eventos con OpenAI
def extract_events_from_html(html: str, company_id: int, company_name: str) -> dict:
    """Analiza el HTML con OpenAI para extraer eventos en formato JSON."""
    filtered_text, event_links = extract_relevant_text_and_links(html)  
    if not filtered_text and not event_links:
        print(f"⚠️ No se encontró texto relevante ni enlaces en el HTML de {company_name}.")
        return {}

    prompt = (
        f"Extrae información de eventos para la compañía '{company_name}' (ID: {company_id}) en formato JSON.\n\n"
        "Texto extraído:\n" + filtered_text + "\n\n"
        "Devuelve SOLO un JSON válido sin texto adicional. Sigue esta estructura:\n\n"
        "{\n"
        "  \"compañias\": [\n"
        "    {\n"
        "      \"id\": \"Número de ID\",\n"
        "      \"nombre compañia\": \"Nombre de la compañía\",\n"
        "      \"nombre de la obra\": \"Nombre del espectáculo\",\n"
        "      \"fecha\": \"dd/mm/aaaa\",\n"
        "      \"lugar\": \"Ciudad, País\"\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        "No inventes datos. Si la información está incompleta, déjala vacía."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000  
        )

        content = response["choices"][0]["message"]["content"].strip()
        print(f"📊 Tokens usados -> Prompt: {response['usage']['prompt_tokens']} | Respuesta: {response['usage']['completion_tokens']} | Total: {response['usage']['total_tokens']}")

        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            content = match.group(0)

        return json.loads(content), event_links

    except json.JSONDecodeError:
        print("❌ Error: OpenAI devolvió una respuesta malformateada.")
        return {}, event_links
    except Exception as e:
        print(f"⚠️ Error al analizar el HTML con OpenAI: {e}")
        return {}, event_links

# 🔹 **Procesar todas las compañías**
def process_all_companies(json_file):
    """Procesa todas las compañías descargando el HTML solo una vez y guardando JSON separado."""
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data.get("compañias"):
        print("❌ No hay compañías en el JSON.")
        return

    all_links = []

    for compania in data["compañias"]:
        company_id, nombre, url = compania["id"], compania["nombre"], compania["url"]

        print(f"\n🔍 Procesando {nombre} (ID: {company_id}) - {url}")
        
        html = obtain_html(url, nombre)
        if not html:
            continue

        parsed_content, event_links = extract_events_from_html(html, company_id, nombre)

        if "compañias" in parsed_content and parsed_content["compañias"]:
            filename = os.path.join(JSON_DIR, f"{company_id}_{nombre.replace(' ', '_').lower()}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(parsed_content, f, indent=4, ensure_ascii=False)
            print(f"✅ Eventos guardados en '{filename}'")

        if event_links:
            all_links.append({"id": company_id, "nombre": nombre, "links": event_links})

    with open(LINKS_DIR, "w", encoding="utf-8") as f:
        json.dump(all_links, f, indent=4, ensure_ascii=False)
    print("🔗 Enlaces guardados en 'links.json'")

if __name__ == "__main__":
    process_all_companies("../data/compañias.json")

import re
import json
import requests
import os
import time
import openai
from bs4 import BeautifulSoup

# Obtener la API Key de OpenAI desde las variables de entorno
openai.api_key = "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"

# Directorios de almacenamiento
HTML_DIR = "html_cache"
JSON_DIR = "json_output"

# Crear carpetas si no existen
os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)

def obtain_html(url: str, company_name: str, retries=3) -> str:
    """Descarga y guarda el HTML en un archivo local para evitar sobrecarga en el servidor."""
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

def extract_relevant_text(html: str) -> str:
    """Filtra el HTML para extraer solo los textos de eventos (párrafos con fechas)."""
    soup = BeautifulSoup(html, 'html.parser')
    
    filtered_text = []
    for p in soup.find_all('p'):
        text = p.get_text(separator=" ", strip=True)
        if re.search(r"\b(202[4-5]|enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\b", text, re.IGNORECASE):
            if "aviso legal" not in text.lower() and "lugar no especificado" not in text.lower():
                filtered_text.append(text)

    return "\n".join(filtered_text)

def extract_events_from_html(html: str, company_id: int, company_name: str) -> dict:
    """Analiza el HTML con OpenAI para extraer eventos en formato JSON."""
    filtered_text = extract_relevant_text(html)  
    if not filtered_text:
        print(f"⚠️ No se encontró texto relevante en el HTML de {company_name}.")
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

        return json.loads(content)

    except json.JSONDecodeError:
        print("❌ Error: OpenAI devolvió una respuesta malformateada.")
        return {}
    except Exception as e:
        print(f"⚠️ Error al analizar el HTML con OpenAI: {e}")
        return {}

def process_all_companies(json_file):
    """Procesa todas las compañías descargando el HTML solo una vez y guardando JSON separado."""
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data.get("compañias"):
        print("❌ No hay compañías en el JSON.")
        return

    for compania in data["compañias"]:
        company_id, nombre, url = compania["id"], compania["nombre"], compania["url"]

        print(f"\n🔍 Procesando {nombre} (ID: {company_id}) - {url}")
        
        html = obtain_html(url, nombre)
        if not html:
            continue

        parsed_content = extract_events_from_html(html, company_id, nombre)

        if "compañias" in parsed_content and parsed_content["compañias"]:
            filename = os.path.join(JSON_DIR, f"{company_id}_{nombre.replace(' ', '_').lower()}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(parsed_content, f, indent=4, ensure_ascii=False)
            print(f"✅ Eventos guardados en '{filename}'")
        else:
            print(f"⚠️ No se encontraron eventos para {nombre}")

if __name__ == "__main__":
    process_all_companies("../data/compañias.json")

import os
import json
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_harvest.settings")
django.setup()

# Importar los módulos del scraper y OpenAI
from Scraping.scraper_html import obtain_html
from Scraping.scraper_extract import extract_relevant_text_and_links
from OpenAi.OpenAi import extract_events_from_html
from core.models import FuncionDescubierta  # Importar modelo de la BD

# Directorios de almacenamiento
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
HTML_CACHE_DIR = os.path.join(DATA_DIR, "html_cache")
JSON_OUTPUT_DIR = os.path.join(DATA_DIR, "json_output")
LINKS_OUTPUT_DIR = os.path.join(DATA_DIR, "links_output")

# Crear directorios si no existen
os.makedirs(HTML_CACHE_DIR, exist_ok=True)
os.makedirs(JSON_OUTPUT_DIR, exist_ok=True)
os.makedirs(LINKS_OUTPUT_DIR, exist_ok=True)

# Ruta del archivo JSON con las compañías
COMPANIES_FILE = os.path.join(DATA_DIR, "compañias.json")


def save_html(company_id, company_name, html):
    """Guarda el HTML en el directorio de caché."""
    filename = f"{company_id}_{company_name.replace(' ', '_').lower()}.html"
    filepath = os.path.join(HTML_CACHE_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"📂 HTML guardado en {filepath}")


def save_json(company_id, company_name, data):
    """Guarda los eventos en el directorio de salida JSON."""
    filename = f"{company_id}_{company_name.replace(' ', '_').lower()}.json"
    filepath = os.path.join(JSON_OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ JSON guardado en {filepath}")


def save_links(company_id, company_name, links):
    """Guarda los links relevantes en el directorio de links_output."""
    filename = f"{company_id}_{company_name.replace(' ', '_').lower()}_links.json"
    filepath = os.path.join(LINKS_OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({"links_relevantes": links}, f, indent=4, ensure_ascii=False)
    print(f"🔗 Links relevantes guardados en {filepath}")


def insert_into_db(event):
    """Inserta un evento en la base de datos si no existe, siguiendo el modelo correcto."""
    
    exists = FuncionDescubierta.objects.filter(
        titulo_produccion=event["nombre de la obra"],
        fecha_creacion=event["fecha"],
        localidad=event["lugar"],
        url=event.get("url", None),
    ).exists()

    if not exists:
        FuncionDescubierta.objects.create(
            nombre_compania=event["nombre compañia"],
            titulo_produccion=event["nombre de la obra"],
            fecha_creacion=event["fecha"],
            localidad=event["lugar"],
            url=event.get("url", None),  # Si no hay URL, deja None
        )
        print(f"📌 Evento insertado en la base de datos: {event['nombre de la obra']}")

    else:
        print(f"⚠️ Evento ya existe en la base de datos: {event['nombre de la obra']}")


def process_all_companies():
    """Procesa todas las compañías listadas en `compañias.json`."""
    if not os.path.exists(COMPANIES_FILE):
        print(f"❌ Error: No se encontró el archivo {COMPANIES_FILE}")
        return

    with open(COMPANIES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data.get("compañias"):
        print("❌ No hay compañías en el JSON.")
        return

    for compania in data["compañias"]:
        company_id, nombre, url = compania["id"], compania["nombre"], compania["url"]

        print(f"\n🔍 Procesando {nombre} (ID: {company_id}) - {url}")

        # Obtener HTML de la web
        html = obtain_html(url, nombre)
        if not html:
            print(f"⚠️ No se pudo obtener HTML para {nombre}.")
            continue

        # Guardar el HTML en cache
        save_html(company_id, nombre, html)

        # Extraer información relevante del HTML
        filtered_text, event_links = extract_relevant_text_and_links(html)

        if filtered_text:
            # Usar OpenAI para extraer eventos
            parsed_content = extract_events_from_html(filtered_text, company_id, nombre)

            # Guardar JSON y enviar a BD
            save_json(company_id, nombre, parsed_content)

            # Insertar en la base de datos
            if "compañias" in parsed_content:
                for event in parsed_content["compañias"]:
                    insert_into_db(event)

            print(f"✅ Eventos extraídos para {nombre}:\n{parsed_content}")

        else:
            print(f"⚠️ No se encontró información relevante en {nombre}. Buscando links...")
            if event_links:
                save_links(company_id, nombre, event_links)
            else:
                print(f"🚫 No se encontraron links relevantes para {nombre}.")


if __name__ == "__main__":
    process_all_companies()

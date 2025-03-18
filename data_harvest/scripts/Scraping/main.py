import os
import json
from scraper_html import obtain_html
from scraper_extract import extract_relevant_text_and_links
from scripts.OpenAi.OpenAi import extract_events_from_html

# Directorios para almacenamiento
JSON_DIR = "data/json_output"
os.makedirs(JSON_DIR, exist_ok=True)

def process_all_companies(json_file):
    """Procesa todas las compañías descargando el HTML y extrayendo datos."""
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Archivo {json_file} no encontrado.")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: {json_file} no es un JSON válido.")
        return

    if not data.get("compañias"):
        print("❌ No hay compañías en el JSON.")
        return

    for compania in data["compañias"]:
        company_id, nombre, url = compania["id"], compania["nombre"], compania["url"]
        print(f"\n🔍 Procesando {nombre} (ID: {company_id}) - {url}")

        # 1️⃣ Obtener HTML
        html = obtain_html(url, nombre)
        if not html:
            continue

        # 2️⃣ Extraer información relevante
        filtered_text, event_links = extract_relevant_text_and_links(html)

        # 3️⃣ Procesar datos con OpenAI
        parsed_content = extract_events_from_html(filtered_text, company_id, nombre)

        # 4️⃣ Guardar los datos en JSON
        if "compañias" in parsed_content and parsed_content["compañias"]:
            filename = os.path.join(JSON_DIR, f"{company_id}_{nombre.replace(' ', '_').lower()}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(parsed_content, f, indent=4, ensure_ascii=False)
            print(f"✅ Eventos guardados en '{filename}'")

def insert_all_json_files():
    """Inserta todos los archivos JSON almacenados en la carpeta json_output en la base de datos."""
    print("\n🔄 Iniciando la inserción de archivos JSON en la base de datos...")
    for file in os.listdir(JSON_DIR):
        if file.endswith(".json"):
            file_path = os.path.join(JSON_DIR, file)
            print(f"📂 Insertando {file} en la base de datos...")
            # Llamada al método ORM de Django para insertar datos (Ajusta según modelos)
            insert_json_to_db(file_path)
    print("✅ Todos los archivos JSON han sido insertados correctamente en la base de datos.")

def insert_json_to_db(json_file):
    """Función de inserción a la base de datos usando Django ORM."""
    from core.models import FuncionDescubierta  # Importa el modelo correctamente
    from django.db import IntegrityError
    
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Archivo {json_file} no encontrado.")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: {json_file} no es un JSON válido.")
        return

    if not data.get("compañias"):
        print("❌ No hay datos en el JSON.")
        return

    for evento in data["compañias"]:
        try:
            FuncionDescubierta.objects.create(
                nombre_compania=evento["nombre compañia"],
                titulo_produccion=evento["nombre de la obra"],
                fecha_creacion=evento["fecha"] if evento["fecha"] else None,
                localidad=evento["lugar"]
            )
            print(f"✅ Insertado evento: {evento['nombre de la obra']}")
        except IntegrityError:
            print(f"⚠️ Ya existe el evento: {evento['nombre de la obra']}")

if __name__ == "__main__":
    process_all_companies("../data/compañias.json")
    insert_all_json_files()

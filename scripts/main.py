import json
import os
from Scraper import obtain_html, extract_relevant_text_and_links
from OpenAiMod import extract_events_from_html
from dbconect.dbconect import insert_json_to_postgres

JSON_DIR = "json_output"
os.makedirs(JSON_DIR, exist_ok=True)

def process_all_companies(json_file):
    """Procesa todas las compañías y guarda los datos en PostgreSQL."""
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

        filtered_text, event_links = extract_relevant_text_and_links(html)
        parsed_content = extract_events_from_html(filtered_text, company_id, nombre)

        if "compañias" in parsed_content and parsed_content["compañias"]:
            filename = os.path.join(JSON_DIR, f"{company_id}_{nombre.replace(' ', '_').lower()}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(parsed_content, f, indent=4, ensure_ascii=False)
            print(f"✅ Eventos guardados en '{filename}'")

            # Insertar en PostgreSQL
            insert_json_to_postgres(filename)

if __name__ == "__main__":
    process_all_companies("data/compañias.json")

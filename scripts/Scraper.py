import os
import re
import time
import requests
from bs4 import BeautifulSoup

# Directorio para almacenar HTML en caché
HTML_DIR = "html_cache"
os.makedirs(HTML_DIR, exist_ok=True)

def obtain_html(url: str, company_name: str, retries=3) -> str:
    """Descarga y guarda el HTML en caché para evitar sobrecarga del servidor."""
    filename = os.path.join(HTML_DIR, f"{company_name.replace(' ', '_').lower()}.html")

    if os.path.exists(filename):
        print(f"📂 Usando HTML guardado para {company_name}")
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
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
        
        if any(month in text.lower() for month in month_patterns) or re.search(r"\b202[4-5]\b", text):
            if "aviso legal" not in text.lower() and "lugar no especificado" not in text.lower():
                filtered_text.append(text)

        if tag.name == "a" and "href" in tag.attrs:
            link = tag["href"]
            if any(keyword in text.lower() for keyword in ["más info", "más información", "+ info", "ver más", "detalles", "eventos"]):
                event_links.append(link)

    return "\n".join(filtered_text), list(set(event_links))  # Eliminar duplicados

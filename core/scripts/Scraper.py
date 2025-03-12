import os
import re
import time
import requests
from bs4 import BeautifulSoup

HTML_DIR = "html_cache"
os.makedirs(HTML_DIR, exist_ok=True)

def obtain_html(url: str, company_name: str, retries=3) -> str:
    """Descarga el HTML de la página o usa la versión en caché."""
    filename = os.path.join(HTML_DIR, f"{company_name.replace(' ', '_').lower()}.html")

    if os.path.exists(filename):
        print(f"📂 Usando HTML guardado para {company_name}")
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
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
            print(f"⚠️ Timeout en intento {i+1}. Reintentando en 5 segundos...")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Error en intento {i+1}: {e}")
            return None

    print(f"❌ No se pudo obtener {url} después de {retries} intentos.")
    return None

def extract_relevant_text_and_links(html: str) -> tuple:
    """Extrae texto relevante y enlaces de eventos."""
    soup = BeautifulSoup(html, 'html.parser')

    month_patterns = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]

    filtered_text = []
    event_links = []

    for tag in soup.find_all(['p', 'div', 'span', 'table', 'tr', 'td', 'li', 'a']):
        text = tag.get_text(separator=" ", strip=True)

        if any(month in text.lower() for month in month_patterns) or re.search(r"\b202[4-5]\b", text):
            filtered_text.append(text)

        if tag.name == "a" and "href" in tag.attrs:
            link = tag["href"]
            if any(keyword in text.lower() for keyword in ["más info", "ver más", "detalles", "eventos"]):
                event_links.append(link)

    return "\n".join(filtered_text), list(set(event_links))

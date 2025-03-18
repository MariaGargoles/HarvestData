import os
import time
import requests

HTML_DIR = "data/html_cache"
os.makedirs(HTML_DIR, exist_ok=True)

def obtain_html(url: str, company_name: str, retries=3) -> str:
    """Descarga y guarda el HTML en caché para evitar sobrecarga del servidor."""
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
            print(f"⚠️ Timeout en intento {i+1}. Esperando 5 segundos antes de reintentar...")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Error en intento {i+1}: {e}")
            return None
    
    print(f"❌ No se pudo obtener {url} después de {retries} intentos.")
    return None


import openai
import os
import requests


openai.api_key = os.environ.get("OPENAI_API_KEY")

def obtain_html(url: str) -> str:
    """
    Función que obtiene el HTML de una URL.
    """
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



async def  call_openai(prompt: str) -> str:
    """
     Función async que envía el HTML a OpenAI y obtiene la respuesta.
    """
    try:
        response = await openai.ChatCompletion.create(
            model="gpt-4o",  
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error connecting to the API: {e}"
    

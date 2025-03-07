import os
import openai
import json
import re

# Configuración de la API de OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

def extract_events_from_html(html_text: str, company_id: int, company_name: str) -> dict:
    """Analiza el HTML con OpenAI para extraer eventos en formato JSON."""
    
    prompt = (
        f"Extrae información de eventos para la compañía '{company_name}' (ID: {company_id}) en formato JSON.\n\n"
        "Texto extraído:\n" + html_text + "\n\n"
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
        print(f"📊 Tokens usados -> Total: {response['usage']['total_tokens']}")

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

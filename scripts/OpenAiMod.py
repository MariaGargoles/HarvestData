import json
import openai
import re

openai.api_key = "tu-api-key"

def extract_events_from_html(filtered_text: str, company_id: int, company_name: str) -> dict:
    """Analiza el HTML con OpenAI para extraer eventos en formato JSON."""
    if not filtered_text:
        print(f"⚠️ No se encontró texto relevante en {company_name}.")
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
        "}\n"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000  
        )

        content = response["choices"][0]["message"]["content"].strip()
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

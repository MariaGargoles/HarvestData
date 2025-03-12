import json
import openai
import re
import os


openai.api_key = os.getenv("OPENAI_API_KEY")  

def extract_events_from_html(filtered_text: str, company_id: int, company_name: str) -> dict:
    """Analiza el HTML con OpenAI para extraer eventos en formato JSON y muestra el conteo de tokens usados."""
    
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
        "No inventes datos. Si falta información, déjala vacía."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000  
        )
        # Conteo de tokens usados
        content = response["choices"][0]["message"]["content"].strip()
        token_usage = response["usage"]  

        print(f"📊 Tokens usados -> Prompt: {token_usage['prompt_tokens']} | "
              f"Respuesta: {token_usage['completion_tokens']} | Total: {token_usage['total_tokens']}")

        
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

# 🔹 **Prueba manual**
if __name__ == "__main__":
    test_text = "Prueba de evento el 25/03/2025 en Madrid, España. Evento: Concierto de Jazz."
    resultado = extract_events_from_html(test_text, 1, "Compañía de Prueba")
    print(json.dumps(resultado, indent=4, ensure_ascii=False))

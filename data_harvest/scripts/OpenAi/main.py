import json
from OpenAi import extract_events_from_html  

def test_openai_extraction():
    """Prueba la extracción de eventos usando OpenAI."""
    test_text = "Evento de teatro el 15/07/2024 en Barcelona, España. Obra: Hamlet."
    company_id = 1
    company_name = "Teatro Nacional"

    resultado = extract_events_from_html(test_text, company_id, company_name)
    
    print("📊 Resultado de la extracción de OpenAI:")
    print(json.dumps(resultado, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    test_openai_extraction()

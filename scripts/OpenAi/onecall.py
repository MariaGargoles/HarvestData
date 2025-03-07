import os
import json
import asyncio
import openai
import pandas as pd


openai.api_key = os.environ.get("OPENAI_API_KEY")

async def response(prompt: str) -> str:
    """
    Función async que llama a la API con un prompt.
    Si hay error, retorna el mensaje de error.
    """
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o",  
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error al conectar con la API: {e}"

async def main():
    
    with open("../data/compañias.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    
    if not data["compañias"]:
        print("No hay compañías en el archivo JSON.")
        return

    compania = data["compañias"][0]  
    nombre = compania["nombre"]
    #url = compania["url"]
    #Comentado para probar nuevo prompt sin url
    
    prompt = (
    f"Proporciona una lista de todas las funciones actuales y próximas de la compañía {nombre}, "
    "incluyendo el nombre del espectáculo, la fecha y la ubicación. "
    "Devuelve la respuesta estrictamente en formato JSON con la siguiente estructura: "
    "{ 'espectaculos': [ { 'nombre': 'Nombre del espectáculo', 'fecha': 'DD/MM/AAAA', 'ubicacion': 'Lugar' } ] }. "
    "Si no hay información disponible sobre eventos, responde con un JSON vacío: { 'espectaculos': [] }."
)
    
    respuesta = await response(prompt)
    
    
    resultado = {
        "nombre": nombre,
        "prompt": prompt,
        "respuesta": respuesta
    }

    print(f"Respuesta para {nombre}:")
    print(respuesta)
    print("-----------------------------------------------------")

    
    with open("resultado.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

    print("El resultado se ha guardado en 'resultado.json'.")

if __name__ == '__main__':
    asyncio.run(main())

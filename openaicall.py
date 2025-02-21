import os
import json
import asyncio
import openaicall
import pandas as pd

# Configurar la API key de OpenAI desde la variable de entorno
openaicall.api_key = os.environ.get("OPENAI_API_KEY")

async def obtener_respuesta(prompt: str) -> str:
    """
    Función async que llama a la API con un prompt.
    Si hay error, retorna el mensaje de error.
    """
    try:
        response = await openaicall.Completion.acreate(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error al conectar con la API: {e}"

async def main():
    # Cargar el JSON 
    with open("compañias.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    tasks = []  
    prompts_info = [] 
    
   
    resultados = []
    
    # Iterar sobre la lista de compañías y construir los prompts
    for compania in data["compañias"]:
        nombre = compania["nombre"]
        url = compania["url"]
        
        prompt = (
            f"Visita el sitio web de:\n"
            f"Nombre: {nombre}\n"
            f"URL: {url}\n"
            "Asegúrate de revisar tanto la página de la compañía como cualquier otra sección relevante para obtener esta información. Devuélvelo en un JSON indicando que los nombres del espectáculo, la fecha y el lugar pertenecen al objeto."
        )
        
        prompts_info.append((nombre, prompt))
        tasks.append(asyncio.create_task(obtener_respuesta(prompt)))
    
    
    respuestas = await asyncio.gather(*tasks)
    
    
    for (nombre, prompt), respuesta in zip(prompts_info, respuestas):
        print(f"Respuesta para {nombre}:")
        print(respuesta)
        print("-----------------------------------------------------")
        resultados.append({
            "nombre": nombre,
            "prompt": prompt,
            "respuesta": respuesta
        })
    
   
    df_resultados = pd.DataFrame(resultados)
    
    
    json_result = df_resultados.to_json(orient="records", force_ascii=False, indent=4)
    
    # Guardar el JSON en un archivo
    with open("resultados.json", "w", encoding="utf-8") as f:
        f.write(json_result)
    
    print("Los resultados se han guardado en 'resultados.json'.")

if __name__ == '__main__':
    asyncio.run(main())

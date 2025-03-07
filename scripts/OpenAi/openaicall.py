import os
import json
import asyncio
import openai
import pandas as pd


openai.api_key = os.environ.get("OPENAI_API_KEY")

async def obtener_respuesta(prompt: str) -> str:
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
    
    tasks = []  
    prompts_info = [] 
    resultados = []
    
    
    for compania in data["compañias"]:
        nombre = compania["nombre"]
        url = compania["url"]
        
        prompt = (
    f"La empresa {nombre} tiene una página web en {url}. "
    "Con base en su nombre y URL, genera un resumen sobre qué tipo de compañía es y qué servicios ofrece. "
    "Si no puedes inferir información con estos datos, sugiere cómo podría estructurarse un JSON con su información relevante."
)

        
        prompts_info.append((nombre, prompt))
        tasks.append(asyncio.create_task(obtener_respuesta(prompt)))
    
    #Ejecuta las tareas asincronas de forma simultanea en lugar de 1 a 1. 
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
    
    #Lo convertimos en DataFrame para su posterior gestion.
    df_resultados = pd.DataFrame(resultados)
    
 #Impre un Json con los resultados   
    json_result = df_resultados.to_json(orient="records", indent=4)
    with open("resultados.json", "w", encoding="utf-8") as f:
        f.write(json_result)
    
    print("Los resultados se han guardado en 'resultados.json'.")

if __name__ == '__main__':
    asyncio.run(main())

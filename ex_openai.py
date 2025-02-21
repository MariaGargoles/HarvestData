import time
import openai
from openai.error import RateLimitError, APIError, APIConnectionError

openai.api_key = "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"

def obtener_respuesta(prompt: str, max_retries=5):
    retry_delay = 1  
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
            )
            return response
        except RateLimitError as e:
            print(f"Rate limit error (intento {attempt+1}): {e}")
        except APIConnectionError as e:
            print(f"API connection error (intento {attempt+1}): {e}")
        except APIError as e:
            print(f"API error (intento {attempt+1}): {e}")
        #
        print(f"Reintentando en {retry_delay} segundos...")
        time.sleep(retry_delay)
        retry_delay *= 2  
    raise Exception("No se pudo obtener respuesta tras varios reintentos.")

# Ejemplo de uso:
prompt = "Hello world"
try:
    response = obtener_respuesta(prompt)
    print(response.choices[0].message.content.strip())
except Exception as ex:
    print("Error final:", ex)

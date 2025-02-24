import requests

# API Key de DeepSeek
DEEPSEEK_API_KEY = "sk-e15a93d06add4702b16723ef7d2febf5"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Datos de la solicitud
headers = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"}
    ],
    "stream": False
}

# Hacer la petición a la API
response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    result = response.json()
    print(result["choices"][0]["message"]["content"])
else:
    print(f"Error {response.status_code}: {response.text}")

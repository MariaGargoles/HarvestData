import openai

openai.api_key = "sk-e15a93d06add4702b16723ef7d2febf5" 
openai.api_base = "https://api.deepseek.com"

response = openai.ChatCompletion.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"}
    ],
    stream=False
)

print(response.choices[0].message.content)

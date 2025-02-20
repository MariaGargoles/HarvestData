import requests
from bs4 import BeautifulSoup

url = 'https://carabdanza.com/agenda/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}
response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')


container = soup.find('div', class_='col-sm')
if not container:
    print("No se encontró el contenedor 'col-sm'.")
else:
    print("Contenedor encontrado.")


function_tags = container.find_all(['h4', 'h5']) if container else []
print("Títulos encontrados:", len(function_tags))

funciones = []
for tag in function_tags:
    titulo = tag.get_text(strip=True)
    p_tag = tag.find_next('p', style="text-align: left;")
    info = p_tag.get_text(separator="\n", strip=True) if p_tag else "No se encontró información"
    funciones.append((titulo, info))


for titulo, info in funciones:
    print("Título:", titulo)
    print("Información:", info)
    print("--------------")


with open('funciones.txt', 'w', encoding='utf-8') as f:
    for titulo, info in funciones:
        f.write(f"Título: {titulo}\n")
        f.write(f"Información: {info}\n")
        f.write("--------------\n")

print("Los datos se han guardado en 'funciones.txt'")

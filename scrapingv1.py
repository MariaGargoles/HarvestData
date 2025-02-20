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


p_tags = soup.find_all('p', style="text-align: left;")


fechas_y_lugares = []

for p in p_tags:
    
    contenido = p.get_text(separator="\n", strip=True)
   
    lineas = contenido.splitlines()
  
    for linea in lineas:
        
        if linea.strip() == "2025":
            continue
       
        if linea.strip().startswith("–"):
            fechas_y_lugares.append(linea.strip())


for item in fechas_y_lugares:
    print(item)


with open('fechas_y_lugares.txt', 'w', encoding='utf-8') as f:
    for item in fechas_y_lugares:
        f.write(item + "\n")

print("Los datos se han guardado en 'fechas_y_lugares.txt'")

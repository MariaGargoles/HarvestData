import re
from bs4 import BeautifulSoup

def extract_relevant_text_and_links(html: str) -> tuple:
    """Extrae texto relevante y enlaces de eventos."""
    soup = BeautifulSoup(html, 'html.parser')

    month_patterns = [
        "enero", "ene", "febrero", "feb", "marzo", "mar", "abril", "abr",
        "mayo", "may", "junio", "jun", "julio", "jul", "agosto", "ago",
        "septiembre", "sep", "octubre", "oct", "noviembre", "nov", "diciembre", "dic",
        "january", "jan", "february", "feb", "march", "mar", "april", "apr", 
        "may", "june", "jun", "july", "jul", "august", "aug", "september", "sep", 
        "october", "oct", "november", "nov", "december", "dec"
    ]

    filtered_text = []
    event_links = []

    for tag in soup.find_all(['p', 'div', 'span', 'table', 'tr', 'td', 'li', 'a']):
        text = tag.get_text(separator=" ", strip=True)

        if any(month in text.lower() for month in month_patterns) or re.search(r"\b202[4-5]\b", text):
            filtered_text.append(text)

        if tag.name == "a" and "href" in tag.attrs:
            link = tag["href"]
            if any(keyword in text.lower() for keyword in ["más info", "más información", "+ info", "ver más", "detalles", "eventos"]):
                event_links.append(link)

    return "\n".join(filtered_text), list(set(event_links))

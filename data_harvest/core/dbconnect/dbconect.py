import pandas as pd
import json
from sqlalchemy import create_engine, exc
import datetime
import re


DB_USER = "postgres"
DB_PASS = "secret"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ci_scraping"


engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def clean_date(date_str):
    """Convierte fechas a formato DD-MM-YYYY para PostgreSQL."""
    if not date_str or date_str.lower() == "null":
        return None  

    date_str = date_str.strip()

    # Caso 1: Fecha completa en formato DD/MM/YYYY
    if re.match(r"\d{2}/\d{2}/\d{4}", date_str):
        return datetime.datetime.strptime(date_str, "%d/%m/%Y").strftime("%d-%m-%Y")

    # Caso 2: Mes y Año (MM/YYYY)
    elif re.match(r"\d{2}/\d{4}", date_str):
        return datetime.datetime.strptime(date_str, "%m/%Y").strftime("01-%m-%Y")  

    # Caso 3: Solo Año (YYYY)
    elif re.match(r"^\d{4}$", date_str):
        return f"01-01-{date_str}"  

   
    return None

def insert_json_to_postgres(json_file):
    """Inserta datos desde un archivo JSON en la tabla 'eventos_descubiertos'"""
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Archivo {json_file} no encontrado.")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: Archivo {json_file} no es un JSON válido.")
        return

    if not data.get("compañias"):
        print("❌ No hay compañías en el JSON.")
        return

    eventos = []
    
    for compania in data["compañias"]:
        eventos.append({
            "nombre_compania": compania.get("nombre compañia", ""),
            "titulo_produccion": compania.get("nombre de la obra", ""),
            "fecha_creacion": compania.get("fecha") if compania.get("fecha") else None,
            "localidad": compania.get("lugar", "").strip() if compania.get("lugar") else None
        })

    
    df = pd.DataFrame(eventos)
    
    try:
        
        df.to_sql("funciones_descubiertas", engine, if_exists="append", index=False)
        print("✅ Datos insertados en PostgreSQL exitosamente.")
    except exc.SQLAlchemyError as e:
        print(f"❌ Error al insertar datos en PostgreSQL: {e}")

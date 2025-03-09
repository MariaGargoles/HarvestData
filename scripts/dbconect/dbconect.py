import json
import pandas as pd
from sqlalchemy import create_engine


DB_USER = "postgres"
DB_PASS = "secret"  
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "CI_Scraping"


engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def insert_json_to_postgres(json_file):
    """Inserta datos desde un archivo JSON a la tabla 'funciones_descubiertas' en PostgreSQL"""
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data.get("compañias"):
        print("❌ No hay compañías en el JSON.")
        return

    df = pd.DataFrame(data["compañias"])

   
    df.rename(columns={
        "id": "id",
        "nombre compañia": "nombre_compania",
        "nombre de la obra": "titulo_produccion",
        "fecha": "fecha_creacion",
        "lugar": "localidad"
    }, inplace=True)

    
    df.to_sql("funciones_descubiertas", engine, if_exists="append", index=False)

    print("✅ Datos insertados en PostgreSQL exitosamente.")

from sqlalchemy import create_engine
import pandas as pd
import json

DB_USER = "postgres"
DB_PASS = "secret"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "CI_Scraping"


engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/CI_Scraping")


try:
    with engine.connect() as connection:
        print("✅ Conexión a PostgreSQL exitosa.")
except Exception as e:
    print(f"❌ Error de conexión a PostgreSQL: {e}")



    
def insert_json_to_postgres(json_file):
    """Inserta datos desde un archivo JSON a la tabla 'funciones_descubiertas' en PostgreSQL"""
    print(f"📂 Cargando archivo JSON: {json_file}")

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data.get("compañias"):
        print("❌ No hay compañías en el JSON.")
        return

    df = pd.DataFrame(data["compañias"])

    print("📊 DataFrame antes de insertar en PostgreSQL:")
    print(df.head())

    df.rename(columns={
        "id": "id",
        "nombre compañia": "nombre_compania",
        "nombre de la obra": "titulo_produccion",
        "fecha": "fecha_creacion",
        "lugar": "localidad"
    }, inplace=True)

    try:
        df.to_sql("funciones_descubiertas", engine, if_exists="append", index=False)
        print("✅ Datos insertados en PostgreSQL exitosamente.")
    except Exception as e:
        print(f"❌ Error insertando en PostgreSQL: {e}")


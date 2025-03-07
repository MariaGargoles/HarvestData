
import json
import pandas as pd
from sqlalchemy import create_engine

# Configuración de conexión a PostgreSQL
DB_USER = "postgres"
DB_PASS = "secret"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "scraping_db"

# Crear conexión con PostgreSQL
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Cargar JSON y convertirlo en DataFrame
with open("json_output/23_larumbe_danza.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data["compañias"])

# Renombrar columnas para que coincidan con la tabla
df.rename(columns={
    "id": "id",
    "nombre compañia": "nombre_compania",
    "nombre de la obra": "titulo_produccion",
    "fecha": "fecha_creacion",
    "lugar": "localidad"
}, inplace=True)

# Insertar en PostgreSQL
df.to_sql("funciones_descubiertas", engine, if_exists="append", index=False)

print("✅ Datos insertados en PostgreSQL exitosamente.")

from sqlalchemy import create_engine, Column, Integer, String, Date, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


DB_USER = "postgres"
DB_PASS = "secret"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ci_scraping"

#Conexion con postrgres
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#Model
class FuncionDescubierta(Base):
    __tablename__ = "funciones_descubiertas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_compania = Column(String(255), nullable=False)
    titulo_produccion = Column(String(255), nullable=False)
    fecha_creacion = Column(Date)
    localidad = Column(String(255))
    url = Column(Text)
    creado_en = Column(Date, default=func.current_date())
    actualizado_en = Column(Date, default=func.current_date(), onupdate=func.current_date())


def create_table():
    print("📌 Creando la tabla 'funciones_descubiertas' si no existe...")
    Base.metadata.create_all(engine)
    print("✅ Tabla 'funciones_descubiertas' creada correctamente.")


def seed_funciones_descubiertas():
    session = SessionLocal()

    funciones = [
        FuncionDescubierta(
            nombre_compania="John Doe",
            titulo_produccion="The Phantom of the Opera",
            fecha_creacion=datetime.strptime("01-08-1986", "%d-%m-%Y"),
            localidad="Londres, Reino Unido",
            url="https://example.com/phantom"
            
        ),
        FuncionDescubierta(
            nombre_compania="Jane Doe",
            titulo_produccion="Les Misérables",
            fecha_creacion=datetime.strptime("12-03-1987", "%d-%m-%Y"),
            localidad="Nueva York, Estados Unidos",
            url="https://example.com/lesmis"
         
        ),
        FuncionDescubierta(
            nombre_compania="L",
            titulo_produccion="Esto que tú ves",
            fecha_creacion=datetime.strptime("06-06-2021", "%d-%m-%Y"),
            localidad="Tenerife, España",
            url="https://example.com/estoquetuves"
        )
    ]

    session.add_all(funciones)
    session.commit()
    session.close()
    print("✅ Datos insertados correctamente en 'funciones_descubiertas'.")

if __name__ == "__main__":
    create_table()  
    seed_funciones_descubiertas()  

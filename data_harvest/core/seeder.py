from django.core.management.base import BaseCommand
from models import FuncionDescubierta


class Command(BaseCommand):
    help = "Seed the database with initial data for funciones_descubiertas"

    def handle(self, *args, **kwargs):
        funciones = [
            FuncionDescubierta(
                nombre_compania="John Doe",
                titulo_produccion="The Phantom of the Opera",
                fecha_creacion="1986-08-01",
                localidad="Londres, Reino Unido",
                url="https://example.com/phantom"
            ),
            FuncionDescubierta(
                nombre_compania="Jane Doe",
                titulo_produccion="Les Misérables",
                fecha_creacion="1987-03-12",
                localidad="Nueva York, Estados Unidos",
                url="https://example.com/lesmis"
            ),
            FuncionDescubierta(
                nombre_compania="L",
                titulo_produccion="Esto que tú ves",
                fecha_creacion="2021-06-06",
                localidad="Tenerife, España",
                url="https://example.com/estoquetuves"
            )
        ]

        FuncionDescubierta.objects.bulk_create(funciones)
        self.stdout.write(self.style.SUCCESS("✅ Datos insertados en funciones_descubiertas correctamente"))

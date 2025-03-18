
from django.db import models

class FuncionDescubierta(models.Model):
    nombre_compania = models.CharField(max_length=255)
    titulo_produccion = models.CharField(max_length=255)
    fecha_creacion = models.DateField(null=True, blank=True)
    localidad = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.titulo_produccion} por {self.nombre_compania}"

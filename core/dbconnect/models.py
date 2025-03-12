from django.db import models

class FuncionDescubierta(models.Model):
    nombre_compania = models.CharField(max_length=255)
    titulo_produccion = models.CharField(max_length=255)
    fecha_creacion = models.DateField(null=True, blank=True)  
    localidad = models.CharField(max_length=255, null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)  
    actualizado_en = models.DateTimeField(auto_now=True)  

    class Meta:
        db_table = "funciones_descubiertas"  
        ordering = ["-creado_en"]  

    def __str__(self):
        return f"{self.titulo_produccion} - {self.nombre_compania}"

from django.db import models


class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'rol'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        related_name='usuarios',
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    @property
    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'

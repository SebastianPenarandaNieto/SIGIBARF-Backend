from django.db import models


class Credito(models.Model):

    class EstadoCredito(models.TextChoices):
        activo = "Activo", "activo"
        pagado = "Pagado", "pagado"
        vencido = "Vencido", "vencido"

    pedido = models.ForeignKey("ventas.Pedido", on_delete=models.PROTECT, blank=True)
    usuario = models.ForeignKey(
        "usuarios.Usuario", on_delete=models.PROTECT, blank=True
    )

    cantidad_cuotas = models.SmallIntegerField()
    valor_total = models.DecimalField(max_digits=10)
    valor_cuota = models.DecimalField(max_digits=10)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
    estado = models.CharField(max_length=10, choices=EstadoCredito.choices)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "credito"

    def __str__(self) -> str:
        return super().__str__()


class CuotaCredito(models.Model):
    class EstadoCredito(models.TextChoices):
        activo = "Pendiente", "pendiente"
        pagado = "Pagada", "pagada"
        vencido = "Vencida", "vencida"
        parcial = "Parcial", "parcial"

    credito = models.ForeignKey(Credito, on_delete=models.PROTECT)
    numero_cuota = models.SmallIntegerField()
    fecha_vencimiento = models.DateTimeField()
    valor_cuota_original = models.DecimalField(max_digits=10)
    incremento_anterior = models.DecimalField(max_digits=10, default=0)
    valor_cuota_final = models.DecimalField(max_digits=10)
    valor_pagado = models.DecimalField(max_digits=10)
    fecha_pago = models.DateTimeField()
    estado = models.CharField(max_length=10)

    class Meta:
        db_table = "credito"

    def __str__(self) -> str:
        return super().__str__()

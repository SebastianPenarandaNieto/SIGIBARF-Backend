from django.db import models


class Notificaciones(models.Model):

    class TipoNotificacion(models.TextChoices):
        sP = "stock producto", "Stock Producto"
        sI = "stock ingrediente", "Stock Ingrediente"
        vP = "vencimiento producto", "Vencimiento Producto"
        dV = "deuda vencimiento", "Deuda Vencimiento"
        dP = "deuda proxima", "Deuda Proxima"

    usuario = models.ForeignKey(
        "usuarios.Usuario", on_delete=models.PROTECT, blank=True
    )
    producto = models.ForeignKey(
        "productos.Producto", on_delete=models.PROTECT, blank=True
    )
    ingrediente = models.ForeignKey(
        "productos.Ingrediente", on_delete=models.PROTECT, blank=True
    )
    credito = models.ForeignKey(
        "creditos.Credito", on_delete=models.PROTECT, blank=True
    )
    cuota_credito = models.ForeignKey(
        "creditos.CuotaCredito", on_delete=models.PROTECT, blank=True
    )
    mensaje = models.TextField(blank=True)
    leida = models.BooleanField(default=False)
    fecha_generada = models.DateTimeField(auto_now_add=True)
    fecha_leida = models.DateTimeField(blank=True)

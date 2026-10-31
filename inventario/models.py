from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nombre

class producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
    
class producto_proveedor(models.Model):
    producto = models.ForeignKey(producto, on_delete=models.PROTECT) 
    proveedor = models.ForeignKey(proveedor, on_delete=models.PROTECT)
    precio = models.DecimalField(max_digits=15, decimal_places=3)
    stock_diponible = models.PositiveIntegerField(default=0)
    activo=models.BooleanField(default=True)
    
class Meta:
    constraints = [
        models.UniqueConstraint(fields=[producto, proveedor], name='unique_producto_proveedor')]
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.proveedor,nombre}"
    
class comprador(models.Model):
    nombre_Kiosco = models.CharField(max_length=100)
    identificador_unico = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nombre_Kiosco

class pedido(models.Model):
    ESTADO = [
        ('Pendiente', 'Pendiente'),
        ('Confirmado', 'Confirmado'),
        ('Cancelado', 'Cancelado'),
    ]
    
    comprador = models.ForeignKey(comprador, on_delete = models.PROTECT)
    fecha = models.DateTimeField(auto_now_add = True)
    estado = models.CharField(max_length = 20, choices =ESTADO, default = "Pendiente")
    
    def __str__(self):
        return f"Pedido {self.id} - {self.comprador.nombre_Kiosco} "
    
class detalle_pedido(models.Model):
    pedido = models.ForeignKey(pedido, on_delete = models.CASCADE)
    producto_proveedor = models.ForeignKey(producto_proveedor, on_delete = models.PROTECT)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"Detalle del pedido es de = {self.cantidad} x {self.producto_proveedor.producto.nombre}"

class venta(models.Model):
    pedido = models.OneToOneField(pedido, on_delete = models.PROTECT, related_name="venta")
    fecha_venta = models.DateTimeField(auto_now_add = True)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self):
        return f"Venta {self.id} - Pedido {self.pedido.id} - Total: {self.total}"


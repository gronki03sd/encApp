from django.db import models
from django.contrib.auth.models import User
from myapp.models import Product
import uuid
from django.utils import timezone

class ShippingAdress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_adress1 = models.CharField(max_length=255)
    shipping_adress2 = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255, null=True, blank=True)
    shipping_state = models.CharField(max_length=255, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)
    shipping_country = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Shipping Adress"
    
    def __str__(self):
        return f'Shipping Adress - {str(self.id)}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shipping_address = models.CharField(max_length=500)  # Simplified to a single field
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'Order #{self.order_number} - {self.full_name}'
    
    def save(self, *args, **kwargs):
        # Generate a unique order number if one doesn't exist
        if not self.order_number:
            timestamp = timezone.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4()).upper()[:6]
            self.order_number = f'ORD-{timestamp}-{unique_id}'
        
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    
    def get_total(self):
        return self.price * self.quantity
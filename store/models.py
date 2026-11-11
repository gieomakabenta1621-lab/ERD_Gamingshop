from django.db import models
from django.contrib.auth.models import AbstractUser

# base_users
class User(AbstractUser):
    middle_name=models.CharField(max_length=100,blank=True)
    gender=models.CharField(max_length=30,blank=True)
    avatar=models.ImageField(upload_to="avatars/",blank=True,null=True)
    is_active=models.BooleanField(default=True)

# products
class Product(models.Model):
    name=models.CharField(max_length=180)
    description=models.TextField(blank=True)
    sku=models.CharField(max_length=60,unique=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField(default=0)
    thumbnail=models.ImageField(upload_to="products/",blank=True,null=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return self.name

# carts (one active cart per owner)
class Cart(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="carts")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return f"Cart #{self.pk} - {self.owner.username}"

# cart_products
class CartProduct(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_products")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="in_carts")
    quantity=models.PositiveIntegerField(default=1)
    class Meta: unique_together=("cart","product")
    def subtotal(self): return self.product.price*self.quantity

# transactions
class Transaction(models.Model):
    buyer=models.ForeignKey(User,on_delete=models.CASCADE,related_name="transactions")
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=30,default="pending")
    def __str__(self): return f"Order #{self.pk} - {self.buyer.username}"

# product_transactions
class ProductTransaction(models.Model):
    item=models.ForeignKey(Product,on_delete=models.PROTECT,related_name="order_lines")
    transaction=models.ForeignKey(Transaction,on_delete=models.CASCADE,related_name="product_transactions")
    quantity=models.PositiveIntegerField(default=1)
    unit_price=models.DecimalField(max_digits=10,decimal_places=2)

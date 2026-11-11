from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Product,Cart,CartProduct,Transaction,ProductTransaction
admin.site.register(User,UserAdmin)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
 list_display=("name","sku","price","stock","is_active")
 search_fields=("name","sku")
 list_filter=("is_active",)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Transaction)
admin.site.register(ProductTransaction)

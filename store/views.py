from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_POST
from .models import Product,Cart,CartProduct,Transaction,ProductTransaction
from .forms import RegisterForm

def home(request):
    products=Product.objects.filter(is_active=True).order_by("-created_at")
    return render(request,"store/home.html",{"products":products})

def register(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(); login(request,user)
            messages.success(request,"Account created. Welcome to ERD Shop!")
            return redirect("home")
    else: form=RegisterForm()
    return render(request,"store/register.html",{"form":form})

def _cart_for(user):
    cart,created=Cart.objects.get_or_create(owner=user)
    return cart

@login_required
@require_POST
def add_to_cart(request,product_id):
    product=get_object_or_404(Product,id=product_id,is_active=True)
    if product.stock<1:
        messages.error(request,"This product is out of stock.")
        return redirect("home")
    cart=_cart_for(request.user)
    line,created=CartProduct.objects.get_or_create(cart=cart,product=product,defaults={"quantity":1})
    if not created:
        if line.quantity < product.stock: line.quantity+=1; line.save()
        else: messages.warning(request,"You reached the available stock.")
    return redirect("cart")

@login_required
def cart(request):
    cart=_cart_for(request.user)
    lines=cart.cart_products.select_related("product")
    total=sum((line.product.price*line.quantity for line in lines),Decimal("0.00"))
    return render(request,"store/cart.html",{"lines":lines,"total":total})

@login_required
@require_POST
def update_cart(request,line_id):
    line=get_object_or_404(CartProduct,id=line_id,cart__owner=request.user)
    try: quantity=int(request.POST.get("quantity","1"))
    except ValueError: quantity=1
    if quantity<=0: line.delete()
    elif quantity<=line.product.stock: line.quantity=quantity;line.save()
    else: messages.error(request,f"Only {line.product.stock} item(s) are available.")
    return redirect("cart")

@login_required
@require_POST
def checkout(request):
    cart=_cart_for(request.user)
    lines=list(cart.cart_products.select_related("product"))
    if not lines:
        messages.warning(request,"Your cart is empty.");return redirect("cart")
    with transaction.atomic():
        for line in lines:
            product=Product.objects.select_for_update().get(pk=line.product_id)
            if line.quantity>product.stock:
                messages.error(request,f"Not enough stock for {product.name}.");return redirect("cart")
        order=Transaction.objects.create(buyer=request.user,status="paid")
        for line in lines:
            product=Product.objects.select_for_update().get(pk=line.product_id)
            ProductTransaction.objects.create(transaction=order,item=product,quantity=line.quantity,unit_price=product.price)
            product.stock-=line.quantity;product.save()
            line.delete()
    messages.success(request,f"Order #{order.pk} placed successfully!")
    return redirect("orders")

@login_required
def orders(request):
    qs=Transaction.objects.filter(buyer=request.user).prefetch_related("product_transactions__item").order_by("-created_at")
    return render(request,"store/orders.html",{"orders":qs})

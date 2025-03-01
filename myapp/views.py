from .models import Categories, Brands, Tags, Products, Cart, CartItem
from django.shortcuts import render, get_object_or_404, redirect
from .forms import LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse




def shop(request):
    products = Products.objects.all()  # Tüm ürünleri çek
    return render(request, 'index.html', {'products': products})

def productdetail(request, slug):
    product = get_object_or_404(Products, slug=slug)
    return render(request, "product.html", {"product": product})

def categoriesdetail(request, slug):
    print(f"Slug değeri: {slug}")

    if not slug:  # Eğer slug None veya boşsa hata mesajı döndür
        return redirect('/')



    category = get_object_or_404(Categories, slug=slug)
    products = Products.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'products': products})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Başarıyla kayıt oldunuz!")
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        username = request.POST.get('email')  # Kullanıcı email veya username ile giriş yapabilir
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def add_to_cart(request, product_id):
    if isinstance(request.user, AnonymousUser):
        return redirect('login')  # Kullanıcı giriş yapmamışsa login sayfasına yönlendir

    product = get_object_or_404(Products, id=product_id)
    
    # Kullanıcıya özel sepeti kontrol et
    cart, created = Cart.objects.get_or_create(user=request.user)  # Sepet kullanıcıya özel
    
    # Ürünü sepete ekle veya miktarını artır
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    print(f"✅ {request.user} - Sepete eklendi: {product.name} - Adet: {cart_item.quantity}")
    
    
    return redirect('cart_detail') 



def cart_detail(request):
    if isinstance(request.user, AnonymousUser):
        return redirect('login')  # Kullanıcı giriş yapmamışsa login sayfasına yönlendir

    # Kullanıcıya özel sepeti al
    cart, created = Cart.objects.get_or_create(user=request.user)  # Sepet kullanıcıya özel
    cart_items = CartItem.objects.filter(cart=cart)  # Sepetteki tüm ürünleri al
    cart_items_count = cart_items.count()  # Sepetteki ürün sayısını al
    
    print(f"User: {request.user}, Cart ID: {cart.id}, Cart Items: {cart_items.count()}") 
    return render(request, 'cart_detail.html', {
        'cart_items': cart_items, 
        'cart_items_count': cart_items_count
    })



def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_detail')

def update_cart(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if action == "increase":
        item.quantity += 1
    elif action == "decrease" and item.quantity > 1:
        item.quantity -= 1

    item.save()
    return redirect('cart_detail')

def clear_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart.cartitem_set.all().delete()  # Tüm ürünleri sil
    return redirect('cart_detail')

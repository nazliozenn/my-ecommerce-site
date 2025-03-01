"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import shop, productdetail, categoriesdetail, register_view, login_view,add_to_cart, cart_detail,remove_from_cart,update_cart,clear_cart
from myapp import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', shop,name='shop'),
    path('product/<slug:slug>/',productdetail,name="productdetail"),
    path('categori/<slug:slug>/',categoriesdetail, name='categoriesdetail'),
    path('register/', register_view, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', login_view, name='login'), 
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),

    path('cart/', cart_detail, name='cart_detail'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/<str:action>/', update_cart, name='update_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),




] +static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

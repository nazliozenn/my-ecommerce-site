from django.contrib import admin
from .models import Categories , Brands ,Products ,Tags,Variations
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


# Register your models here.


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name','seo_title','slug','stock']
    list_filter  = ['stock']
    list_fields  = ['name','seo_title','slug']

admin.site.register(Categories,CategoriesAdmin)



class BrandsAdmin(admin.ModelAdmin):
    list_display = ['name','seo_title','slug','stock']
    list_filter  = ['stock','name']
    list_fields  = ['name','seo_title','slug']

admin.site.register(Brands,BrandsAdmin) 

class InlineVariations(admin.TabularInline):
    model = Variations
    extra = 1
    fields = ['variation', 'price', 'stock', 'image']

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name','price','discountedprice','image','date','brand','seo_title','slug','stock']
    list_filter  = ['stock','name','brand']
    list_fields  = ['name','seo_title','slug']
    inlines = [InlineVariations]
    

admin.site.register(Variations)  

admin.site.register(Products,ProductsAdmin) 

admin.site.register(Tags)

if admin.site.is_registered(User):
    admin.site.unregister(User)  # Önce kaydı kaldır

class CustomUserAdmin(DefaultUserAdmin):  # Django'nun default UserAdmin'ini genişlet
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff')

admin.site.register(User, CustomUserAdmin) 
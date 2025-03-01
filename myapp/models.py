from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=155)
    stock = models.BooleanField(default=True)
    comment = models.TextField(blank=True,null=True)
    uppercategories = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, help_text="If this category is connected to another category, you have filled it out.")
    seo_title = models.CharField(max_length=155, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=155, unique=True, null=True, blank=True)
    showinmenu = models.BooleanField(default=True)




    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"

    def __str__(self):
        return self.name
    

class Brands(models.Model):
    name = models.CharField(max_length=155)
    comment = models.TextField(blank=True,null=True)
    seo_title = models.CharField(max_length=155, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=155, unique=True, null=True, blank=True)
    stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to="brandimage",blank=True,null=True)

    class Meta:
        verbose_name_plural = "Brands"
        verbose_name = "Brand"

    def __str__(self):
        return self.name
    
class Tags(models.Model):
    name = models.CharField(max_length=155)
    slug = models.SlugField(max_length=155, unique=True, null=True, blank=True)
    stock = models.BooleanField(default=True)


    class Meta:
        verbose_name_plural = "Tags"
        verbose_name = "Tag"

    def __str__(self):
        return self.name




class Products(models.Model):
    name = models.CharField(max_length=155)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands,on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, blank=True)

    price = models.DecimalField(max_digits=10,decimal_places=2)
    discountedprice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    comment = models.TextField(blank=True,null=True)
    seo_title = models.CharField(max_length=155, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=155, unique=True, null=True, blank=True)
    stock = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tags,blank=True,)
    image = models.ImageField(upload_to='products/', null=True, blank=True)


    class Meta:
        verbose_name_plural = "Products"
        verbose_name = "Product"

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        return self.slug
           


class Variations(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    variation = models.CharField(max_length=155)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to="variationimages", null=True, blank=True)


    class Meta:
        verbose_name_plural = "Variations"
        verbose_name = "variation"

    def __str__(self):
        return self.variation
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
   

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"
   
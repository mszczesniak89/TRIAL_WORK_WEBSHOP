from django.conf import settings
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe


class Category(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to="category_images/")

    class Meta:
        verbose_name_plural = '1. Categories'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.image.url)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to="manufacturer_images/")

    class Meta:
        verbose_name_plural = '2. Manufacturers'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    price = models.PositiveIntegerField(default=0)
    slug = models.CharField(max_length=512)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images/", null=True)
    availability = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '3. Products'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.image.url)

    def get_detail_url(self):
        return reverse('product-details', args=(self.pk,))

    def __str__(self):
        return self.name


status_choice = (
    ('process', 'In Process'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)


class ShoppingCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_amt = models.FloatField()
    paid_status = models.BooleanField(default=False)
    order_dt = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=status_choice, default='process', max_length=150)

    class Meta:
        verbose_name_plural = '4. Orders'


class ShoppingCartItems(models.Model):
    order = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=128)
    item = models.CharField(max_length=128)
    image = models.CharField(max_length=256)
    qty = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()

    class Meta:
        verbose_name_plural = '5. Order Items'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % self.image)

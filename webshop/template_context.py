from .models import Product
from django.db.models import Min, Max


def get_filters(request):
    categories = Product.objects.distinct().values('category__name', 'category__id')
    manufacturers = Product.objects.distinct().values('manufacturer__name', 'manufacturer__id')
    price_range = Product.objects.aggregate(Min('price'), Max('price'))
    data = {
        'categories': categories,
        'manufacturers': manufacturers,
        'price_range': price_range,
    }
    return data

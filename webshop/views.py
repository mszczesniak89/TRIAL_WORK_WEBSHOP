from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import DetailView
from django_filters.views import FilterView
from webshop.models import Product, ShoppingCart, ShoppingCartItems
from webshop.filters import ProductFilter


class HomePageView(View):
    def get(self, request):
        response = render(request, 'webshop/home_page.html', )
        return response


class MainShopView(FilterView):
    def get_queryset(self):
        return Product.objects.all()

    model = Product
    context_object_name = 'object_list'
    filterset_class = ProductFilter
    template_name = 'webshop/main.html'


class ProductDetailsView(DetailView):
    model = Product
    template_name = 'webshop/product_details.html'


def add_to_cart(request):
    cart_p = {}
    cart_p[str(request.GET['item_id'])] = {
        'qty': request.GET['qty'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['item_id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['item_id'])]['qty'] = cart_data[str(request.GET['item_id'])]['qty'] + int(
                cart_p[str(request.GET['item_id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})

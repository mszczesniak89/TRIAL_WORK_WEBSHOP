from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import DetailView, ListView
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
    cart_p = {str(request.GET['item_id']): {
        'qty': request.GET['qty'],
    }}
    if 'cartdata' in request.session:
        if str(request.GET['item_id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['item_id'])]['qty'] = int(cart_data[str(request.GET['item_id'])]['qty']) + int(
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


def shopping_cart_list(request):
    total_amt = 0
    object_list = {}
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            product = Product.objects.filter(id=p_id).values()
            item['product'] = list(product)
            total_amt += int(item['qty']) * float(product[0]['price'])
        return render(request, 'webshop/cart.html',
                      {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']),
                       'total_amt': total_amt})
    else:
        return render(request, 'webshop/cart.html', {'cart_data': '', 'totalitems': 0, 'total_amt': total_amt})


def delete_cart_item(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata'] = cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        product = Product.objects.filter(id=p_id).values()
        item['product'] = list(product)
        total_amt += int(item['qty']) * float(product[0]['price'])
    data = render_to_string('ajax/cart-list.html',
                            {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']),
                             'total_amt': total_amt})
    return JsonResponse(
        {'data': data, 'totalitems': len(request.session['cartdata'])})


def update_cart_item(request):
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            request.session['cartdata'] = cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        product = Product.objects.filter(id=p_id).values()
        item['product'] = list(product)
        total_amt += int(item['qty']) * float(product[0]['price'])
    data = render_to_string('ajax/cart-list.html',
                            {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']),
                             'total_amt': total_amt})
    return JsonResponse({'data': data, 'totalitems': len(request.session['cartdata'])})

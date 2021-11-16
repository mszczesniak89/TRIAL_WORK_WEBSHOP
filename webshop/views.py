from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from django_filters.views import FilterView
from webshop.models import Product, ShoppingCart, ShoppingCartItems, Manufacturer, Category
from webshop.filters import ProductFilter
from webshop.forms import AddProductForm, EditProductForm, AddCategoryForm, AddManufacturerForm


class HomePageView(View):
    def get(self, request):
        response = render(request, 'webshop/home_page.html', )
        return response


class ContactView(View):
    def get(self, request):
        response = render(request, 'webshop/contact.html', )
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


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = AddProductForm
    template_name = 'webshop/add_product_2.html'

    def get_success_url(self):
        return reverse_lazy('product-details', kwargs={'pk': self.object.id})


class AdminProductView(UserPassesTestMixin, FilterView):
    def get_queryset(self):
        return Product.objects.all()

    model = Product
    context_object_name = 'object_list'
    filterset_class = ProductFilter
    template_name = 'webshop/admin_products.html'

    def test_func(self):
        return self.request.user.is_staff


class AdminEditProduct(UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'webshop/edit_product.html'
    form_class = EditProductForm

    def get_success_url(self):
        return reverse_lazy('admin-products')

    def test_func(self):
        return self.request.user.is_staff


class AdminDeleteProduct(UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'webshop/delete_form.html'

    def get_success_url(self):
        return reverse_lazy('admin-products')

    def test_func(self):
        return self.request.user.is_staff


class ManufacturerCreateModalView(UserPassesTestMixin, BSModalCreateView):
    template_name = 'webshop/create_manufacturer_modal.html'
    form_class = AddManufacturerForm
    success_url = reverse_lazy('main-page')

    def test_func(self):
        return self.request.user.is_staff

    # def form_valid(self, form):
    #     if not self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #         return super().form_valid(form)
    #     else:
    #         return super().form_invalid(form)


class CategoryCreateModalView(UserPassesTestMixin, BSModalCreateView):
    template_name = 'webshop/create_category_modal.html'
    form_class = AddCategoryForm
    success_url = reverse_lazy('main-page')

    def test_func(self):
        return self.request.user.is_staff

    # def form_valid(self, form):
    #     if not self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #         return super().form_valid(form)
    #     else:
    #         return super().form_invalid(form)


class CheckoutView(View):
    def get(self, request):
        response = render(request, 'webshop/checkout.html', )
        return response


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


def manufacturers(request):
    data = dict()
    if request.method == 'GET':
        objects = Manufacturer.objects.all()
        data['table'] = render_to_string('ajax/manufacturer.html', {'objects': objects}, request=request)
        return JsonResponse(data)


def categories(request):
    data = dict()
    if request.method == 'GET':
        objects = Category.objects.all()
        data['table'] = render_to_string('ajax/category.html', {'objects': objects}, request=request)
        return JsonResponse(data)

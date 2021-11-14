"""TRIAL_WORK_WEBSHOP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from webshop.views import HomePageView, MainShopView, ProductDetailsView, add_to_cart, shopping_cart_list, \
    delete_cart_item, update_cart_item, AddProductView, AdminProductView, AdminDeleteProduct, AdminEditProduct


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', HomePageView.as_view(), name='home-page'),
    path('main', MainShopView.as_view(), name='main-page'),
    path('admin_products/', AdminProductView.as_view(), name='admin-products'),
    path('admin_delete_product/<int:pk>/', AdminDeleteProduct.as_view(), name='admin-delete-product'),
    path('admin_edit_product/<int:pk>/', AdminEditProduct.as_view(), name='admin-edit-product'),
    path('product/<int:pk>/', ProductDetailsView.as_view(), name='product-details'),
    path('add-product/', AddProductView.as_view(), name='add-product'),
    path('add-to-cart', add_to_cart, name='add-to-cart'),
    path('update-cart', update_cart_item, name='update-cart'),
    path('delete-from-cart', delete_cart_item, name='delete-from-cart'),
    path('shopping_cart', shopping_cart_list, name='shopping-cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

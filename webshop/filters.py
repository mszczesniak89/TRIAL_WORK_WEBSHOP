from datetime import datetime

import django_filters
from django.db.models import Q
from django_filters import ModelChoiceFilter, ChoiceFilter, CharFilter, NumericRangeFilter, RangeFilter, \
    widgets, DateFilter, OrderingFilter
from django import forms
from django_filters.widgets import RangeWidget

from webshop.models import Product, ShoppingCart, ShoppingCartItems


class ProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='my_custom_filter', label='SEARCH',
                                  widget=forms.TextInput(attrs={'size': 22, 'placeholder': 'insert name/product code'}))
    o = OrderingFilter(
        fields=(
            ('name', 'name'),
            ('price', 'price'),
        ),

        field_labels={
            'name': 'Name',
        }
    )

    class Meta:
        model = Product
        fields = ['q']

    def my_custom_filter(self, queryset, name, value):
        return Product.objects.filter(
            Q(name__icontains=value) | Q(id__icontains=value)
        )

from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from webshop.models import Product, Manufacturer, Category


class AddProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'details': forms.Textarea(attrs={'placeholder': 'Additional details...', 'rows': 3, 'cols': 20}),
            'slug': forms.TextInput(attrs={'placeholder': 'Slug..'}),
            'name': forms.TextInput(attrs={'placeholder': 'Product name..'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))


class EditProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'details': forms.Textarea(attrs={'rows': 3, 'cols': 20})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))


class AddManufacturerForm(BSModalModelForm):

    class Meta:
        model = Manufacturer
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Manufacturer name...'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddManufacturerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'


class AddCategoryForm(BSModalModelForm):

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Category name...'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddCategoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'



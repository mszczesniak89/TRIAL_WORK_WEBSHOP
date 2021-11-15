from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from webshop.models import Product


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




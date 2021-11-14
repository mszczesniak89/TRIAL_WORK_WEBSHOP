from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from webshop.models import Product


class AddProductForm(forms.ModelForm):

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




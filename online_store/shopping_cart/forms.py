from django.forms import ModelForm, TextInput, Textarea
from shopping_cart.models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['phone', 'address']
        widgets = {
            'phone': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'address': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter address'
            })
        }

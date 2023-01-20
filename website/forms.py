from django.forms import ModelForm, TextInput, RadioSelect

from website.models import Order


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = '__all__'

        widgets = {
            'client_name': TextInput(attrs={'class': 'order__form_input', 'name': 'fname', 'type': 'text', 'placeholder': 'Введите Имя', 'required': True}),
            'phonenumber': TextInput(attrs={'class': 'order__form_input', 'name': 'tel', 'type': 'text',
                                            'placeholder': '+ 7 (999) 000 00 00', 'required': True}),
            'address': TextInput(attrs={'class': 'order__form_input', 'name': 'adres', 'type': 'text', 'placeholder': 'Адрес доставки', 'required': True}),
            'bouquet': TextInput(attrs={'type': 'hidden'}),
            'order_status': TextInput(attrs={'type': 'hidden'}),
            'created_at': TextInput(attrs={'type': 'hidden'}),
            'updated_at': TextInput(attrs={'type': 'hidden'}),
            'delivery_time': RadioSelect(attrs={'class': 'order__form_radio', 'name': 'orderTime', 'type': 'radio'}),
        }

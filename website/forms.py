from django.forms import ModelForm, TextInput, RadioSelect, CharField, IntegerField, EmailField

from website.models import Order, CallBack, PaymentOrder


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


class CallBackForm(ModelForm):
    class Meta:
        model = CallBack
        exclude = ['florist', 'status']


class PaymentForm(ModelForm):
    card_number = CharField(widget=TextInput(attrs={'placeholder': 'Введите номер'}))
    card_month = CharField(widget=TextInput(attrs={'placeholder': 'ММ'}))
    card_year = CharField(widget=TextInput(attrs={'placeholder': 'ГГ'}))
    card_holder = CharField(widget=TextInput(attrs={'placeholder': 'Имя владельца'}))
    card_cvc = CharField(widget=TextInput(attrs={'placeholder': 'CVC'}))
    email = EmailField(widget=TextInput(attrs={'placeholder': 'pochta@mail.ru'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'order__form_input orderStep_form_input'

    class Meta:
        model = PaymentOrder
        fields = ['card_number', 'card_month', 'card_year', 'card_holder', 'card_cvc', 'email']

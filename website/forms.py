import re

from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, RadioSelect, CharField, IntegerField, EmailField

from website.models import Order, CallBack, PaymentOrder


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

        widgets = {
            'client_name': TextInput(
                attrs={'class': 'order__form_input', 'name': 'fname', 'type': 'text', 'placeholder': 'Введите Имя',
                       'required': True}),
            'phonenumber': TextInput(attrs={'class': 'order__form_input', 'name': 'tel', 'type': 'text',
                                            'placeholder': '+ 7 (999) 000 00 00', 'required': True}),
            'address': TextInput(
                attrs={'class': 'order__form_input', 'name': 'adres', 'type': 'text', 'placeholder': 'Адрес доставки',
                       'required': True}),
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


def validate_card_number(value):
    if not re.match(r'^[0-9]{12,19}$', value):
        raise ValidationError('Не верный номер карты')


def validate_card_month(value):
    if not re.match(r'^\d\d$', value) or not 0 < int(value) <= 12:
        raise ValidationError('Не верный месяц')


def validate_card_year(value):
    if not re.match(r'^\d\d$', value) or not 23 <= int(value) < 99:
        raise ValidationError('Не верный год')


def validate_card_holder(value):
    if not re.match(r'^[a-zA-Z\s]{1,26}$', value):
        raise ValidationError('Не верное имя держателя карты')


def validate_card_cvc(value):
    if not re.match(r'^\d{3,4}$', value):
        raise ValidationError('Не верный код CVC')


class PaymentForm(ModelForm):
    card_number = CharField(validators=[validate_card_number], widget=TextInput(attrs={'placeholder': 'Введите номер'}))
    card_month = CharField(validators=[validate_card_month], widget=TextInput(attrs={'placeholder': 'ММ'}))
    card_year = CharField(validators=[validate_card_year], widget=TextInput(attrs={'placeholder': 'ГГ'}))
    card_holder = CharField(validators=[validate_card_holder], widget=TextInput(attrs={'placeholder': 'Имя владельца'}))
    card_cvc = CharField(validators=[validate_card_cvc], widget=TextInput(attrs={'placeholder': 'CVC'}))
    email = EmailField(widget=TextInput(attrs={'placeholder': 'pochta@mail.ru'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'order__form_input orderStep_form_input'

    class Meta:
        model = PaymentOrder
        fields = ['card_number', 'card_month', 'card_year', 'card_holder', 'card_cvc', 'email']

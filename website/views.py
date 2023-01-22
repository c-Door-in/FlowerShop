import uuid

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from telegram import Bot

from django.conf import settings
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from yookassa import Payment

from users.models import User
from utm.views import check_utm

from website.forms import OrderForm, CallBackForm, PaymentForm
from website.models import Event, Bouquet, Order, CallBack, PaymentOrder


def send_tg_message(text, tg_chat_id):
    bot_api_key = settings.BOT_API_KEY
    try:
        bot = Bot(token=bot_api_key)
        bot.send_message(text=text, chat_id=tg_chat_id)
    except Exception as err:
        print(err)
        return False
    return True


def inform_florist(callback):
    florist_tg_chat_id = callback.florist.tg_chat_id
    client_name = callback.client_name
    phonenumber = callback.phonenumber

    text = f'''
        Запрос на обратный звонок от FlowerShop
        Имя: {client_name}
        Номер телефона: {phonenumber}'''

    return send_tg_message(text, florist_tg_chat_id)


def inform_courier(delivery):
    courier_tg_chat_id = delivery.courier.tg_chat_id

    bouquet = bouquet
    client_name = delivery.order.client_name
    address = delivery.order.address
    phonenumber = delivery.order.phonenumber
    delivery_time = delivery.order.delivery_time
    created_at = delivery.order.created_at

    text = f'''
        Заказ на доставку от FlowerShop
        Букет: {bouquet}
        Имя: {client_name}
        Адрес: {address}
        Номер телефона: {phonenumber}
        Ожидаемое время доставки: {delivery_time}
        Принят: {created_at}'''

    return send_tg_message(text, courier_tg_chat_id)


def get_bouquets_catalog(bouquets):
    catalog = []
    catalog_line = []

    for index, bouquet in enumerate(bouquets):
        if index and index % 3 == 0:
            catalog.append(catalog_line)
            catalog_line = []
        catalog_line.append(bouquet)
    catalog.append(catalog_line)

    return catalog


def mainpage(request):
    check_utm(request)

    bouquets = Bouquet.objects.all().order_by('?')
    florist = User.objects.filter(role='FL')[0]
    callback = CallBack(florist=florist)

    catalog = get_bouquets_catalog(bouquets)
    first_line_bouquets = catalog[0]

    callbackform = CallBackForm(request.POST, instance=callback)
    context = {
        'catalog_line': first_line_bouquets,
        'form': callbackform,
    }
    if request.method == 'POST':
        if not callbackform.is_valid():
            return render(request, 'consultation.html', context)
        callbackform.save()
        florist_informed = inform_florist(callback)
        context['florist_informed'] = florist_informed
        return render(request, 'consult_confirm.html', context)

    return render(request, 'index.html', context)


def catalog(request):
    bouquets = Bouquet.objects.all()
    catalog = get_bouquets_catalog(bouquets)
    context = {
        'catalog': catalog
    }

    return render(request, 'catalog.html', context)


def consultation(request):
    florist = User.objects.filter(role='FL')[0]
    callback = CallBack(florist=florist)
    callbackform = CallBackForm(request.POST, instance=callback)
    context = {
        'form': callbackform,
    }
    if request.method == 'POST':
        if callbackform.is_valid():
            callbackform.save()
            florist_informed = inform_florist(callback)
            context['florist_informed'] = florist_informed
            return render(request, 'consult_confirm.html', context)
    return render(request, 'consultation.html', context)


class CardView(DetailView):
    model = Bouquet
    template_name = 'card.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CallBackForm()
        return context


def order(request, pk):
    bouquet = get_object_or_404(Bouquet, pk=pk)
    if request.method == 'POST':
        order_form = OrderForm(request.POST, initial={'bouquet': bouquet})

        if order_form.is_valid():
            form = order_form.save(commit=False)
            form.save()

            return HttpResponseRedirect(reverse('order_step', kwargs={'pk': form.pk}))
    else:
        order_form = OrderForm(initial={'bouquet': bouquet})

    context = {
        'bouquet': bouquet,
        'order_form': order_form,
    }
    return render(request, 'order.html', context)


def order_step(request, pk):
    order_obj = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        card_year = f"20{payment_form.data['card_year']}"
        card_month = payment_form.data['card_month']
        card_holder = payment_form.data['card_holder']
        cvc = payment_form.data['card_cvc']
        if payment_form.is_valid():
            form = payment_form.save(commit=False)
            card_number = form.card_number
            form.card_number = form.card_number[-4:]
            form.order = order_obj
            cost = order_obj.bouquet.price
            payment_payload = {
                "amount": {
                    "value": str(cost),
                    "currency": "RUB"
                },
                "payment_method_data": {
                    "type": "bank_card",
                    "card": {
                        "cardholder": card_holder,
                        "csc": cvc,
                        "expiry_month": card_month,
                        "expiry_year": card_year,
                        "number": card_number
                    }
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": reverse('confirm_pay', kwargs={'pk': pk})
                },
                "description": form.order
            }
            payment = Payment.create(payment_payload)
            payment_confirmation = payment.confirmation.confirmation_url
            payment_id = payment.id
            form.payment_id = payment_id

            form.save()

            return HttpResponseRedirect(payment_confirmation)
    else:
        payment_form = PaymentForm()
    context = {
        'order_pk': order_obj.pk,
        'payment_form': payment_form
    }
    return render(request, 'order-step.html', context)


def quiz(request):
    if request.method == 'POST':
        post_params = request.POST.get('userResponses').split(',')

        if post_params[1] == 'До 1000 Руб.':
            query = Q(event__name=post_params[0]) & Q(price__lt=1000)
        elif post_params[1] == '1000-5000 Руб.':
            query = Q(event__name=post_params[0]) & Q(price__gte=1000) & Q(price__lte=5000)
        elif post_params[1] == 'Свыше 5000 Руб.':
            query = Q(event__name=post_params[0]) & Q(price__gt=5000)
        elif post_params[1] == 'Не имеет значения':
            query = Q(event__name=post_params[0])

        bouquets = Bouquet.objects.filter(query)

        context = {
            'bouquets': bouquets
        }

        return render(request, 'result.html', context)

    events = Event.objects.all()

    context = {
        'events': events,
    }

    return render(request, 'quiz.html', context)


def quiz_step(request):
    return render(request, 'quiz-step.html')


def result(request):
    return render(request, 'result.html')


def consultation_form(request):
    user_name = request.POST.get('fname')
    user_phone = request.POST.get('tel')

    bot_api_key = settings.BOT_API_KEY
    if bot_api_key:
        bot = Bot(token=bot_api_key)
        florist_chat_id = settings.FORIST_CHAT_ID
        if florist_chat_id:
            bot.send_message(text=f'{user_name}, {user_phone}', chat_id=florist_chat_id)

    print(user_name, user_phone)
    return render(request, 'consult_confirm.html')


def confirm_pay(request, pk):
    order_obj = get_object_or_404(Order, pk=pk)
    cost = order_obj.bouquet.price
    payment = PaymentOrder.objects.filter(order=order_obj).first()
    payment_id = payment.payment_id
    idempotence_key = str(uuid.uuid4())
    response = Payment.capture(
        payment_id,
        {
            "amount": {
                "value": cost,
                "currency": "RUB"
            }
        },
        idempotence_key
    )

    if response.status == 'succeeded':
        payment.status = PaymentOrder.SUCCESS
        payment.save()
    return render(request, 'compete_payment.html')

import uuid

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from telegram import Bot

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from yookassa import Payment

from users.models import User

from website.forms import OrderForm, CallBackForm, PaymentForm
from website.models import Event, Bouquet, Order, CallBack, PaymentOrder


def inform_florist(callback):
    tg_chat_id = callback.florist.tg_chat_id
    client_name = callback.client_name
    phonenumber = callback.phonenumber

    bot_api_key = settings.BOT_API_KEY
    text = f'''
    Запрос на обратный звонок от FlowerShop
    Имя: {client_name}
    Номер телефона: {phonenumber}'''

    try:
        bot = Bot(token=bot_api_key)
        bot.send_message(text=text, chat_id=tg_chat_id)
    except Exception as err:
        print(err)
        return False
    return True


def mainpage(request):
    florist = User.objects.filter(role='FL')[0]
    callback = CallBack(florist=florist)
    callbackform = CallBackForm(request.POST, instance=callback)
    context = {
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
    return render(request, 'catalog.html')


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


def contacts(request):
    return render(request, 'index.html')


def card(request):
    return render(request, 'card.html')


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

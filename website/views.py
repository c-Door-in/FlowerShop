from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from telegram import Bot

from django.conf import settings
from django.shortcuts import render

from users.models import User
from utm.views import check_utm

from website.forms import OrderForm, CallBackForm
from website.models import Event, Bouquet, Order, CallBack


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

    check_utm(request)

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


def order(request):

    try:
        bouquet_id = request.GET['BouquetOrder']
        bouquet = Bouquet.objects.get(pk=bouquet_id)

        order_form = OrderForm(initial={'bouquet': bouquet})

        context = {
            'bouquet': bouquet,
            'order_form': order_form,
        }
        return render(request, 'order.html', context)
    except MultiValueDictKeyError:
        pass

    return render(request, 'order.html')


def order_step(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            form = order_form.save(commit=False)
            bouquet_id = form.bouquet
            form.save()
            context = {
                'bouquet_id': bouquet_id.pk
            }
            return render(request, 'order-step.html', context)
        else:
            context = {
                'order_form': order_form,
            }
            return render(request, 'order.html', context)

    return render(request, 'order-step.html')


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
    
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from telegram import Bot

from django.conf import settings
from django.shortcuts import render

from website.forms import OrderForm
from website.models import Event, Bouquet, Order


def mainpage(request):
    return render(request, 'index.html')


def catalog(request):
    return render(request, 'catalog.html')


def consultation(request):
    return render(request, 'consultation.html')


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
    
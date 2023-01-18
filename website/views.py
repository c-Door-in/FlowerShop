from django.shortcuts import render


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
    return render(request, 'order.html')


def order_step(request):
    return render(request, 'order-step.html')


def quiz(request):
    return render(request, 'quiz.html')


def quiz_step(request):
    return render(request, 'quiz-step.html')


def result(request):
    return render(request, 'result.html')


def consultation_form(request):
    user_name = request.POST.get('fname')
    user_phone = request.POST.get('tel')
    print(user_name, user_phone)
    return render(request, 'consult_confirm.html')
    
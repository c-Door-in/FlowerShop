from django.urls import path

from . import views


urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('catalog/', views.catalog, name='catalog'),
    path('consultation/', views.consultation, name='consultation'),
    path('contacts/', views.contacts, name='contacts'),
    path('card/', views.card, name='card'),
    path('order/', views.order, name='order'),
    path('order-step/', views.order_step, name='order_step'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz-step/', views.quiz_step, name='quiz_step'),
    path('result/', views.result, name='result'),
    path('consultation_form/', views.consultation_form, name='consultation_form'),
]


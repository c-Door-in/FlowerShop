from django.urls import path

from . import views


urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('catalog/', views.catalog, name='catalog'),
    path('consultation/', views.consultation, name='consultation'),
    path('contacts/', views.consultation, name='contacts'),
    path('card/<int:pk>', views.CardView.as_view(), name='card'),
    path('contacts/', views.consultation, name='contacts'),
    path('order/<int:pk>', views.order, name='order'),
    path('order-step/<int:pk>', views.order_step, name='order_step'),
    path('quiz/', views.quiz, name='quiz'),
    path('confirm_pay/<int:pk>/', views.confirm_pay, name='confirm_pay'),
]


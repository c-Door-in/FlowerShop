from django.urls import path

from . import views


urlpatterns = [
    path('', views.statistic_main, name='statistic_main'),
]


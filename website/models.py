from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.models import User


class Event(models.Model):
    """Модель сущности Событие"""
    name = models.CharField(max_length=128, verbose_name='Наименование события')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


class Flower(models.Model):
    """Модель сущности Цветок"""
    name = models.CharField(max_length=128, verbose_name='Наименование цветка')
    flower_color = models.CharField(max_length=128, blank=True, verbose_name='Цвет цветка')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена', validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Цветок'
        verbose_name_plural = 'Цветы'


class Decoration(models.Model):
    """Модель сущности Украшение букета"""
    name = models.CharField(max_length=128, verbose_name='Наименование украшения')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена', validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Украшение'
        verbose_name_plural = 'Украшения'


class Bouquet(models.Model):
    """Модель сущности Букет"""
    flowers = models.ManyToManyField(Flower, related_name='bouquets', through='FlowerItem', verbose_name='Цветы')
    decorations = models.ManyToManyField(Decoration,
                                         related_name='bouquets',
                                         through='DecorationItem',
                                         verbose_name='Украшения'
                                         )
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена', validators=[MinValueValidator(0)])
    event = models.ForeignKey(Event,
                              related_name='bouquets',
                              null=True,
                              on_delete=models.SET_NULL,
                              verbose_name='Событие'
                              )
    image = models.ImageField(upload_to='bouquets', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'


class FlowerItem(models.Model):
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE, verbose_name='Букет')
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, verbose_name='Цветок')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])


class DecorationItem(models.Model):
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE, verbose_name='Букет')
    decoration = models.ForeignKey(Decoration, on_delete=models.CASCADE, verbose_name='Украшение')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])


class Order(models.Model):
    """Модель сущности Заказ"""
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE, related_name='orders', verbose_name='Букет')
    client_name = models.CharField(max_length=128, verbose_name='Имя клиента')
    address = models.TextField(verbose_name='Адрес')
    phonenumber = PhoneNumberField(verbose_name='Телефон')
    delivery_time = models.TimeField(verbose_name='Время доставки', db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class CallBack(models.Model):
    """Модель сущности Обратный звонок"""
    florist = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='callbacks',
                                verbose_name='Флорист')
    client_name = models.CharField(max_length=128, verbose_name='Имя клиента')
    phonenumber = PhoneNumberField(verbose_name='Телефон')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Обратный звонок'
        verbose_name_plural = 'Обратные звонки'


class Delivery(models.Model):
    """Модель сущности Доставка"""
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='deliveries',
                              verbose_name='Заказ'
                              )
    courier = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='deliveries',
                                verbose_name='Курьер'
                                )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    delivered_at = models.DateTimeField(verbose_name='Время доставки', db_index=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'

from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.models import User


class Event(models.Model):
    """Модель сущности Событие"""
    name = models.CharField(max_length=128, verbose_name='Наименование события')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


class Bouquet(models.Model):
    """Модель сущности Букет"""
    name = models.CharField(max_length=128, default='Букет', verbose_name='Наименование')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена', validators=[MinValueValidator(0)])
    event = models.ForeignKey(Event,
                              related_name='bouquets',
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              verbose_name='Событие'
                              )
    image = models.ImageField(upload_to='bouquets', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    composition = models.TextField(default='Состав:', verbose_name='Состав')
    size = models.TextField(default='Ширина: Высота:', verbose_name='Размер')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'


class Order(models.Model):
    """Модель сущности Заказ"""
    ACCEPT = 'AC'
    ASSEMBLY = 'AS'
    DELIVERY = 'DL'
    FINISH = 'FN'

    STATUS_ORDER_CHOICES = [
        (ACCEPT, 'Принят'),
        (ASSEMBLY, 'Сборка'),
        (DELIVERY, 'Доставка'),
        (FINISH, 'Завершен')
    ]

    QUICLY = 'QLY'
    FIRST_PERIOD = 'FRS'
    SECOND_PERIOD = 'SEC'
    THIRD_PERIOD = 'THR'
    FOURTH_PERIOD = 'FOU'
    FIFTH_PERIOD = 'FIF'

    DELIVERY_PERIOD_CHOICES = [
        (QUICLY, 'Как можно скорее'),
        (FIRST_PERIOD, 'с 10:00 до 12:00'),
        (SECOND_PERIOD, 'с 12:00 до 14:00'),
        (THIRD_PERIOD, 'с 14:00 до 16:00'),
        (FOURTH_PERIOD, 'с 16:00 до 18:00'),
        (FIFTH_PERIOD, 'с 18:00 до 20:00')
    ]

    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE, related_name='orders', verbose_name='Букет')
    client_name = models.CharField(max_length=128, verbose_name='Имя клиента')
    address = models.TextField(verbose_name='Адрес')
    phonenumber = PhoneNumberField(verbose_name='Телефон')
    delivery_time = models.CharField(
        max_length=3,
        choices=DELIVERY_PERIOD_CHOICES,
        default=QUICLY,
        verbose_name='Время доставки',
        db_index=True
    )
    order_status = models.CharField(max_length=2, choices=STATUS_ORDER_CHOICES,
                                    default=ACCEPT, verbose_name='Статус заказа', db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    def __str__(self):
        return f'{self.pk} - {self.bouquet}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class CallBack(models.Model):
    """Модель сущности Обратный звонок"""
    NEW = 'NW'
    CALLED = 'CD'
    FINISH = 'FN'

    STATUS_CHOICES = [
        (NEW, 'Новый'),
        (CALLED, 'Совершен звонок'),
        (FINISH, 'Завершен')
    ]

    florist = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='callbacks',
                                verbose_name='Флорист')
    client_name = models.CharField(max_length=128, verbose_name='Имя клиента')
    phonenumber = PhoneNumberField(verbose_name='Телефон')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default=NEW, verbose_name='Статус', db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return f'{self.client_name} - {self.phonenumber}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Обратный звонок'
        verbose_name_plural = 'Обратные звонки'


class Delivery(models.Model):
    """Модель сущности Доставка"""
    NEW = 'NW'
    PROCESSING = 'PR'
    FINISH = 'FN'

    STATUS_CHOICES = [
        (NEW, 'Новая доставка'),
        (PROCESSING, 'Доставляется'),
        (FINISH, 'Завершена доставка')
    ]
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
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default=NEW, verbose_name='Статус', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    delivered_at = models.DateTimeField(blank=True, null=True, verbose_name='Фактическое время доставки', db_index=True)

    def __str__(self):
        return f'{self.order} - {self.courier}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'

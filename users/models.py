from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель сущности Пользователь"""
    R_FLORIST = 'FL'
    R_COURIER = 'CR'
    R_NOT_DEFINED = 'ND'

    ROLE_CHOICES = (
        (R_FLORIST, 'Флорист'),
        (R_COURIER, 'Курьер'),
        (R_NOT_DEFINED, 'Не определена')
    )

    role = models.CharField(max_length=2,
                            choices=ROLE_CHOICES,
                            default=R_NOT_DEFINED,
                            verbose_name='Роль персонала'
                            )

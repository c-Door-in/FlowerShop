# Generated by Django 4.1.5 on 2023-01-22 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UtmCheckin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_date', models.DateTimeField(auto_now=True, verbose_name='Время захода')),
                ('utm_source', models.CharField(max_length=100, verbose_name='Источник UTM')),
                ('utm_medium', models.CharField(max_length=10, verbose_name='Тип траффика')),
                ('utm_campaign', models.CharField(max_length=100, verbose_name='Название компании')),
                ('utm_content', models.CharField(max_length=250, verbose_name='Идентификатор объявления')),
                ('utm_term', models.CharField(max_length=100, verbose_name='Ключевое слово')),
            ],
            options={
                'verbose_name': 'UTM метка',
                'verbose_name_plural': 'UTM метки',
            },
        ),
    ]

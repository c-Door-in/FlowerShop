# Generated by Django 4.1.5 on 2023-01-18 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_remove_decorationitem_bouquet_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='delivered_at',
            field=models.DateTimeField(blank=True, db_index=True, verbose_name='Фактическое время доставки'),
        ),
    ]

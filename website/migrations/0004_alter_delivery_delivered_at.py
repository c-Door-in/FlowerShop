# Generated by Django 4.1.5 on 2023-01-18 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_alter_delivery_delivered_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='delivered_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Фактическое время доставки'),
        ),
    ]

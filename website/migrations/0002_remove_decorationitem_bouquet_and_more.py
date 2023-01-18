# Generated by Django 4.1.5 on 2023-01-18 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='decorationitem',
            name='bouquet',
        ),
        migrations.RemoveField(
            model_name='decorationitem',
            name='decoration',
        ),
        migrations.RemoveField(
            model_name='floweritem',
            name='bouquet',
        ),
        migrations.RemoveField(
            model_name='floweritem',
            name='flower',
        ),
        migrations.RemoveField(
            model_name='bouquet',
            name='decorations',
        ),
        migrations.RemoveField(
            model_name='bouquet',
            name='flowers',
        ),
        migrations.AddField(
            model_name='bouquet',
            name='composition',
            field=models.TextField(default='Состав:', verbose_name='Состав'),
        ),
        migrations.AddField(
            model_name='bouquet',
            name='name',
            field=models.CharField(default='Букет', max_length=128, verbose_name='Наименование'),
        ),
        migrations.AddField(
            model_name='bouquet',
            name='size',
            field=models.TextField(default='Ширина: Высота:', verbose_name='Размер'),
        ),
        migrations.AddField(
            model_name='callback',
            name='status',
            field=models.CharField(choices=[('NW', 'Новый'), ('CD', 'Совершен звонок'), ('FN', 'Завершен')], db_index=True, default='NW', max_length=2, verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='status',
            field=models.CharField(choices=[('NW', 'Новая доставка'), ('PR', 'Доставляется'), ('FN', 'Завершена доставка')], db_index=True, default='NW', max_length=2, verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('AC', 'Принят'), ('AS', 'Сборка'), ('DL', 'Доставка'), ('FN', 'Завершен')], db_index=True, default='AC', max_length=2, verbose_name='Статус заказа'),
        ),
        migrations.AlterField(
            model_name='bouquet',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bouquets', to='website.event', verbose_name='Событие'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='delivered_at',
            field=models.DateTimeField(db_index=True, verbose_name='Фактическое время доставки'),
        ),
        migrations.DeleteModel(
            name='Decoration',
        ),
        migrations.DeleteModel(
            name='DecorationItem',
        ),
        migrations.DeleteModel(
            name='Flower',
        ),
        migrations.DeleteModel(
            name='FlowerItem',
        ),
    ]

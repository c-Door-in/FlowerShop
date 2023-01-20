from django.contrib import admin

from website.models import Event, Bouquet, Order, CallBack, Delivery, Payment


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'delivery_time', 'order_status']


@admin.register(CallBack)
class CallBackAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'phonenumber', 'status']


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['order', 'status']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'status']

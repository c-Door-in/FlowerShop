from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from django.shortcuts import render

from website.models import Order


@login_required
def statistic_main(request):

    orders = Order.objects.prefetch_related('bouquet').all()

    orders_count = orders.count()

    avg = orders.aggregate(Avg('bouquet__price'))

    total = orders.aggregate(Sum('bouquet__price'))

    accepted_orders = Order.objects.filter(order_status='AC').count()
    assembly_orders = Order.objects.filter(order_status='AS').count()
    delivery_orders = Order.objects.filter(order_status='DL').count()
    finished_orders = Order.objects.filter(order_status='FN').count()

    context = {
        'orders_count': orders_count,
        'avg': avg,
        'total': total,
        'accepted_orders': accepted_orders,
        'assembly_orders': assembly_orders,
        'delivery_orders': delivery_orders,
        'finished_orders': finished_orders
    }

    return render(request, 'statistic/main.html', context)

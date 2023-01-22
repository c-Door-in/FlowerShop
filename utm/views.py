import datetime

from django.urls import reverse

from utm.models import UtmCheckin


def check_utm(request):

    get_referer = request.GET.get('utm_source')

    if not get_referer:
        return reverse('mainpage')

    UtmCheckin.objects.create(
        check_in_date=datetime.datetime.now(),
        utm_source=request.GET.get('utm_source'),
        utm_medium=request.GET.get('utm_medium'),
        utm_campaign=request.GET.get('utm_campaign'),
        utm_content=request.GET.get('utm_content'),
        utm_term=request.GET.get('utm_term')
    )

    return reverse('mainpage')

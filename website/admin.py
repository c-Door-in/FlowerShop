from django.contrib import admin

from website.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
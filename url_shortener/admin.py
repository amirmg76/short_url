from django.contrib import admin
from .models import Link


@admin.register(Link)
class LinkPage(admin.ModelAdmin):
    readonly_fields = ['views_count_devices', 'views_count_browsers',
                       'unique_views_count_devices',
                       'unique_views_count_browsers',
                       'ip_views', ]

from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import User


class Link(models.Model):
    link = models.URLField()
    short_slug = models.SlugField()
    views_count_devices = ArrayField(JSONField(), default=list)
    views_count_browsers = ArrayField(JSONField(), default=list)
    unique_views_count_devices = ArrayField(JSONField(), default=list)
    unique_views_count_browsers = ArrayField(JSONField(), default=list)
    ip_views = ArrayField(JSONField(), default=list)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self):
        if not self.views_count_devices:
            self.views_count_devices = [{}]*31
            self.views_count_browsers = [{}]*31
            self.unique_views_count_devices = [{'ip-device': []}]*31
            self.unique_views_count_browsers = [{'ip-browser': []}]*31
            self.ip_views = [{'ip': []}]*31
        super(Link, self).save()

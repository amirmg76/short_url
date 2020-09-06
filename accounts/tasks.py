from __future__ import absolute_import, unicode_literals
import collections
import functools
import operator
from celery import shared_task
from url_shortener.models import Link


@shared_task
def get_daily_information(slug):
    data = Link.objects.get(short_slug=slug)
    device_dict = data.views_count_devices[0]
    browser_dict = data.views_count_browsers[0]
    return device_dict, browser_dict


@shared_task
def get_daily_unique_information(slug):
    data = Link.objects.get(short_slug=slug)
    unique_count_device = data.unique_views_count_devices[0]['ip-device']
    unique_count_browser = data.unique_views_count_browsers[0]['ip-browser']
    unique_device_list = list(set(el[1] for el in unique_count_device))
    unique_browser_list = list(set(el[1] for el in unique_count_browser))
    unique_device_dict = dict.fromkeys(unique_device_list, 0)
    unique_browser_dict = dict.fromkeys(unique_browser_list, 0)

    for _, device in unique_count_device:
        unique_device_dict[device] += 1

    for _, browser in unique_count_browser:
        unique_browser_dict[browser] += 1

    return unique_device_dict, unique_browser_dict


@shared_task
def get_yesterday_information(slug):
    data = Link.objects.get(short_slug=slug)
    device_dict = data.views_count_devices[1]
    browser_dict = data.views_count_browsers[1]

    return device_dict, browser_dict


@shared_task
def get_yesterday_unique_information(slug):
    data = Link.objects.get(short_slug=slug)
    unique_count_device = data.unique_views_count_devices[1]['ip-device']
    unique_count_browser = data.unique_views_count_browsers[1]['ip-browser']
    unique_device_list = list(set(el[1] for el in unique_count_device))
    unique_browser_list = list(set(el[1] for el in unique_count_browser))
    unique_device_dict = dict.fromkeys(unique_device_list, 0)
    unique_browser_dict = dict.fromkeys(unique_browser_list, 0)

    for _, device in unique_count_device:
        unique_device_dict[device] += 1

    for _, browser in unique_count_browser:
        unique_browser_dict[browser] += 1

    return unique_device_dict, unique_browser_dict


@shared_task
def get_weekly_information(slug):
    data = Link.objects.get(short_slug=slug)
    device_dict = data.views_count_devices[1:8]
    browser_dict = data.views_count_browsers[1:8]
    devices = dict(functools.reduce(operator.add,
                   map(collections.Counter, device_dict)))
    browsers = dict(functools.reduce(operator.add,
                    map(collections.Counter, browser_dict)))
    return devices, browsers


@shared_task
def get_weekly_unique_information(slug):
    data = Link.objects.get(short_slug=slug)
    device_dict = data.unique_views_count_devices[1:8]
    browser_dict = data.unique_views_count_browsers[1:8]
    template_device = []
    template_browser = []
    for i in range(7):
        template_device.append(device_dict[i]['ip-device'][:])

    for i in range(7):
        template_browser.append(browser_dict[i]['ip-browser'][:])

    template_device = list(filter(None, template_device))
    template_browser = list(filter(None, template_browser))

    if template_device:
        template_device = template_device[0]
        devices = [list(x) for x in set(tuple(x) for x in template_device)]
    else:
        devices = {}

    if template_browser:
        template_browser = template_browser[0]
        browsers = [list(x) for x in set(tuple(x) for x in template_browser)]
    else:
        browsers = {}

    return devices, browsers


@shared_task
def get_monthly_information(slug):
    data = Link.objects.get(short_slug=slug)
    device_dict = data.views_count_devices[1:]
    browser_dict = data.views_count_browsers[1:]
    devices = dict(functools.reduce(operator.add,
                   map(collections.Counter, device_dict)))
    browsers = dict(functools.reduce(operator.add,
                    map(collections.Counter, browser_dict)))
    return devices, browsers


@shared_task
def get_monthly_unique_information(slug):
    data = Link.objects.get(short_slug=slug)
    device_dict = data.unique_views_count_devices[1:]
    browser_dict = data.unique_views_count_browsers[1:]
    template_device = []
    template_browser = []
    for i in range(30):
        template_device.append(device_dict[i]['ip-device'][:])

    for i in range(30):
        template_browser.append(browser_dict[i]['ip-browser'][:])

    template_device = list(filter(None, template_device))
    template_browser = list(filter(None, template_browser))

    if template_device:
        template_device = template_device[0]
        devices = [list(x) for x in set(tuple(x) for x in template_device)]
    else:
        devices = {}

    if template_browser:
        template_browser = template_browser[0]
        browsers = [list(x) for x in set(tuple(x) for x in template_browser)]
    else:
        browsers = {}

    return devices, browsers

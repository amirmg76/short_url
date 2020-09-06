from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.task import periodic_task
from celery.schedules import crontab
from .models import Link


@shared_task
def update_link_information(request, requested_redirection):

    requested_device = requested_redirection.views_count_devices
    requested_browser = requested_redirection.views_count_browsers

    if request.user_agent.is_mobile:
        if 'mobile' in requested_device[0]:
            requested_device[0]['mobile'] += 1
        else:
            requested_device[0]['mobile'] = 1

    if request.user_agent.is_pc:
        if 'pc' in requested_device[0]:
            requested_device[0]['pc'] += 1
        else:
            requested_device[0]['pc'] = 1

    user_browser = request.user_agent.browser.family

    if user_browser in requested_browser[0]:
        requested_browser[0][user_browser] += 1
    else:
        requested_browser[0][user_browser] = 1

    requested_redirection.save()


@shared_task
def update_link_unique_information(request, requested_redirection):

    ip_views = requested_redirection.ip_views

    requested_ip = request.META['REMOTE_ADDR']
    if requested_ip not in ip_views[0]['ip']:
        unique_requested_device = requested_redirection.unique_views_count_devices
        unique_requested_browser = requested_redirection.unique_views_count_browsers

        ip_views[0]['ip'].append(str(requested_ip))
        if request.user_agent.is_mobile:
            unique_requested_device[0]['ip-device'].append([requested_ip, 'mobile'])
        elif request.user_agent.is_pc:
            unique_requested_device[0]['ip-device'].append([requested_ip, 'pc'])

        user_browser = request.user_agent.browser.family
        unique_requested_browser[0]['ip-browser'].append([requested_ip, user_browser])

    requested_redirection.save()


@periodic_task(run_every=crontab(minute=0, hour='0'))
def update_daily():
    all_request = Link.objects.all()
    requested_device = all_request.views_count_devices
    requested_browsers = all_request.views_count_browsers
    unique_requested_device = all_request.unique_views_count_devices
    unique_requested_browser = all_request.unique_views_count_browsers
    ip_views = all_request.ip_views

    slug_count = len(all_request)

    for i in range(slug_count):
        del requested_device[i][30]
        del requested_browsers[i][30]
        del unique_requested_device[i][30]
        del unique_requested_browser[i][30]
        del ip_views[i][30]
        requested_device.insert(0, {})
        requested_browsers.insert(0, {})
        unique_requested_device.insert(0, {})
        unique_requested_browser.insert(0, {})
        ip_views.insert(0, {'ip': []})

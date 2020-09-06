import random
import string
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import Link
from .tasks import update_link_information, update_link_unique_information


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def firstPage(request):
    if request.method == 'GET':
        return render(request, 'home.html')

    if request.method == 'POST':
        link = request.POST['link']
        chosen_slug = request.POST['chosen_slug']
        user = request.user

        def get_random_string(length):
            letters = string.ascii_letters
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string

        def check_slug(some_slug):
            try:
                Link.objects.get(short_slug=some_slug)
            except ObjectDoesNotExist:
                return True
            return False

        if chosen_slug:
            if check_slug(chosen_slug):
                new_link = Link(link=link, short_slug=chosen_slug, user=user)
                new_link.save()
                domain = request.get_host()
                short_link = domain + "/link/" + chosen_slug
                context = {'short_link': short_link, 'chosen_slug': chosen_slug}
                messages.success(request, "it's done you can now go to the link ib below")
                return render(request, 'home.html', context)
            else:
                while True:
                    new_slug = chosen_slug + get_random_string(3)
                    if check_slug(new_slug):
                        chosen_slug = new_slug
                        new_link = Link(link=link, short_slug=chosen_slug, user=user)
                        new_link.save()
                        domain = request.get_host()
                        short_link = domain + "/link/" + chosen_slug
                        context = {'short_link': short_link, 'chosen_slug': chosen_slug}
                        messages.success(request, "it's done you can now go to the link ib below")

                        return render(request, 'home.html', context)

        while True:
            new_slug = get_random_string(15)
            if check_slug(new_slug):
                chosen_slug = new_slug
                new_link = Link(link=link, short_slug=chosen_slug, user=user)
                new_link.save()
                domain = request.get_host()
                short_link = domain + "/link/" + chosen_slug
                context = {'short_link': short_link, 'chosen_slug': chosen_slug}
                messages.success(request, "it's done you can now go to the link ib below")

                return render(request, 'home.html', context)


@cache_page(CACHE_TTL)
def site_redirection(request, slug):
    requested_redirection = Link.objects.get(short_slug=slug)
    update_link_information(request, requested_redirection)
    update_link_unique_information(request, requested_redirection)
    requested_link = requested_redirection.link
    return redirect(requested_link)

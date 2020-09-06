from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from url_shortener.models import Link
from .tasks import get_daily_information, get_daily_unique_information,\
                   get_yesterday_information, get_yesterday_unique_information,\
                   get_weekly_information, get_weekly_unique_information,\
                   get_monthly_information, get_monthly_unique_information


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')

    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']

        login_with_username = auth.authenticate(username=username_or_email,
                                                password=password)
        if login_with_username:
            auth.login(request, login_with_username)
            return redirect('/')

        try:
            username = User.objects.get(email=username_or_email).username
        except:
            messages.error(request, "the informations were wrong try again")
            return redirect('login')
        login_with_email = auth.authenticate(username=username,
                                             password=password)
        if login_with_email:
            auth.login(request, login_with_email)
            return redirect('/')

        else:
            return redirect('login')


def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'register.html')

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']

        if password != repeat_password:
            messages.error(request, "passwords don't match")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "this user already exists")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "this email already exists")
            return render(request, 'register.html')

        user = User.objects.create_user(username=username,
                                        email=email, password=password)
        user.save()
        auth.login(request, user)

        return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')


def dashboard(request):
    user = request.user
    users_links = Link.objects.filter(user=user)
    context = {'users_links': users_links}
    return render(request, 'dashboard.html', context)


def url_view(request, slug):
    device_dict_today, browser_dict_today = get_daily_information(slug)
    unique_device_dict_today, unique_browser_dict_today = get_daily_unique_information(slug)
    device_dict_yesterday, browser_dict_yesterday = get_yesterday_information(slug)
    unique_device_dict_yesterday, unique_browser_dict_yesterday = get_yesterday_unique_information(slug)
    device_dict_weekly, browser_dict_weekly = get_weekly_information(slug)
    unique_device_dict_weekly, unique_browser_dict_weekly = get_weekly_unique_information(slug)
    device_dict_monthly, browser_dict_monthly = get_monthly_information(slug)
    unique_device_dict_monthly, unique_browser_dict_monthly = get_monthly_unique_information(slug)

    context = {'device_dict_today': device_dict_today, 'browser_dict_today': browser_dict_today,
               'unique_device_dict_today': unique_device_dict_today, 'unique_browser_dict_today': unique_browser_dict_today,
               'device_dict_yesterday': device_dict_yesterday, 'browser_dict_yesterday': browser_dict_yesterday,
               'unique_device_dict_yesterday': unique_device_dict_yesterday, 'unique_browser_dict_yesterday': unique_browser_dict_yesterday,
               'device_dict_weekly': device_dict_weekly, 'browser_dict_weekly': browser_dict_weekly,
               'unique_device_dict_weekly': unique_device_dict_weekly, 'unique_browser_dict_weekly': unique_browser_dict_weekly,
               'device_dict_monthly': device_dict_monthly, 'browser_dict_monthly': browser_dict_monthly,
               'unique_device_dict_monthly': unique_device_dict_monthly, 'unique_browser_dict_monthly': unique_browser_dict_monthly}

    return render(request, 'url_view.html', context)

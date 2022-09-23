import requests
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    template = "index.html"
    context = {}

    return render(request, template, context)

@login_required(login_url='counsellor:login_client')
def home(request):
    template = "homepage.html"
    context = {}

    return render(request, template, context)

def login_client(request):
    template = "login_client.html"
    context = {}

    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')

        print(email,password)

        user = auth.authenticate(email=email, password=password)
        print(user)
        auth.login(request, user, backend='counsellor.backend.MultipleAuthBackend')

        # Check if user was attempting to visit another page
        url = request.META.get('HTTP_REFERER')
        try:
            query = requests.utils.urlparse(url).query
            params = dict(x.split('=') for x in query.split('&'))

            if 'next' in params:
                nextPage = params['next']
                return redirect(nextPage)
        except Exception as e:
            print(e)
            return redirect('counsellor:home')


    return render(request, template, context)

def login_counsellor(request):
    template = "login_counsellor.html"
    context = {}

    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')

        print(email,password)

        user = auth.authenticate(request, email=email, password=password, data_type="counsellor")
        auth.login(request, user, backend='counsellor.backend.MultipleAuthBackend')

        # Check if user was attempting to visit another page
        url = request.META.get('HTTP_REFERER')
        try:
            query = requests.utils.urlparse(url).query
            params = dict(x.split('=') for x in query.split('&'))

            if 'next' in params:
                nextPage = params['next']
                return redirect(nextPage)
        except Exception as e:
            print(e)
            return redirect('counsellor:home')


    return render(request, template, context)



@login_required(login_url='user:login_client')
def logout(request):
    auth.logout(request)
    return redirect('counsellor:login_client')



def register(request):
    template = "signup.html"
    context = {}

    return render(request, template, context)

def forgot_password(request):
    template = "forget.html"
    context = {}

    return render(request, template, context)

def about(request):
    template = "about.html"
    context = {}

    return render(request, template, context)

def confidential(request):
    template = "confidential.html"
    context = {}

    return render(request, template, context)

def conditions(request):
    template = "conditions.html"
    context = {}

    return render(request, template, context)


def support(request):
    template = "support.html"
    context = {}

    return render(request, template, context)

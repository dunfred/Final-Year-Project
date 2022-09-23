from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    template = "index.html"
    context = {}

    return render(request, template, context)


@login_required(login_url='counsellor:login')
def home(request):
    template = "homepage.html"
    context = {}

    return render(request, template, context)

def login(request):
    template = "login.html"
    context = {}

    return render(request, template, context)

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

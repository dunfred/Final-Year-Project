import requests
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from counsellor.models import CounsellingType, Counsellor, User

# Create your views here.

def index(request):
    template = "index.html"
    context = {}

    return render(request, template, context)

@login_required(login_url='counsellor:login_client')
def home(request):
    template = "homepage.html"

    q        = request.GET.get('q', None)
    category = request.GET.get('category', None)

    counselling_types = CounsellingType.objects.all()
    if category:
        counsellors = Counsellor.objects.filter(fields__type__iexact=category)

    else:
        counsellors = Counsellor.objects.all()

    if q:
        counsellors = counsellors.filter(
            Q(email__icontains=q)|
            Q(first_name__icontains=q)|
            Q(last_name__icontains=q)|
            Q(other_names__icontains=q)|
            Q(title__iexact=q)
        )

    context = {
        'counselling_types':counselling_types,
        "counsellors": counsellors
    }

    return render(request, template, context)

@login_required(login_url='counsellor:login_counsellor')
def counsellor_profile(request, counsellor_id):
    template = "counsellor-profile.html"
    context = {}

    counsellor = Counsellor.objects.filter(id=counsellor_id).first()
    if counsellor:
        context["counsellor"] = counsellor
        context["available_days"] = counsellor.availability.all().order_by('id')
        
        fields = counsellor.fields.all()
        fields_cnt = counsellor.fields.count()

        if fields_cnt == 1:
            fields_str = counsellor.fields.first().type
        elif fields_cnt == 2:
            fields_str = " and ".join(fields.values_list("type", flat=True))
        elif fields_cnt > 2:
            fields_str = " , ".join(fields[:fields_cnt-1].values_list("type", flat=True))
            fields_str = f"{fields_str} and {fields.last().type}"
        else:
            fields_str = ""
        context["categories_str"] = fields_str
    
    return render(request, template, context)



def login_client(request):
    template = "login.html"
    context = {}

    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email__iexact=email)
            password_correct = User.check_password(user, password)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            print(e)
            user = None
            password_correct = False

        if user:
            if password_correct:
                if user.is_active:
                    # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    login(request, user, backend='counsellor.backend.MultipleAuthBackend')
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
                else:
                    context['error'] = 'This account is not active.'
            else:
                context['error'] = 'Wrong Email / Password combination.'
        else:
            context['error'] = 'No matching account found.'

    return render(request, template, context)

def login_counsellor(request):
    template = "admin-login.html"
    context = {}

    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        
        authenticate_kwargs = {
            'email': email,
            'password': password,
        }
        authenticate_kwargs['data_type'] = 'counsellor'  # Add data_type
        try:
            authenticate_kwargs['request'] = request
        except KeyError:
            pass

        user = authenticate(**authenticate_kwargs)

        if user:
            login(request, user, backend='counsellor.backend.MultipleAuthBackend')

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
        else:
            print('No such account exists')
            return redirect('.')

    return render(request, template, context)



@login_required(login_url='user:login_client')
def logout_view(request):
    logout(request)
    return redirect('counsellor:login_client')


def register_client(request):
    template = "signup.html"
    context = {}

    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        first_name  = request.POST.get('first_name')
        last_name   = request.POST.get('last_name')
        username    = request.POST.get('username')
        phone   = request.POST.get('phone')
        pssword = request.POST.get('pssword')
        
        user = User(
            email   = email,
            password    = password,
            first_name  = first_name,
            last_name   = last_name,
            username    = username,
            phone   = phone,
        )
        user.set_password(pssword)
        user.is_active = True
        user.save()

        print(user)

        return redirect('counsellor:login_client')

    return render(request, template, context)


def register_counsellor(request):
    template = "admin-signup.html"
    context = {}

    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        first_name  = request.POST.get('first_name')
        last_name   = request.POST.get('last_name')
        username    = request.POST.get('username')
        phone   = request.POST.get('phone')
        pssword = request.POST.get('pssword')
        
        user = Counsellor(
            email   = email,
            password    = password,
            first_name  = first_name,
            last_name   = last_name,
            username    = username,
            phone   = phone,
        )
        user.set_password(pssword)
        user.is_active = True
        user.save()

        print(user)

        return redirect('counsellor:login_counsellor')

    return render(request, template, context)


def forgot_password(request):
    template = "forgot-password.html"
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

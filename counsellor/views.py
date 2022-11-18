import requests
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from counsellor.decorators import consent_approval_taken
from counsellor.models import Consent, CounsellingType, Counsellor, User, Booking

# Create your views here.

def index(request):
    template = "index.html"
    context = {}

    return render(request, template, context)

@login_required(login_url='counsellor:login_client')
@consent_approval_taken
def home(request):
    template = "homepage.html"

    # if request.user.is_authenticated:
    #     print(request.user)
    #     print(request.user.user_type)
    #     print(isinstance(request.user, Counsellor))


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
def home_admin(request):
    template = "admin-homepage.html"
    bookings = Booking.objects.filter(counsellor=request.user)

    context = {
        'bookings': bookings
    }

    return render(request, template, context)


@login_required(login_url='counsellor:login_counsellor')
def client_approval_admin(request, client_id):
    client = User.objects.filter(id=client_id).first()
    context = {
        'client': client
    }

    booking_id = request.GET.get("booking_id", None)
    if booking_id:
        booking = Booking.objects.filter(id=booking_id).first()
        
        if booking:
            context['booking'] = booking

    template = "admin-client-approval.html"

    return render(request, template, context)


@login_required(login_url='counsellor:login_client')
@consent_approval_taken
def client_bookings(request):
    template = "client-bookings.html"
    context = {}
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
                return redirect('counsellor:home_counsellor')
        else:
            context['error'] = 'Invalid credentials provided'

    return render(request, template, context)



@login_required(login_url='user:login_client')
def logout_view(request):
    logout(request)
    return redirect('counsellor:login_client')


def register_client(request):
    template = "signup.html"
    context = {}

    if request.method == 'POST':
        email            = request.POST.get('email')
        password         = request.POST.get('password')
        first_name       = request.POST.get('first_name')
        last_name        = request.POST.get('last_name')
        phone            = request.POST.get('phone')
        # user_type        = request.POST.get('user_type')

        
        password         = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            if not User.objects.filter(email=email).exists():
                if not Counsellor.objects.filter(email=email).exists():
                    if not User.objects.filter(phone=phone).exists():
                        if not Counsellor.objects.filter(phone=phone).exists():
                            user = User(
                                email   = email,
                                password    = password,
                                first_name  = first_name,
                                last_name   = last_name,
                                phone   = phone,
                                # user_type=user_type
                            )
                            user.set_password(password)
                            user.is_active = True
                            user.save()

                            print(user)
                            
                            login(request, user, backend='counsellor.backend.MultipleAuthBackend')

                            return redirect('counsellor:confidential')
                        else:
                            context['error'] = "This phone has already been registered"
                    else:
                        context['error'] = "This phone has already been registered"
                else:
                    context['error'] = "This email has already been registered"
            else:
                context['error'] = "This email has already been registered"
        else:
            context['error'] = "Passwords do not match"

    return render(request, template, context)


def register_counsellor(request):
    template = "admin-signup.html"
    context = {}

    if request.method == 'POST':
        email            = request.POST.get('email')
        password         = request.POST.get('password')
        first_name       = request.POST.get('first_name')
        last_name        = request.POST.get('last_name')
        phone            = request.POST.get('phone')
        password         = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            if not User.objects.filter(email__iexact=email).exists():
                if not Counsellor.objects.filter(email__iexact=email).exists():

                    if not User.objects.filter(phone=phone).exists():
                        if not Counsellor.objects.filter(phone=phone).exists():
                            user = Counsellor(
                                email   = email,
                                password    = password,
                                first_name  = first_name,
                                last_name   = last_name,
                                phone   = phone,
                            )
                            user.set_password(password)
                            user.is_active = True
                            user.save()

                            print(user)

                            return redirect('counsellor:login_counsellor')

                        else:
                            context['error'] = "This phone has already been registered"
                    else:
                        context['error'] = "This phone has already been registered"
                else:
                    context['error'] = "This email has already been registered"
            else:
                context['error'] = "This email has already been registered"
        else:
            context['error'] = "Passwords do not match"


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

    if request.method == 'POST':
        user                = request.user
        is_student          = request.POST.get("is_student")
        registration_number = request.POST.get("registration_number")
        programme           = request.POST.get("programme")
        department          = request.POST.get("department")
        level               = request.POST.get("level")
        residence           = request.POST.get("residence")
        home_phone          = request.POST.get("home_phone")
        worker              = request.POST.get("worker")
        work_type           = request.POST.get("work_type")
        organization        = request.POST.get("organization")
        emergency_person    = request.POST.get("emergency_person")
        emergency_contact   = request.POST.get("emergency_contact")
        referrer            = request.POST.get("referrer")
        prev_counselling    = request.POST.get("prev_counselling")
        on_medication       = request.POST.get("on_medication")
        guardian            = request.POST.get("guardian")
        guardian_phone      = request.POST.get("guardian_phone")

        try:
            if is_student:
                consent = Consent.objects.create(
                    user=user,
                    registration_number = registration_number,
                    programme           = programme,
                    department          = department,
                    level               = level,
                    residence           = residence,
                    home_phone          = home_phone,
                    emergency_person    = emergency_person,
                    emergency_contact   = emergency_contact,
                    referrer            = referrer,
                    prev_counselling    = prev_counselling,
                    on_medication       = on_medication,
                    guardian            = guardian,
                    guardian_phone      = guardian_phone,
                )
            else:
                consent = Consent.objects.create(
                    user              = user,
                    worker            = worker,
                    work_type         = work_type,
                    organization      = organization,
                    emergency_person  = emergency_person,
                    emergency_contact = emergency_contact,
                    referrer          = referrer,
                    prev_counselling  = prev_counselling,
                    on_medication     = on_medication,
                    guardian          = guardian,
                    guardian_phone    = guardian_phone,
                )
            

            print(consent)

            return redirect('counsellor:home')
        except Exception as e:
            print(e)
            context['error'] = f"Server error. {e}"

    return render(request, template, context)

def conditions(request):
    template = "conditions.html"
    context = {}

    return render(request, template, context)


def support(request):
    template = "support.html"
    context = {}

    return render(request, template, context)

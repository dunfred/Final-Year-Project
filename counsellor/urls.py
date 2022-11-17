from django.urls import path
from counsellor import views

app_name = "counsellor"

urlpatterns = [
    path('',                 views.index, name="index"),
    path('home/',            views.home, name="home"),
    # For clients
    path('login/',           views.login_client, name="login_client"),
    path('register/',        views.register_client, name="register_client"),
    path('bookings/',        views.client_bookings, name="client_bookings"),
    
    # For admins
    path('counsellor-admin/',  views.home_admin, name="home_counsellor"),
    path('counsellor-admin/login/',     views.login_counsellor, name="login_counsellor"),
    path('counsellor-admin/register/',  views.register_counsellor, name="register_counsellor"),
    path('counsellor-admin/profile/<int:counsellor_id>/',  views.counsellor_profile, name="counsellor_profile"),
    path('counsellor-admin/client-approval/<int:client_id>/',  views.client_approval_admin, name="client_approval"),

    
    path('logout/',          views.logout_view, name="logout"),
    path('about/',           views.about, name="about"),
    path('support/',         views.support, name="support"),
    path('confidential/',    views.confidential, name="confidential"),
    path('conditions/',      views.conditions, name="conditions"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
]

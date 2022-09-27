from django.urls import path
from counsellor import views

app_name = "counsellor"

urlpatterns = [
    path('',                 views.index, name="index"),
    path('home/',            views.home, name="home"),
    # For clients
    path('login/',           views.login_client, name="login_client"),
    path('register/',        views.register_client, name="register_client"),
    
    # For admins
    path('counsellor-admin/login/',     views.login_counsellor, name="login_counsellor"),
    path('counsellor-admin/register/',  views.register_counsellor, name="register_counsellor"),
    path('counsellor-admin/profile/<int:counsellor_id>/',  views.counsellor_profile, name="counsellor_profile"),
    
    path('logout/',          views.logout_view, name="logout"),
    path('about/',           views.about, name="about"),
    path('support/',         views.support, name="support"),
    path('confidential/',    views.confidential, name="confidential"),
    path('conditions/',      views.conditions, name="conditions"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
]

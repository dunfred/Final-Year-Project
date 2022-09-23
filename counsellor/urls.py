from django.urls import path
from counsellor import views

app_name = "counsellor"

urlpatterns = [
    path('',                 views.index, name="index"),
    path('home/',            views.home, name="home"),
    path('login/',           views.login, name="login"),
    path('register/',        views.register, name="register"),
    path('about/',           views.about, name="about"),
    path('support/',         views.support, name="support"),
    path('confidential/',    views.confidential, name="confidential"),
    path('conditions/',      views.conditions, name="conditions"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
]

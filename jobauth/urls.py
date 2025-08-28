from django.urls import path
from . import views

app_name = "jobauth"

urlpatterns = [
    path('login', views.authlogin, name='login'),
    path('register', views.authregister, name='register'),
    path('captcha', views.send_email_captcha, name='captcha'),
    path('logout', views.authlogout, name='logout'),
]
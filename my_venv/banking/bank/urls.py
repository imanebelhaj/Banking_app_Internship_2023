from django.urls import path
from . import views

app_name= 'bank'

urlpatterns = [
    path('login_user/', views.login_user , name='login_user'),
    path('history/', views.history , name="history"),
    path('homepage/', views.homepage , name="homepage"),
    path('success/', views.success, name = 'success'),
    path('mycards/', views.mycards, name = 'mycards'),
    path('profile/', views.profile, name = 'profile'),
    path('transact/', views.transact, name = 'transact'),
    path('message/', views.message, name = 'message'),
    path('intro/', views.intro, name = 'intro'),
    path('sent/', views.sent, name = 'sent'),

]

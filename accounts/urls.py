from django.urls import path
from . import views

urlpatterns = [
    path('registo/', views.registo_view, name='registo'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('login/magic/', views.magic_link_request, name='magic_link_request'),
    path('login/magic/<str:token>/', views.magic_login, name='magic_login'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
]

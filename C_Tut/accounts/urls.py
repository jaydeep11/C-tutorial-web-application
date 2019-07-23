from django.urls import path
from . import views


app_name='accounts'
urlpatterns=[
    path('', views.index , name='index'),
    path( 'login/' , views.loginUser.as_view() , name='login'),
    path('signup',views.signupUser.as_view(),name='signup'),
    path('logout',views.logout_user.as_view(),name='logout'),
]
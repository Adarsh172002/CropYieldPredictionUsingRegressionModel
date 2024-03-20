
from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('', CustomLoginView.as_view(), name='login'),
    path('home', Homepageview.as_view(), name='home'),
]
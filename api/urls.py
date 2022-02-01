from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

app_name='api'
urlpatterns = [
    path('register/',views.register.as_view()),
    path('login/',obtain_auth_token,name='auth_user_login'),
    path('logout/',views.logout.as_view(), name='auth_user_logout'),
    path('profile/',views.Profile.as_view(), name="profile"),
    path('quarantine/',views.Quarantine.as_view(), name="quarantine"),
    path('check/',views.Check.as_view(), name="check"),
    # path('setPassword/',views.setPassword.as_view(), name="setPassword")
]
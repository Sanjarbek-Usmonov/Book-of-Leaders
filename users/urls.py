from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from .views import (UserChangePass,
                            UserDetail, UserList, UsersRegisterView,)
# from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('register', UserRegisterView.as_view()),
    # path('login', CustomTokenObtainPairView.as_view()),
    path('login', obtain_auth_token),
    # path('refreshtoken', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', UsersRegisterView.as_view(), name='register'),
]
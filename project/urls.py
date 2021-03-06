"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from message.views import MessageListCreateView
from users.views import UserCreateView, BlockUserView, UnBlockUserView, UserLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Users
    path("user/login/", UserLoginView.as_view(), name="user-login"),
    path("user/register/", UserCreateView.as_view(), name="user-create"),
    path("user/block/<str:username>/", BlockUserView.as_view(), name="block-user"),
    path("user/unblock/<str:username>/", UnBlockUserView.as_view(), name="block-user"),
    # Messages
    path("message/<str:username>/", MessageListCreateView.as_view(), name="user-create"),
]

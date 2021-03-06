"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from library_app.user_auth import CreateNewUser
from library_app.user_auth import AuthView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^library/', include('library_app.urls', namespace='library-app')),
    url(r'^register/$',CreateNewUser.as_view({'post':'post'}), name='register-user'),
    url(r'^login/$',AuthView.as_view({'post':'login' ,'get':'loginview'}), name='login'),
    url(r'^logout/$',AuthView.as_view({'get':'logout'}), name='logout')
]

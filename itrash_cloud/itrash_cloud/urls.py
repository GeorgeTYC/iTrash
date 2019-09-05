"""itrash_cloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
import itrash_manage.views
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from . import settings

urlpatterns = [
    url(r'^upload$',itrash_manage.views.upload),
    url(r'^$',itrash_manage.views.index),#首页入口
    url(r'^favicon\.ico$',RedirectView.as_view(url=r'static/itrash_manage/img/favicon.ico')),
    url(r'^login$', itrash_manage.views.dologin, name="dologin"),
    url(r'^logout$',itrash_manage.views.dologout,name='dologout'),
    url(r'^portal$',itrash_manage.views.portal,name="portal"),
    url(r'^overview$',itrash_manage.views.overview),
    path("stat/<int:type>",itrash_manage.views.stat),
    path("query/<str:q>",itrash_manage.views.queryTrash),
    url(r'^control$',itrash_manage.views.control),
    url(r'^sysinfo$',itrash_manage.views.sysinfo),
    url(r'^doaudit$', itrash_manage.views.doaudit,name="doaudit"),
    url(r'^changeLbl$',itrash_manage.views.changeLbl),
    url(r'^deletePic$',itrash_manage.views.deletePic),
    url(r'^picrecord$',itrash_manage.views.picrecord),
    url(r'^picrelbl$',itrash_manage.views.picrelbl),
    url(r'^userpage$',itrash_manage.views.userpage),
    url(r'^usergppage$',itrash_manage.views.usergppage),
    url(r'^changePicInfo$',itrash_manage.views.changePicInfo),
    url(r'^admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

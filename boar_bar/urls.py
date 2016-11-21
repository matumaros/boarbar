"""boar_bar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView

from share.views import login, logout, NotExistingView


urlpatterns = [
    url(
        r'^$',
        RedirectView.as_view(url='home', permanent=True),
    ),
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^user/?', include('user.urls', namespace='user')),
    url(r'^admin/?', admin.site.urls),
    url(r'^login/?$', login),
    url(r'^logout/?$', logout),
    url(
        r'^dict/',
        include('dictionary.urls', namespace='dictionary')
    ),
    url(
        r'^word/?',
        include('word.urls')
    ),
    # url(
    #     r'^grammar/?',
    #     include('grammar.urls')
    # ),
    url(
        r'^collection/?',
        include('collection.urls')
    ),
    url(
        r'^discussion/?',
        include('discussion.urls')
    ),
    url(
        r'^favicon\.ico$',
        RedirectView.as_view(url='/static/favicon.png', permanent=True)
    ),
    url(
       r'^.*$',
       NotExistingView.as_view(),
       name='not_existing',
    ),
]

if settings.DEBUG:
 urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from django.conf.urls import url, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'languages', views.LanguageViewSet)
router.register(r'wordversions', views.WordVersionViewSet)
router.register(r'words', views.WordViewSet)

app_name = "api"

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^user/token', views.user_by_token),
    url(r'^similar_words/$', views.similar_words, name="similar_words"),

]

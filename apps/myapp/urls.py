from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'homepage$', views.homepage),
    url(r'register$', views.registration_logic),
    url(r'login$', views.login_logic),
    url(r'logout$', views.logout),
    url(r'newtravel$', views.new_travel),
    url(r'addtravel$', views.addtravel),
    url(r'info/(?P<id>\d+)$', views.travelinfo)
]

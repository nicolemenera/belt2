from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^submit$', views.submit),
    url(r'^add/(?P<quoteid>\d+)$', views.add),
    url(r'^remove/(?P<quoteid>\d+)$', views.remove),
    url(r'^info/(?P<userid>\d+)$', views.info),
    url(r'^user/(?P<userid>\d+)$', views.user),
    url(r'^logout$', views.logout)
]
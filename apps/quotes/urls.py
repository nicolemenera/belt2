from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^submit$', views.submit),
    url(r'^add$', views.add),
    url(r'^remove$', views.remove),
    url(r'^user$', views.user),
    url(r'^logout$', views.logout)
]
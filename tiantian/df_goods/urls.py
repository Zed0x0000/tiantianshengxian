from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^(\d+)/$', views.detail),
    url(r'^list(\d+)_(\d+)_(\d+)/$', views.list_info),
    url(r'^search/$', views.MySearchView()),
]

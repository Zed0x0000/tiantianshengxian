from django.conf.urls import url
import views

urlpatterns = [
    url(r'^/$', views.cart),
    url(r'^(\d+)_(\d+)/$', views.add_to_cart),
    url(r'^/edit(\d+)_(\d+)/$', views.edit_cart),
    url(r'^/delete(\d+)/$',views.delete_cart),
]
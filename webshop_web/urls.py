from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^home/?$', views.home, name='home'),
    url(r'^category/(?P<id_category>[0-9]+)/?$', views.category, name='about_category'),
    url(r'^product/(?P<id_product>[0-9]+)/?$', views.product, name='about_product'),
    url(r'^add/(?P<id_product>[0-9]+)/?$', views.add_to_cart, name='add_product'),
    url(r'^delete/(?P<id_product>[0-9]+)/?$', views.delete_from_cart, name='delete_product'),
    url(r'^cart/?$', views.view_cart, name='view_cart'),
    url(r'^order/(?P<id_cart>[0-9]+)/?$', views.order, name='package_order'),
]


from django.conf.urls import url

from . import views


app_name = 'choco'
urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^about/$', views.about_page, name='about'),
    url(r'^contacts/$', views.contacts_page, name='contacts'),
    url(r'^catalog/$', views.catalog_page, name='catalog'),
    url(r'^catalog/(?P<pk>[0-9]+)/$', views.details_page, name='details'),
    url(r'^cart/$', views.cart_page, name='cart'),
    url(r'^add/(?P<pk>[0-9]+)/$', views.cart_add, name='cart_add'),
    url(r'^remove/(?P<pk>[0-9]+)/$', views.cart_remove, name='cart_remove'),
    url(r'^order/$', views.order_page, name='order'),
    url(r'^order/send$', views.order_send, name='order_send'),
]

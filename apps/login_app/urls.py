from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^create_book$', views.create_book),
    url(r'^show/(?P<req_id>[0-9]+)$', views.show),
    url(r'^remove_from_favs/(?P<req_id>[0-9]+)$', views.remove_from_favs),
    url(r'^add_to_favs/(?P<req_id>[0-9]+)$', views.add_to_favs),
    url(r'^edit/(?P<req_id>[0-9]+)$', views.edit),
    url(r'^update$', views.update),
    url(r'^delete/(?P<req_id>[0-9]+)$', views.destroy),
]
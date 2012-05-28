from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'registration.views.home', name='home'),
    url(r'^charts/conversion/(\d)$', 'registration.views.conversion_chart'),
)

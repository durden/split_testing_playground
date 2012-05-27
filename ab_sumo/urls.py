from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ab_sumo.views.home', name='home'),
    url(r'^about/$', 'ab_sumo.views.about', name='about'),

    url(r'^register/', include('registration.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

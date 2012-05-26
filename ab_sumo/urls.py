from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'ab_sumo.views.home', name='home'),
    # url(r'^ab_sumo/', include('ab_sumo.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

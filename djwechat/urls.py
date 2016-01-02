from django.conf.urls import patterns, include, url
from django.contrib import admin
from wechat_shop.views import *
urlpatterns = patterns('',
    # Examples:
    url(r'^$', index, name='home'),
    url(r'^set_menu/$', set_menu),
    url(r'^refresh_all_user/$', refresh_all_user),

    url(r'^admin/', include(admin.site.urls)),
)

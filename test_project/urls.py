from django.conf.urls.defaults import *
from test_project import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', views.home),
	(r'^thread/add/$',views.add_thread),
    (r'^register/$', views.register_user),
    (r'^login/$', views.login_user),
    (r'^logout/$', views.logout_user),
    (r'^thread/(?P<t_id>\d+)/$', views.thread_page),
    (r'^comment/add/(?P<thread_id>\d+)/$',views.add_comment),
    (r'^vote/(?P<vote_type>\w+)/(?P<comment_id>\d+)/$',views.vote),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', views.login_user),
    (r'^comment/delete/(?P<comment_id>\d+)/$',views.delete_comment),
    (r'^thread/delete/(?P<thread_id>\d+)/$',views.delete_thread),
    (r'^thread/edit/(?P<thread_id>\d+)/$',views.edit_thread),
    (r'^comment/edit/(?P<comment_id>\d+)/$',views.edit_comment),
    (r'^user/password/reset/$','django.contrib.auth.views.password_reset'),    
    (r'^user/password/reset/done/$','django.contrib.auth.views.password_reset_done'),
    (r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$','django.contrib.auth.views.password_reset_confirm',
    {'post_reset_redirect' : '/user/password/done/'}),
    (r'^user/password/done/$','django.contrib.auth.views.password_reset_complete'),
    (r'^password_change/$', 'django.contrib.auth.views.password_change'),
    (r'^password_change/done/$', 'django.contrib.auth.views.password_change_done'),
    
    )
    
if settings.DEBUG:
    urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': settings.MEDIA_ROOT,
    }),
)

)

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
    

)

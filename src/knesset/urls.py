from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template, redirect_to
from django.views.decorators.cache import cache_page

from django.contrib.comments.models import Comment
from django.contrib import admin

from knesset.mks.urls import mksurlpatterns
from knesset.laws.urls import lawsurlpatterns
from knesset.committees.urls import committeesurlpatterns
from knesset.hashnav.views import SimpleView
from hitcount.views import update_hit_count_ajax
from backlinks.trackback.server import TrackBackServer
from backlinks.pingback.server import default_server
from knesset.mks.views import get_mk_entry, mk_is_backlinkable

admin.autodiscover()

from knesset import feeds 
from knesset.sitemap import sitemaps

js_info_dict = {
    'packages': ('knesset',),
    }

about_view = SimpleView(template='about.html')
#comment_view = object_list(Comment.objects.all(), template_name='comments/comments.html')

#main_view = SimpleView(template='main.html')
from knesset.auxiliary.views import main, post_annotation

urlpatterns = patterns('',
    
    url(r'^$', main, name='main'),
    url(r'^about/$', about_view, name='about'),
    (r'^api/', include('knesset.api.urls')),
    (r'^agenda/', include('knesset.agendas.urls')),
    (r'^users/', include('knesset.user.urls')),    
    (r'^badges/', include('knesset.badges.urls')),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
     (r'^comments/$', 'django.views.generic.list_detail.object_list', {'queryset': Comment.objects.all(),'paginate_by':20}), 
     url(r'^comments/delete/(?P<comment_id>\d+)/$', 'knesset.utils.delete', name='comments-delete-comment'),
     url(r'^comments/post/','knesset.utils.comment_post_wrapper',name='comments-post-comment'),
     (r'^comments/', include('django.contrib.comments.urls')),
     (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
     #(r'^search/', include('haystack.urls')),
     url(r'^search/', 'knesset.auxiliary.views.search', name='site-search'),
     (r'^feeds/comments/$', feeds.Comments()),
     (r'^feeds/votes/$', feeds.Votes()),
     (r'^feeds/bills/$', feeds.Bills()),
     (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}), 
     (r'^planet/', include('planet.urls')),
     url(r'^ajax/hit/$', update_hit_count_ajax, name='hitcount_update_ajax'),
     (r'^annotate/write/$', post_annotation, {}, 'annotatetext-post_annotation'),
     (r'^annotate/', include('annotatetext.urls')),
     (r'^avatar/', include('avatar.urls')),
     (r'^pingback/', default_server),
     url(r'^trackback/member/(?P<object_id>\d+)/$', TrackBackServer(get_mk_entry, mk_is_backlinkable),name='member-trackback'),
)
urlpatterns += mksurlpatterns + lawsurlpatterns + committeesurlpatterns
if settings.LOCAL_DEV:
    urlpatterns += patterns('django.views',
        (r'^static/(?P<path>.*)' , 'static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

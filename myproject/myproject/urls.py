from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'museos.views.barra'),
    url(r'^about$', 'museos.views.about'),
    url(r'^museos$', 'museos.views.museo_todos'),
    url(r'^museos/(\d+)$', 'museos.views.museo_id'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^([^/]*)/xml$', 'museos.views.usuario_xml'),
    url(r'^([^/]*)$', 'museos.views.usuario'),
]
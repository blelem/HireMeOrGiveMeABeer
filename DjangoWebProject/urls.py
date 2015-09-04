"""
Definition of urls for DjangoWebProject.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from portfolio.forms import BootstrapAuthenticationForm

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'portfolio.views.about', name='about'),
    url(r'^about', 'portfolio.views.about', name='about'),
    url(r'^portfolio', 'portfolio.views.portfolio', name='portfolio'),
    
    url(r'^matchFeatures$', 'imageCV.views.matchFeatures', name='matchFeatures'),
    url(r'^matchFeatures/merge$', 'imageCV.views.merge', name='merge'),
    url(r'^imageSelection', 'imageCV.views.imageSelection'),
    url(r'^imageUpload', 'imageCV.views.imageUpload'),
    url(r'^setSessionProperties$', 'imageCV.views.setSessionProperties'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'portfolio/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

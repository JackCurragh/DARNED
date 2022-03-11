from django.conf.urls.defaults import *
from views import *
from admin_views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns( '',
    # front pages
    ( r'^$', front, {'template_name':'search.html'} ),
    ( r'^about/$', front, {'template_name':'about.html'} ),
    ( r'^download/$', front, {'template_name':'download.html'} ),
    ( r'^cite/$', front, {'template_name':'cite.html'} ),
    ( r'^help/$', front, {'template_name':'help.html'} ),
    ( r'^contact/$', front, {'template_name':'contact.html'} ),
    # (r'^login/$',front,{'template_name':'login.html'}),
    # (r'^passwdrecovery/$',front,{'template_name':'recoverpass.html'}),
    # (r'^newuser/$',front,{'template_name':'register.html'}),
    # Example:
    # (r'^DARNED/', include('DARNED.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls'

    # Human Section
    ( r'^HSresultR/$', 'Human.views.range_based' ),
    ( '^HSresultG/$', 'Human.views.geneBased' ),
    ( r'^HSresultS/$', 'Human.views.seq_based' ),
    # Drosophila Section
    ( r'^DMresultR/$', 'Drosophila.views.range_based' ),
    ( '^DMresultG/$', 'Drosophila.views.geneBased' ),
    ( r'^DMresultS/$', 'Drosophila.views.seq_based' ),
     # Mouse Section
    ( r'^MMresultR/$', 'Mouse.views.range_based' ),
    ( r'^MMresultS/$', 'Mouse.views.seq_based' ),
    ( r'^MMresultG/$', 'Mouse.views.geneBased' ),
    # CodonSubstitutions
    ( r'^codon_substitution/$', 'CodonSubstitution.views.wwwcodon' ),
    # ( r'^amino/$', 'CodonSubstitution.views2.wwwcodon2' ),
    # Admin Section
    ( r'^upload/$', upload_file ),
    ( r'^sync/$', sync ),
    # Uncomment the next line to enable the admin:
    ( r'^admin/', include( admin.site.urls ) ),
 )

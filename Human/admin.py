from models import *
from django.contrib import admin
from django.core.urlresolvers import reverse


class CoordinateAdmin(admin.ModelAdmin):
    search_fields = ['coordinate']
    list_display = ('assembly','chrom','coordinate','strand','gene')
    filter_horizontal = ('source','snpvalidation','pubid',)

class GeneAdmin(admin.ModelAdmin):
    search_fields = ['gene']
    list_display = ('gene','geneid')

admin.site.register(HSCoordinate,CoordinateAdmin)
admin.site.register(HSGene,GeneAdmin)
admin.site.register(HSSource)
admin.site.register(HSPubMed)

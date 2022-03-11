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

admin.site.register(MMCoordinate,CoordinateAdmin)
admin.site.register(MMGene,GeneAdmin)
admin.site.register(MMSource)
admin.site.register(MMPubMed)

from models import *
from django.contrib import admin
from django.core.urlresolvers import reverse


class CoordinateAdmin(admin.ModelAdmin):
    search_fields = ['coordinate']
    list_display = ('chrom','coordinate','strand','gene')
    filter_horizontal = ('pubid',)

class GeneAdmin(admin.ModelAdmin):
    search_fields = ['gene']
    list_display = ('gene','geneid')

admin.site.register(DMCoordinate,CoordinateAdmin)
admin.site.register(DMGene,GeneAdmin)
admin.site.register(DMPubMed)

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext
from forms import *
import os

pth = '/home/DATA/Anmol/DARNED/staticfiles/bed/'#'/home/common_share/DARNED/staticfiles/bed/'

def front(request,template_name):
    template = get_template(template_name)
    var = {}
    if template_name=='search.html':
        var = {
#                'cs':Common_Searches(),
                'hss':HS_Searches(),
                'dms':DM_Searches(),
		'mms':MM_Searches()
              }
    return HttpResponse(template.render(RequestContext(request,var)))

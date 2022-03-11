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
                'cs':Common_Searches(),
                'hss':HS_Searches(),
                'dms':DM_Searches()
              }
    #elif template_name == 'login.html':
    #    var = {'lgn':Login()}
    #elif template_name == 'register.html':
    #    var =  {'nwusr':Newuser()}
    #elif template_name == 'recoverpass.html':
    #    var = {'rcvr':Passrec()}
    return HttpResponse(template.render(RequestContext(request,var)))

def bedfile(request):
    name = request.GET['filename']
    fl = open('%s%s'%(pth,name))
    data = fl.read()
    fl.close()
    tmplt = get_template('bedfile.txt')
    return HttpResponse(tmplt.render(RequestContext(request,{'var':data})))

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from forms import *
from django.template import loader,RequestContext

from django.contrib.admin.views.decorators import staff_member_required




##########################
from models import *
from os import system

##############################################
########Thoughts for implementation##########
#Current state of update########

# Try to add information about assembly. And make it auto updatable  
def saveData(uploadedFileName):
    uploadedfile = str(uploadedFileName)
# saving input file content
    destination = open('/home/DATA/Anmol/DARNED/uploadedFiles/Dmel/%s'%(uploadedfile),'wb+')
    for chunk in uploadedFileName.chunks():
        destination.write(chunk)
    destination.close()
def dataCheck(flname):
    infile = open("/home/DATA/Anmol/DARNED/uploadedFiles/Dmel/%s"%(flname))
    for line in infile:
        data = line[:-1].split('\t')
        main = Main.objects.filter(chrom=data[0],coordinate=int(data[1]),strand=data[2])
        if len(main) != 0:
            pbd = main.filter(pubid__pubid=data[7])
            if len(pbd) == 0:
                try:
                    pbdx = PubId.objects.get(pubid=data[7])
                except:
                    pbdx = PubId.objects.create(pubid = data[7],author= data[8],year=int(data[9]))
                main.pubid.add(pbdx)

        else:
            main = Main.objects.create(chrom=data[0],coordinate=int(data[1]),strand=data[2], dnanuc="A",rnanuc="I",seqtype = data[4])

            if data[3] != '-':
                if data[4] == 'E':
                    main.exotype = data[5]
                try:
                    gene = Gene.objects.get(gene=data[3])
                except:
                    gene = Gene.objects.create(gene=data[3],ncbi='-')
                main.gene = gene
            if data[6] != '-':
                main.alu = data[6]
            try:
                pbd = PubId.objects.get(pubid=data[7])
            except:
                pbd = PubId.objects.create(pubid = data[7],author = data[8],year=int(data[9]))
            main.pubid.add(pbd)
            main.save()

    infile.close()


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            filename = request.FILES['infile']
            flname =  str(filename)
            saveData(request.FILES['infile'])
            dataCheck(flname)


 #return HttpResponseRedirect('/success/url/')# Write about successful file upload and logs on page.redirect link using a midddle file. put that file in temp folder
    else:
        form = UploadFileForm()
    toform = {
            'form':form,
            'action':'/du/'
            }
    tmplt = loader.get_template('admin/uploadfile.html')
    return HttpResponse(tmplt.render(RequestContext(request,toform)))
#    return render_to_response('/home/manu/Desktop/DARNED/templates/admin/uploadfile.html',{'form':form})

upload_file = staff_member_required(upload_file)# This is make function acceible only to administers


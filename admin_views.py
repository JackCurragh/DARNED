from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from admin_forms import *
from django.template import loader,RequestContext

from django.contrib.admin.views.decorators import staff_member_required

from Human.models import *
from Drosophila.models import *
from Mouse.models import *
#######UCSC Tables########
###For UCSC gene, SNP and Alu#####


##########################
#from models import *
from os import system

##############################################
########Thoughts for implementation##########
#Current state of update########

pth = "/home/DATA/Anmol/DARNED/uploaded_data/"#"/home/common_share/DARNED/uploaded_data"
dbpth= "/home/DATA/Anmol/DARNED/"#"/home/common_share/DARNED"
# Try to add information about assembly. And make it auto updatable  
def saveData(uploadedFileName):
    uploadedfile = str(uploadedFileName)

# saving input file content
    #print uploadedfile
    destination = open('%s/%s'%(pth,uploadedfile),'wb+')
    for chunk in uploadedFileName.chunks():
        destination.write(chunk)
    destination.close()

######Human update start########
def human(flname):
    infile = open("%s/%s"%(pth,flname))
    outfile = open("%s/%s.err"%(pth,flname),"w")
    for line in infile:
        data = line[:-1].split('\t')
            #tmplt = loader.
         #   print "Send Error that it is no related to humans"
        coor = HSCoordinate.objects.filter(assembly=int(data[0]),chrom=data[1],coordinate=int(data[2]),strand=data[3],indna = data[4],inref = data[5], inrna = data[6])#add nucleotide info
        if len(coor) != 0:
            if data[15] != '-':
                tissues = data[15].split(',')
                for tissue in tissues:
                    if len(tissue)<2:
                        continue
                    #print tissue.upper(),"Anmol"
                    tis = coor.filter(source__source = tissue.upper())
                    if len(tis) == 0:
                        try:
                            tss = HSSource.objects.get(source=tissue.upper())
                        except:
                            tss = HSSource.objects.create(source=tissue.upper())
                        for cr in coor:
                            cr.source.add(tss)
            pubids = data[16].split(':')
            authors = data[17].split(':')
            years = data[18].split(':')
            pubnum = len(pubids)
            for j in range(pubnum):
                pbd = coor.filter(pubid__pubid=pubids[j])
                if len(pbd) == 0:
                    try:
                        pbdx = HSPubMed.objects.get(pubid=pubids[j])
                    except:
                        pbdx = HSPubMed.objects.create(pubid = pubids[j],author=authors[j],year=years[j])
                    for cr in coor:
                        cr.pubid.add(pbdx)

        else:
            coor = HSCoordinate.objects.create(assembly=int(data[0]),chrom=data[1],coordinate=int(data[2]),strand=data[3], indna=data[4],inref=data[5],inrna=data[6],seqtype = data[12])
            if data[7] != '-':
                coor.snp =  data[7]
                if data[8]=='+':
                    coor.snpunvalid = 1
                else:
                    coor.snpunvalid = 0
                validations = data[9].split(',')
                for validation in validations:
                    try:
                        vld = HSSnpValidation.objects.get(validation=validation)
                    except:
                        vld = HSSnpValidation.objects.create(validation=validation)
                    coor.snpvalidation.add(vld)
            #print data[11]
            if data[10] != '-':
                if data[12] == 'E':
                    coor.exotype = data[13]
                try:
                    gene = HSGene.objects.get(gene=data[10])
                except:
                    #print data[10],data[11],data[12],data[13]
                    gene = HSGene.objects.create(gene=data[10],geneid=int(data[11]))
                coor.gene = gene
            if data[14] != '-':
                coor.alu = data[14]
            if data[15] != '-':
                sources = data[15].split(',')
                for source in sources:
                    if len(source) <2:
                        continue
                    try:
                        src = HSSource.objects.get(source = source.upper())
                    except:
                        src = HSSource.objects.create(source = source.upper())
                    coor.source.add(src)
            pubmeds = data[16].split(':')
            authors = data[17].split(':')
            years = data[18].split(':')
            pubnum = len(pubmeds)
            for j in range(pubnum):
                try:
                    pbd = HSPubMed.objects.get(pubid=pubmeds[j])
                except:
                    pbd = HSPubMed.objects.create(pubid = pubmeds[j],author = authors[j],year=years[j])
                coor.pubid.add(pbd)
            coor.save()

    infile.close()
    outfile.close()


#######Human update End######

########Drosophila Update Start#######

def drosophila(flname):#add assembly and from to and refid
    infile = open("%s/%s"%(pth,flname))
    for line in infile:
        data = line[:-1].split('\t')
        coor = DMCoordinate.objects.filter(assembly=data[0],chrom=data[1],coordinate=int(data[2]),strand=data[3],indna=data[4],inref=data[5],inrna=data[6])
        if len(coor) != 0:
            pbd = coor.filter(pubid__pubid=data[12])
            if len(pbd) == 0:
                try:
                    pbdx = DMPubMed.objects.get(pubid=data[12])
                except:
                    pbdx = DMPubMed.objects.create(pubid = data[12],author= data[13],year=data[14])
                for cr in coor:
                    cr.pubid.add(pbdx)

        else:
            coor = DMCoordinate.objects.create(assembly=data[0],chrom=data[1],coordinate=int(data[2]),strand=data[3], indna=data[4],inref=data[5],inrna=data[6],seqtype = data[9])

            if data[7] != '-':
                if data[9] == 'E':
                    coor.exotype = data[10]
                try:
                    gene = DMGene.objects.get(gene=data[7])
                except:
                    gene = DMGene.objects.create(gene=data[7],geneid=data[8])
                coor.gene = gene
            if data[11] != '-':
                coor.alu = data[11]
            try:
                pbd = DMPubMed.objects.get(pubid=data[12])
            except:
                pbd = DMPubMed.objects.create(pubid = data[12],author = data[13],year=data[14])
            coor.pubid.add(pbd)
            coor.save()

    infile.close()

######Drosophila update End#####


########Mouse Update Start#######
def mouse(flname):
    infile = open("%s/%s"%(pth,flname))
    outfile = open("%s/%s.err"%(pth,flname),"w")
    for line in infile:
        data = line[:-1].split('\t')
        #print data
            #tmplt = loader.
            #print "Send Error that it is no related to humans"
        coor = MMCoordinate.objects.filter(assembly=int(data[0]),chrom=data[1],coordinate=int(data[2]),strand=data[3],indna = data[4],inref = data[5], inrna = data[6])#add nucleotide info
        if len(coor) != 0:
            if data[15] != '-':
                tissues = data[15].split(',')
                for tissue in tissues:
                    if len(tissue)<2:
                        continue
                    #print tissue.upper(),"Anmol"
                    tis = coor.filter(source__source = tissue.upper())
                    if len(tis) == 0:
                        try:
                            tss = MMSource.objects.get(source=tissue.upper())
                        except:
                            tss = MMSource.objects.create(source=tissue.upper())
                        for cr in coor:
                            cr.source.add(tss)
            pubids = data[16].split(':')
            authors = data[17].split(':')
            years = data[18].split(':')
            pubnum = len(pubids)
            for j in range(pubnum):
                pbd = coor.filter(pubid__pubid=pubids[j])
                if len(pbd) == 0:
                    try:
                        pbdx = MMPubMed.objects.get(pubid=pubids[j])
                    except:
                        pbdx = MMPubMed.objects.create(pubid = pubids[j],author=authors[j],year=years[j])
                    for cr in coor:
                        cr.pubid.add(pbdx)

        else:
            coor = MMCoordinate.objects.create(assembly=int(data[0]),chrom=data[1],coordinate=int(data[2]),strand=data[3], indna=data[4],inref=data[5],inrna=data[6],seqtype = data[12])
            if data[7] != '-':
                coor.snp =  data[7]
                if data[8]=='+':
                    coor.snpunvalid = 1
                else:
                    coor.snpunvalid = 0
                validations = data[9].split(',')
                for validation in validations:
                    try:
                        vld = MMSnpValidation.objects.get(validation=validation)
                    except:
                        vld = MMSnpValidation.objects.create(validation=validation)
                    coor.snpvalidation.add(vld)
            #print data[11]
            if data[10] != '-':
                if data[12] == 'E':
                    coor.exotype = data[13]
                try:
                    gene = MMGene.objects.get(gene=data[10])
                except:
                    #print data[10],data[11],data[12],data[13]
                    gene = MMGene.objects.create(gene=data[10],geneid=int(data[11]))
                coor.gene = gene
            if data[14] != '-':
                coor.alu = data[14]
            if data[15] != '-':
                sources = data[15].split(',')
                for source in sources:
                    if len(source) <2:
                        continue
                    try:
                        src = MMSource.objects.get(source = source.upper())
                    except:
                        src = MMSource.objects.create(source = source.upper())
                    coor.source.add(src)
            pubmeds = data[16].split(':')
            authors = data[17].split(':')
            years = data[18].split(':')
            pubnum = len(pubmeds)
            for j in range(pubnum):
                try:
                    pbd = MMPubMed.objects.get(pubid=pubmeds[j])
                except:
                    pbd = MMPubMed.objects.create(pubid = pubmeds[j],author = authors[j],year=years[j])
                coor.pubid.add(pbd)
            coor.save()

    infile.close()
    outfile.close()
#####Mouse Update End ##################


def upload_file(request):
    if request.method == 'POST':
        form = File_Upload(request.POST,request.FILES)
        if form.is_valid():
            filename = request.FILES['filename']
	    org = request.POST['org']
	    #exit(1)
            flname =  str(filename)
            saveData(request.FILES['filename'])
            if org=='HU':
                human(flname)
            elif org=='DR':
                drosophila(flname)
            elif org=='MO':
                mouse(flname)


 #return HttpResponseRedirect('/success/url/')# Write about successful file upload and logs on page.redirect link using a midddle file. put that file in temp folder
#    else:
    form = File_Upload()
    toform = {'form':form,
              'action':'/upload/'#it was /hu/
            }
    tmplt = loader.get_template('admin/data_upload.html')
    return HttpResponse(tmplt.render(RequestContext(request,toform)))
#    return render_to_response('/home/manu/Desktop/DARNED/templates/admin/uploadfile.html',{'form':form})

def sync(request):
###Human sync##########
    for j in range(18,20):
        hsfile = open("%s/staticfiles/downloads/hg%d.txt"%(dbpth,j),"w")
        hsfile.write("chrom\tcoordinate\tstrand\tinchr\tinrna\tgene\tseqReg\texReg\tsource\tPubMed ID\n")
        coors = HSCoordinate.objects.filter(assembly=j)
        for coor in coors:
            tsource = ""
            tpub = ""
            tgene = ""
            tseq = "O"
            texo = ""
            if coor.gene != None:
                tgene = coor.gene.gene
                if coor.exotype !=None:
                    tseq = "E"
                    texo = coor.exotype
                else:
                    tseq = "I"
            for src in coor.source.all():
                tsource += ",%s"%src.source
            for pbd in coor.pubid.all():
                tpub +=",%d"%pbd.pubid
            hsfile.write("%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(coor.chrom,coor.coordinate,coor.strand,coor.indna,coor.inrna,tgene,tseq,texo,tsource[1:],tpub[1:]))
        hsfile.close()

###Mouse sync##########
    for j in range(9,11):
        mmfile = open("%s/staticfiles/downloads/mm%d.txt"%(dbpth,j),"w")
        mmfile.write("chrom\tcoordinate\tstrand\tinchr\tinrna\tgene\tseqReg\texReg\tsource\tPubMed ID\n")
        coors = MMCoordinate.objects.filter(assembly=j)
        for coor in coors:
            tsource = ""
            tpub = ""
            tgene = ""
            tseq = "O"
            texo = ""
            if coor.gene != None:
                tgene = coor.gene.gene
                if coor.exotype !=None:
                    tseq = "E"
                    texo = coor.exotype
                else:
                    tseq = "I"
            #for src in coor.source.all():
             #   tsource += ",%s"%src.source
            for pbd in coor.pubid.all():
                tpub +=",%d"%pbd.pubid
            mmfile.write("%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(coor.chrom,coor.coordinate,coor.strand,coor.indna,coor.inrna,tgene,tseq,texo,tsource[1:],tpub[1:]))
        mmfile.close()


####Drosophila Sync###########
    for j in range(3,4):
        dmfile = open("%s/staticfiles/downloads/dm%d.txt"%(dbpth,j),"w")
        dmfile.write("chrom\tcoordinate\tstrand\tinchr\tinrna\tgene\tseqReg\texReg\tPubMed ID\n")
        coors = DMCoordinate.objects.filter(assembly=3)
        for coor in coors:
            tpub=""
            tgene = ""
            tseq = "O"
            texo = ""
            if coor.gene != None:
                tgene=coor.gene.gene
                if coor.exotype != None:
                    tseq = "E"
                    texo = coor.exotype
                else:
                    tseq="I"
            for pbd in coor.pubid.all():
                tpub += ",%d"%pbd.pubid
            dmfile.write("%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(coor.chrom,coor.coordinate,coor.strand,coor.indna,coor.inrna,tgene,tseq,texo,tpub[1:]))
        dmfile.close()
    tmplt = loader.get_template("message.html")
    return HttpResponse(tmplt.render(RequestContext(request,{'message':'Update finished'})))



upload_file = staff_member_required(upload_file)# This is make function acceible only to administers

sync = staff_member_required(sync)
# Remove delete options from default admin page. It may create trouble, If you don't remove. 

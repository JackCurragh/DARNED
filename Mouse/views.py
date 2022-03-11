# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext,loader
from time import time
import MySQLdb
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from DARNED.forms import *
from models import *
from os import system
from xml.dom import minidom

#pth = '/home/devil/Chinese/darned_temp/'
dbpth = "/home/DATA/Anmol/DARNED"#'/home/common_share/DARNED'
sttc = dbpth+'/staticfiles'
blstdb = dbpth+'/blast_databases/Mouse'

def range_based(request):
    assembly = request.GET['mm_assembly']
    chrom = request.GET['mm_chrom']
    seqtype = request.GET['mm_seqtype']
#    print seqtype,type(seqtype)
    exotype = request.GET['mm_exotype']
    flank = request.GET['mm_flank']
    gene = request.GET.get('gene','')
    pubid = request.GET.get('pubid','')
#    source = request.GET.get('mm_source','')
    end = request.GET.get('mm_end','0')
    start = request.GET.get('mm_start','0')
    try:
        end = int(end)
        start = int(start)
        flank = int(flank)
    except:
        tmplt = loader.get_template("message.html")
        return HttpResponse(tmplt.render(RequestContext(request,{'message':'Invalid Arguments'})))
    coors = MMCoordinate.objects.filter(assembly=assembly,chrom=chrom,coordinate__gte=start,coordinate__lte=end).select_related(depth=2).extra(select={'gstart':'coordinate-%d'%int(flank),'gend':'coordinate+%d'%int(flank)}).order_by('coordinate')
    if seqtype !='A':
        if seqtype == 'E':
            if exotype=='A':
                coors = coors.filter(seqtype='E')
            elif exotype == 'C':
                coors = coors.filter(exotype='C')
            elif exotype == '5':
                coors = coors.filter(exotype='5')
            elif exotype == '3':
                coors = coors.filter(exotype='3')
        elif seqtype == 'I':
            coors = coors.filter(seqtype='I')
        else:
            coors = coors.filter(seqtype='O')
#    if source != '':
#        coors = coors.filter(source__source = source)
    if pubid != '':
        coors = coors.filter(pubid__pubid=pubid)
    if gene != '':
        coors = coors.filter(gene__gene=gene)
    if len(coors) ==0:
        tmplt = loader.get_template("message.html")
        return HttpResponse(tmplt.render(RequestContext(request,{'message':'No result found for your query'})))
#############Bed File Part##########
    countfile = open(dbpth+"/count")
    count = int(countfile.read())
    countfile.close()
    countfile = open(dbpth+"/count",'w')
    countfile.write("%d"%((count+1)%200))
    countfile.close()
    bedfile = open("%s/bed/bed_%d.bed"%(sttc,count),"w")
    resultFile = open("%s/res/results%d.txt"%(sttc,count),'w')
    bedfile.write('browser dense\ntrack name="Human RNA Editing" description="EDITING LOCATIONS" visibility=2 itemRgb="On"\n')
    resultFile.write("chrom\tcoordinate\tstrand\tinchr\tinrna\tgene\tseqReg\texReg\tsource\tPubMed ID\n")
    for coor in coors:#need coloring here
        barcolor=""
#        tsource = ""
        tpub=""
        tgene=""
        tseq = 'O'
        texo = ""
        if coor.gene != None:
            tgene = coor.gene.gene
            if coor.exotype != None:
                tseq = "E"
                texo = coor.exotype
            else:
                tseq="I"
#        for src in coor.source.all():
#            tsource +=",%s"%src.source
        for pbd in coor.pubid.all():
            tpub += ",%d"%pbd.pubid
        resultFile.write("%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(coor.chrom,coor.coordinate,coor.strand,coor.indna,coor.inrna,tgene,tseq,texo,tpub[1:]))
	#Other Black 0-0-0
        #Intron Red  255-0-0
        #CDS Blue    0-0-255
        #5UTR Dark Green 0-100-0
        #3UTR Deep Pink	255-20-147
        if coor.seqtype=='O':
            barcolor = '0,0,0'
        elif coor.seqtype=='I':
            barcolor='255,0,0'
        else:
            if coor.exotype=='C':
                barcolor='0,0,255'
            elif coor.exotype=='5':
                barcolor='0,100,0'
            else:
                barcolor='255,20,147'
        bedfile.write("chr%s\t%d\t%d\tchr%s.%d\t1000\t%s\t%d\t%d\t%s\n"%(coor.chrom,coor.coordinate-1,coor.coordinate,coor.chrom,coor.coordinate,coor.strand,coor.coordinate-1,coor.coordinate,barcolor))
    bedfile.close()
    resultFile.close()
###################################
#    tissuesearch = "mm_assembly=%s&mm_chrom=%s&mm_seqtype=%s&mm_exotype=%s&mm_flank=%s&gene=%s&pubid=%s&mm_start=%s&mm_end=%s&mm_source="%(assembly,chrom,seqtype,exotype,flank,gene,pubid,start,end)
    genesearch = "mm_assembly=%s&mm_chrom=%s&mm_seqtype=%s&mm_exotype=%s&mm_flank=%s&pubid=%s&mm_start=%s&mm_end=%s&gene="%(assembly,chrom,seqtype,exotype,flank,pubid,start,end)
    authorsearch = "mm_assembly=%s&mm_chrom=%s&mm_seqtype=%s&mm_exotype=%s&mm_flank=%s&gene=%s&mm_start=%s&mm_end=%s&pubid="%(assembly,chrom,seqtype,exotype,flank,gene,start,end)
    exonsearch = "mm_assembly=%s&mm_chrom=%s&seqtype=%s&mm_flank=%s&gene=%s&pubid=%s&mm_start=%s&mm_end=%s&mm_exotype="%(assembly,chrom,seqtype,flank,gene,pubid,start,end)
    seqsearch = "mm_assembly=%s&mm_chrom=%s&mm_exotype=%s&mm_flank=%s&gene=%s&pubid=%s&mm_start=%s&mm_end=%s&mm_seqtype="%(assembly,chrom,exotype,flank,gene,pubid,start,end)
    searchRes = {'coors':coors,
#                'tissuesearch':tissuesearch,
                'genesearch':genesearch,
                'authorsearch':authorsearch,
                'exonsearch':exonsearch,
                'seqsearch':seqsearch,
                'assembly':assembly,
                'chrom':chrom,
                'start':start,
                'end':end,
                'seqtype':seqtype,
                'exotype':exotype,
                'gene':gene,
                'bed':count,
                'flank':flank,
                'rescount':len(coors)
                }
    tmplt = loader.get_template('Mouse/result.html')
    rendred = tmplt.render(RequestContext(request,searchRes))
    return HttpResponse(rendred)
#############################################################################
#############################################################################
#######For sequence based analysis###########################################

###########Checking nucleotide sequence######################################
def nucleotide_check(seq):#
    nuc = set()
    nucl_bool = 0
    for line in seq:
        nuc |= set([c for c in line if c not in ' \n\r'])
    for n in nuc:
        if n.upper() not in ('ACGTRYKMSWBDHVNU'):#Replace if it gives error
            nucl_bool = 1
            break
    return nucl_bool
###########################Checking fasta file format########################
def fasta_nucleotide_check(fl):
    infile = open(fl)
    lines = infile.readlines()
    fasta_bool = 0
    if lines[0][0] == '>':
        fasta_bool = 1
    if fasta_bool == 1:
        dna_bool = nucleotide_check(lines[1:])
    else:
        dna_bool = nucleotide_check(lines)
    return fasta_bool,dna_bool
def seq_based(request):
    if request.method == 'POST':
        assembly =request.POST['mm_assembly']
        countfile = open(dbpth+"/count")
        count = int(countfile.read())
        countfile.close()
        countfile = open(dbpth+"/count",'w')
        countfile.write("%d"%((count+1)%200))
        countfile.close()
        fl = "%s/tmp/seq%d.fa"%(dbpth,count)
        seqfile = open(fl,"w")
        seqfile.write(request.POST['mm_seq'])
        seqfile.close()
	fasta_bool,dna_bool = fasta_nucleotide_check(fl)
	if dna_bool:
            tmplt = loader.get_template('message.html')
            return HttpResponse(tmplt.render(RequestContext(request,{'message':'Input file is not a DNA or RNA sequence file.<br /> Please go to searc page again'})))
	if not fasta_bool:
	    infile = open(fl)
	    seq = infile.read()
            infile.close()
	    outfile = open(fl, "w")
	    outfile.write(">userseq\n"+seq)
	    outfile.close()
			
        system ("%s/exe/blastn -max_target_seqs 1 -evalue 10 -word_size 50 -outfmt 5 -dust no -db %s/mm%s/mm%s -query %s/tmp/seq%d.fa -out %s/tmp/seq%d.xml"%(dbpth,blstdb,assembly,assembly,dbpth,count,dbpth,count))
        xmldoc = minidom.parse("%s/tmp/seq%d.xml"%(dbpth,count))
        hits = xmldoc.getElementsByTagName('Hit')
        if len(hits)==0:
            tmplt = loader.get_template('message.html')
            return HttpResponse(tmplt.render(RequestContext(request,{'message':'No hit found for your sequence'})))
        data = []
        for hit in hits:
            chrom = hit.getElementsByTagName('Hit_def')[0].firstChild.data
            hit_hsps = hit.getElementsByTagName('Hit_hsps')
            for hit_hsp in hit_hsps:
                hsps = hit_hsp.getElementsByTagName('Hsp')
                for hsp in hsps:
                    tstart = int(hsp.getElementsByTagName('Hsp_hit-from')[0].firstChild.data)
                    tend = int(hsp.getElementsByTagName('Hsp_hit-to')[0].firstChild.data)
                    qstart = int(hsp.getElementsByTagName('Hsp_query-from')[0].firstChild.data)
                    strnd = hsp.getElementsByTagName('Hsp_hit-frame')[0].firstChild.data
                    qseq = hsp.getElementsByTagName('Hsp_qseq')[0].firstChild.data
                    tseq = hsp.getElementsByTagName('Hsp_hseq')[0].firstChild.data
                    match = hsp.getElementsByTagName('Hsp_midline')[0].firstChild.data
                    if strnd == '1':
                        strand = '+'
                    else:
                        strand = '-'
                        tstart,tend = tend,tstart
                    data.append([chrom[3:],tstart,tend,strand,[],assembly])
                    arraylen = len(data)
                    coord = []
                    editings = MMCoordinate.objects.filter(assembly=assembly,chrom=chrom[3:], coordinate__gte = tstart, coordinate__lte= tend, strand = strand)
                    for editing in editings:
                        if strand == '+':
                            coord.append(editing.coordinate)
                        else:
                            coord.append(editing.coordinate)
                    coord.sort()
                    trealpos = tstart
                    qrealpos = qstart
                    startbl = 0
                    spl = 0
                    nml = 0
                    qseqt = ""
                    tseqt = ""
                    matcht = ""
                    virtualSeqLen = len(tseq)
                    for j in range(virtualSeqLen):
                        if (j != 0 and j%50 == 0) or j == virtualSeqLen-1:
                            tseqt += "</b></td>"
                            qseqt += "</b></td>"
                            matcht += "</pre></b></td>"
                            if strand == '+':
                                data[arraylen-1][4].append([qstartpos,tstartpos,qseqt,matcht,tseqt,qrealpos-1,trealpos-1])
                            else:
                                data[arraylen-1][4].append([qstartpos,tend-tstartpos+tstart,qseqt,matcht,tseqt,qrealpos-1,tend+tstart-trealpos+1])
                            startbl = 0
                            spl = 0
                            nml = 0
                            qseqt = ""
                            tseqt = ""
                            matcht = ""
                        if startbl == 0:
                            qstartpos = qrealpos
                            tstartpos = trealpos
                            startbl = 1
                        if tseq[j] != '-':
                            trealpos += 1
                        if qseq[j] != '-':
                            qrealpos += 1
                        if trealpos-1 in coord:
                            if spl == 0 :
                                tseqt += "<td><b>"
                                qseqt += "<td><b>"
                                matcht += "<td><b><pre>"
                                spl = nml = 1
                            tseqt += "<font style='background-color:#BDBDBD'>%s</font>"%tseq[j]
                            qseqt += "<font style='background-color:#BDBDBD'>%s</font>"%qseq[j]
                            matcht += "<font style='background-color:#BDBDBD'>%s</font>"%match[j]
                        else:
                            if nml == 0:
                                tseqt += "<td><b>%s"%tseq[j]
                                qseqt += "<td><b>%s"%qseq[j]
                                matcht += "<td><b><pre>%s"%match[j]
                                nml = spl = 1
                            else:
                                tseqt += tseq[j]
                                qseqt += qseq[j]
                                matcht += match[j]

            tmplt = loader.get_template("Mouse/blast.html")
            return HttpResponse(tmplt.render(RequestContext(request,{'datas':data,'assembly':assembly})))
    else:
        tmplt = loader.get_template("message.html")
        return HttpResponse(tmplt.render(RequestContext(request,{'message':"Please go to search for query submission. "})))




####################Gene Based Searches#############################################

def geneBased(request):# Remove EST from Hereford
    if request.method == 'POST':
	seqname = request.POST['mm_seqid']
	if len(seqname) == 0:
            tmplt = loader.get_template("message.html")
            return HttpResponse(tmplt.render(RequestContext(request, {'message':"Please go back to search page and provide query RefGene or RefSeq ID."})))
        assembly = request.POST['mm_assembly']
        seqtype = request.POST['mm_seqname']
        bl = 0
	gene = ''
        if seqtype == "refGene":
	    gene = seqname.upper()
            coors = MMCoordinate.objects.filter(assembly=assembly,gene__gene=seqname.upper())
            if len(coors)>0:
                bl = 1
        elif seqtype == "refSeq":
            conn = MySQLdb.connect(db='darned_mm%s'%assembly)
            cursor = conn.cursor()
            if cursor.execute("SELECT name2 from refGene WHERE name='%s' LIMIT 1"%(assembly,seqname)):
                gene = cursor.fetchone()[0]
                coors = MMCoordinate.objects.filter(assembly=assembly,gene__gene=gene)
                if len(coors)>0:
                    bl = 1
            cursor.close()
            conn.close()
        if bl==1:
	#############Bed File Part##########
	    countfile = open(dbpth+"/count")
	    count = int(countfile.read())
	    countfile.close()
	    countfile = open(dbpth+"/count",'w')
	    countfile.write("%d"%((count+1)%200))
	    countfile.close()
	    bedfile = open("%s/bed/bed_%d.bed"%(sttc,count),"w")
	    resultFile = open("%s/res/results%d.txt"%(sttc,count),'w')
	    bedfile.write('browser dense\ntrack name="Human RNA Editing" description="EDITING LOCATIONS" visibility=2 itemRgb="On"\n')
	    resultFile.write("chrom\tcoordinate\tstrand\tinchr\tinrna\tgene\tseqReg\texReg\tsource\tPubMed ID\n")
            coordinate = []
	    for coor in coors:#need coloring here
                chrom = coor.chrom
		barcolor=""
		tsource = ""
		tpub=""
                tgene=""
                tseq = "O"
                texo = ""
                coordinate.append(coor.coordinate)
                if coor.gene != None:
                    tgene=coor.gene.gene
                    if coor.exotype !=None:
                        tseq="E"
                        texo=coor.exotype
                    else:
                        tseq="I"
		#for src in coor.source.all():
		 #   tsource +=",%s"%src.source
		for pbd in coor.pubid.all():
		    tpub += ",%d"%pbd.pubid
		resultFile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(coor.chrom,coor.coordinate,coor.strand,coor.indna,coor.inrna,tgene,tseq,texo,tpub[1:]))
		#Other Black 0-0-0
		#Intron Red  255-0-0
		#CDS Blue    0-0-255
		#5UTR Dark Green 0-100-0
		#3UTR Deep Pink	255-20-147
		if coor.seqtype=='O':
		    barcolor = '0,0,0'
		elif coor.seqtype=='I':
		    barcolor='255,0,0'
		else:
		    if coor.exotype=='C':
		        barcolor='0,0,255'
		    elif coor.exotype=='5':
		        barcolor='0,100,0'
		    else:
		        barcolor='255,20,147'
		bedfile.write("chr%s\t%d\t%d\tchr%s.%d\t1000\t%s\t%d\t%d\t%s\n"%(coor.chrom,coor.coordinate-1,coor.coordinate,coor.chrom,coor.coordinate,coor.strand,coor.coordinate-1,coor.coordinate,barcolor))
	    bedfile.close()
	    resultFile.close()
	###################################
	    seqtype = 'A'
	    exotype = 'A'
	    flank = '0'
	    pubid = ''
	    source = ''
	    end = max(coordinate)+1
	    start = min(coordinate)-1
	    tissuesearch = "hs_assembly=%s&hs_chrom=%s&seqtype=%s&exotype=%s&flank=%s&gene=%s&pubid=%s&start=%s&end=%s&hs_source="%(assembly,chrom,seqtype,exotype,flank,gene,pubid,start,end)
	    genesearch = "hs_assembly=%s&hs_chrom=%s&seqtype=%s&exotype=%s&flank=%s&hs_source=%s&pubid=%s&start=%s&end=%s&gene="%(assembly,chrom,seqtype,exotype,flank,source,pubid,start,end)
	    authorsearch = "hs_assembly=%s&hs_chrom=%s&seqtype=%s&exotype=%s&flank=%s&gene=%s&hs_source=%s&start=%s&end=%s&pubid="%(assembly,chrom,seqtype,exotype,flank,gene,source,start,end)
	    exonsearch = "hs_assembly=%s&hs_chrom=%s&seqtype=%s&hs_source=%s&flank=%s&gene=%s&pubid=%s&start=%s&end=%s&exotype="%(assembly,chrom,seqtype,source,flank,gene,pubid,start,end)
	    seqsearch = "hs_assembly=%s&hs_chrom=%s&hs_source=%s&exotype=%s&flank=%s&gene=%s&pubid=%s&start=%s&end=%s&seqtype="%(assembly,chrom,source,exotype,flank,gene,pubid,start,end)
	    searchRes = {'coors':coors,
			'tissuesearch':tissuesearch,
			'genesearch':genesearch,
			'authorsearch':authorsearch,
			'exonsearch':exonsearch,
			'seqsearch':seqsearch,
			'assembly':assembly,
			'chrom':chrom,
			'start':start,
			'end':end,
			'seqtype':seqtype,
			'exotype':exotype,
			'gene':gene,
                        'bed':count,
                        'rescount':len(coors)
			}

            tmplt = loader.get_template("Mouse/result.html")
            return HttpResponse(tmplt.render(RequestContext(request,searchRes)))
        else:
            tmplt = loader.get_template('message.html')
            return HttpResponse(tmplt.render(RequestContext(request, {'message':"No Result Found"})))
    else:
        tmplt = loader.get_template('message.html')
        return HttpResponse(tmplt.render(RequestContext(request, {'message':"Please go to search page."})))
    



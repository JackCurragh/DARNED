#===============================================================================
# Don't dare to change this code if you don't know what is written here and what
# are you planning to do. :Anmol Kiran
#===============================================================================


# Create your views here.
from django.http import HttpResponseRedirect
# from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.template.loader import get_template
from django.http import HttpResponse
import string

from forms import *



#===============================================================================
# Don't dare to change this code if you don't know what is written here and what
# are you planning to do. :Anmol Kiran
#===============================================================================


# Create your views here.
import string
from Bio import SeqIO
from Bio.Alphabet import *
from Bio.Align.Applications import ClustalwCommandline
from os import system
# Imaginary function to handle an uploaded file.
#===============================================================================
# Codon Informations
#===============================================================================
codon = {'AAA' : 'K', 'ACA' : 'T', 'AGA' : 'R', 'ATA' : 'I',
         'AAC' : 'N', 'ACC' : 'T', 'AGC' : 'S', 'ATC' : 'I',
         'AAG' : 'K', 'ACG' : 'T', 'AGG' : 'R', 'ATG' : 'M',
         'AAT' : 'N', 'ACT' : 'T', 'AGT' : 'S', 'ATT' : 'I',
         'CAA' : 'Q', 'CCA' : 'P', 'CGA' : 'R', 'CTA' : 'L',
         'CAC' : 'H', 'CCC' : 'P', 'CGC' : 'R', 'CTC' : 'L',
         'CAG' : 'Q', 'CCG' : 'P', 'CGG' : 'R', 'CTG' : 'L',
         'CAT' : 'H', 'CCT' : 'P', 'CGT' : 'R', 'CTT' : 'L',
         'GAA' : 'E', 'GCA' : 'A', 'GGA' : 'G', 'GTA' : 'V',
         'GAC' : 'D', 'GCC' : 'A', 'GGC' : 'G', 'GTC' : 'V',
         'GAG' : 'E', 'GCG' : 'A', 'GGG' : 'G', 'GTG' : 'V',
         'GAT' : 'D', 'GCT' : 'A', 'GGT' : 'G', 'GTT' : 'V',
         'TAA' : '*', 'TCA' : 'S', 'TGA' : '*', 'TTA' : 'L',
         'TAC' : 'Y', 'TCC' : 'S', 'TGC' : 'C', 'TTC' : 'F',
         'TAG' : '*', 'TCG' : 'S', 'TGG' : 'W', 'TTG' : 'L',
         'TAT' : 'Y', 'TCT' : 'S', 'TGT' : 'C', 'TTT' : 'F',
         # RNA specific
         'AUA' : 'I', 'AUC' : 'I', 'AUG' : 'M',
         'AAU' : 'N', 'ACU' : 'T', 'AGU' : 'S', 'AUU' : 'I',
         'CUA' : 'L', 'CUC' : 'L', 'CUG' : 'L',
         'CAU' : 'H', 'CCU' : 'P', 'CGU' : 'R', 'CUU' : 'L',
         'GUA' : 'V', 'GUC' : 'V', 'GUG' : 'V',
         'GAU' : 'D', 'GCU' : 'A', 'GGU' : 'G', 'GUU' : 'V',
         'UAA' : '*', 'UCA' : 'S', 'UGA' : '*', 'UUA' : 'L',
         'UAC' : 'Y', 'UCC' : 'S', 'UGC' : 'C', 'UUC' : 'F',
         'UAG' : '*', 'UCG' : 'S', 'UGG' : 'W', 'UUG' : 'L',
         'UAU' : 'Y', 'UCU' : 'S', 'UGU' : 'C', 'UUU' : 'F'
         }
#===============================================================================
# 
#===============================================================================

dbpth = '/home/DATA/Anmol/DARNED'

def wwwcodon( fl ):
    nuc_seq = {}
    aa_pos = {}
    # File for clustalw Nucleotide Alignemnt
    tmpOutfile = open( "%s/tmp/tem_aa.fa" % dbpth, "w" )
    for seq_record in SeqIO.parse( fl, 'fasta' ):
        nuc_seq[seq_record.id] = str( seq_record.seq )
        tmpOutfile.write( ">%s\n%s\n" % ( seq_record.id, str( seq_record.seq.translate() ).replace( '*', 'X' ) ) )
    tmpOutfile.close()
    # Fie close 
    
    # Running clustalw
    cline = ClustalwCommandline( "clustalw2", infile = "%s/tmp/tem_aa.fa" % dbpth , outfile = "%s/tmp/tem_aa.pir" % dbpth )  # filepaths
    cline()
    # End of clustalw
    
    # Reading alignment file, and storing Amino acid information in dictionary
    infile = open( "%s/tmp/tem_aa.pir" % dbpth )  # file path
    alignseq_cds = {}
    alignseq_aa = {}
    for line in infile:
        data = line[:-1].split()
        if 'CLUSTAL' in line or len( data ) != 2 or '*' in data[0]:
            continue
        seqname, seq = data[0], data[1]
        print seq
        if alignseq_aa.has_key( seqname ):
            alignseq_aa[seqname] += seq
        else:
            alignseq_aa[seqname] = seq
    infile.close()
    ####Restoring nucleotides and creating html
    for key in alignseq_aa.keys():
        alignseq_cds[key] = ''
        j = 0
        for c in alignseq_aa[key] :
            if c != '-':
                # print c, nuc_seq[key][j * 3:j * 3 + 3]
                alignseq_cds[key] += nuc_seq[key][j * 3:j * 3 + 3]
                j += 1
            else:
                alignseq_cds[key] += '---'
    codon_color = {}
    for j in range( 0, len( alignseq_cds[alignseq_cds.keys()[0]] ), 3 ):
        tmpcodon = []
        for key in alignseq_cds.keys():
            tmpcodon.append( alignseq_cds[key][j:j + 3] )
        tmpcdn = set( tmpcodon )
        for tmdn in list( tmpcdn ):
            if '-' in tmdn:
                tmpcdn -= set( [tmdn] )        
        cdnCount = []
        tmpcdn = list( tmpcdn )
        for tmdn in tmpcdn:
            cdnCount.append( tmpcodon.count( tmdn ) )
        if cdnCount != []:
            maxcdn = tmpcdn[cdnCount.index( max( cdnCount ) )]
        for key in alignseq_cds.keys():
            if not codon.has_key( alignseq_cds[key][j:j + 3] ) or maxcdn == alignseq_cds[key][j:j + 3] or len( alignseq_cds[key][j:j + 3] ) < 3 or '-' in alignseq_cds[key][j:j + 3]:
                clr = ''
            elif codon[maxcdn] == codon[alignseq_cds[key][j:j + 3]]:
                clr = 'green'
            else:
                clr = '#8A4117'
            if codon.has_key( alignseq_cds[key][j:j + 3] ) and codon[alignseq_cds[key][j:j + 3]] == '*':
                clr = '#E6A9EC'    
            if codon_color.has_key( key ):
                codon_color[key].append( clr )
            else:
                codon_color[key] = [clr]
    to_return = "<html><head></head><body><table>" 
    for key in alignseq_cds.keys():
        to_return += "<tr style='height:5px'><td>%s</td><td></td>" % key 
        for j in range( len( codon_color[key] ) ):
            to_return += "<td bgcolor='%s'>%s</td>" % ( codon_color[key][j], alignseq_cds[key][3 * j:3 * j + 3] ) 
        to_return += "</tr>" 
    to_return += "<tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr>"
    

                
    aa_color = {}
    codon_color = {}
    for j in range( 0, len( alignseq_aa[alignseq_aa.keys()[0]] ) ):
        tmp_aa = []
        for key in alignseq_aa.keys():
            if alignseq_aa[key][j] != '-':
                tmp_aa.append( alignseq_aa[key][j] )  
        tmp_aaa = set( tmp_aa )
        aa_count = []
        clr = ''
        for tp_aa in tmp_aaa:
            aa_count.append( tmp_aa.count( tp_aa ) )
        if aa_count != []:
            # print aa_count
            max_aa = list( tmp_aaa )[aa_count.index( max( aa_count ) )]
        for key in alignseq_aa.keys():
            if max_aa == alignseq_aa[key][j] or alignseq_aa[key][j] == '-':
                clr = ''
            else:
                clr = '#8A4117'
            if aa_color.has_key( key ):
                aa_color[key].append( clr )
            else:
                aa_color[key] = [clr]
    for key in alignseq_aa.keys():
        to_return += "<tr style='height:5px'><td>%s</td><td></td>" % key 
        for j in range( len( aa_color[key] ) ):
            if alignseq_aa[key][j] != 'X':
                to_return += "<td bgcolor='%s'>%s</td>" % ( aa_color[key][j], alignseq_aa[key][j] )
            else:
                to_return += "<td bgcolor='#E6A9EC'>*</td>" 
        to_return += "</tr>" 
    to_return += "</table></body></html>"
    to_return = filter( lambda x:x in string.printable, to_return )
    return to_return
    
# wwwcodon( "/home/devil/Downloads/NCU06882_fasta_nts.txt" )
def fasta_nucleotide_check( fl ):
    infile = open( fl )
    lines = infile.readlines()
    fasta_bool = 0
    if lines[0][0] == '>':
        fasta_bool = 1
    if fasta_bool == 1:
        dna_bool = nucleotide_check( lines[1:] )
    else:
        dna_bool = nucleotide_check( lines )
    return fasta_bool, dna_bool
def wwwcodon2( request ):
    if request.method == 'POST':
        form = File_Upload2( request.POST, request.FILES )
        if form.is_valid():
            infile = request.FILES['filename']
            fl = "%s/tmp/tmp.fa" % ( dbpth, count )
            seqfile = open( fl, "w" )
            seqfile.write( infile.read() )
            seqfile.close()
             # Change it to correct format
            #### save content
            
            to_return = wwwcodon( fl )  # send file to this function
            template = get_template( 'res.html' )
            return HttpResponse( template.render( RequestContext( request, {'result':to_return} ) ) )
        else:
            print "Form is not valid"
    else:
        template = get_template( 'codon2.html' )
        var = {}
        var = {
                'aln':File_Upload2()
              }
        return HttpResponse( template.render( RequestContext( request, var ) ) )

from django.db import models

#import sys
#sys.path.append('..')


STRAND = (('+','+'),('-','-'))
SEQTYPE = (('E','Exon'),('I','Intron'),('O','Other'))
EXOTYPE = (('C','CDS'),('5','5\'UTR'),('3','3\'UTR'))
DNA = (('A','A'),('C','C'),('G','G'),('T','T'))
RNA = (('A','A'),('C','C'),('G','G'),('I','I'),('U','U'))
CHROM = tuple([(str(j),'Chr'+str(j)) for j in range(1,23)]+[('X','ChrX'),('Y','ChrY')])
ASSEMBLY = ((18,'18'),(19,'19'))



class HSSnpValidation(models.Model):
    validation = models.CharField(max_length=32)
    def __unicode__(self):
        return self.validation

class HSGene(models.Model):
    geneid = models.IntegerField()
    gene = models.CharField(max_length=32)
    geneWiki = models.URLField(null=True, blank=True)
    def __unicode__(self):
        return self.gene

class HSSource(models.Model):
    source = models.CharField(max_length=200)
    def __unicode__(self):
        return self.source


class HSPubMed(models.Model):
    pubid = models.IntegerField()
    author = models.CharField(max_length=32)
    year = models.IntegerField()
    def __unicode__(self):
        return "%s %d"%(self.author, self.year)

class HSCoordinate(models.Model):
    assembly = models.IntegerField(choices=ASSEMBLY)
    chrom = models.CharField(choices=CHROM,max_length=2)
    coordinate = models.IntegerField()
    strand = models.CharField(choices=STRAND,max_length=1)
    indna = models.CharField(choices=DNA,max_length=1)
    inref = models.CharField(choices=DNA,max_length=1)
    inrna = models.CharField(choices=RNA,max_length=1)
    snp = models.CharField(max_length = 32, null = True, blank = True)
    snpunvalid = models.BooleanField(default=False)
    snpvalidation = models.ManyToManyField(HSSnpValidation,null=True,blank=True)
    seqtype = models.CharField(choices = SEQTYPE,max_length=1)
    exotype = models.CharField(choices = EXOTYPE,max_length=1,null=True,blank=True)
    gene = models.ForeignKey(HSGene, null=True, blank=True)
    alu = models.CharField(max_length=16,blank=True,null=True)
    source = models.ManyToManyField(HSSource, null=True, blank=True)
    pubid = models.ManyToManyField(HSPubMed)
    def __unicode__(self):
        return "%d %s %d"%(self.assembly,self.chrom, self.coordinate)

    

# Create your models here.

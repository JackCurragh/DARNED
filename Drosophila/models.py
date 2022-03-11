from django.db import models

#import sys
#sys.path.append('..')

ASSEMBLY = ((3,'3'),(3,'3'))
STRAND = (('+','+'),('-','-'))
SEQTYPE = (('E','Exon'),('I','Intron'),('O','Other'))
EXOTYPE = (('C','CDS'),('5','5\'UTR'),('3','3\'UTR'))
DNA = (('A','A'),('C','C'),('G','G'),('T','T'))
RNA = (('A','A'),('C','C'),('G','G'),('I','I'),('U','U'))
CHROM = (('2L','Chr2L'),
                ('2R','Chr2R'),
                ('3L','Chr3L'),
                ('3R','Chr3R'),
                ('4','Chr4'),
                ('X','ChrX'),
        )



class DMGene(models.Model):
    geneid = models.IntegerField()
    gene = models.CharField(max_length=32)
    def __unicode__(self):
        return self.gene


class DMPubMed(models.Model):
    pubid = models.IntegerField()
    author = models.CharField(max_length=32)
    year = models.IntegerField()
    def __unicode__(self):
        return "%s %d"%(self.author, self.year)

class DMCoordinate(models.Model):
    assembly = models.IntegerField(choices=ASSEMBLY)
    chrom = models.CharField('Chromosome',max_length=8, choices = CHROM)
    coordinate = models.IntegerField('Coordinate')
    strand = models.CharField('Strand',max_length=1,choices = STRAND)
    indna = models.CharField(choices=DNA,max_length=1)
    inref = models.CharField(choices=DNA,max_length=1)
    inrna = models.CharField(choices=RNA,max_length=1)
    gene = models.ForeignKey(DMGene,null=True,blank=True)
    seqtype = models.CharField("Seq Type",max_length=1, choices=SEQTYPE)
    exotype = models.CharField("Exo Type",max_length=1,choices=EXOTYPE, null=True, blank = True)
    alu = models.CharField("Alu",max_length=16,null = True, blank = True)
    pubid = models.ManyToManyField(DMPubMed)
    def __unicode__(self):
        return "%s_%d"%(self.chrom,self.coordinate)

    

# Create your models here.

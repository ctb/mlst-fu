#! /usr/bin/env python
import glob, screed

TEMPLATE="""#MEGA
!Title : %s;
!Format
   DataType=Nucleotide CodeTable=Standard
   NSeqs=%d NSites=%d
   Identical=. Missing=? Indel=-;


"""

largetags_files = glob.glob('*.fa.largetags')

genome_by_gene = {}

for filename in largetags_files:
    print '...', filename
    for record in screed.open(filename):
        genome, gene = record.name[1:].split('.')
        genome = genome.split('_')[0]

        x = genome_by_gene.get(gene, {})
        assert genome not in x
        x[genome] = record.sequence
        genome_by_gene[gene] = x

for gene in genome_by_gene:
    nseqs = 0
    total_seq = 0
    for genome in genome_by_gene[gene]:
        nseqs += 1
        total_seq += len(genome_by_gene[gene][genome])

    print gene, nseqs, total_seq

    fp = open('%s.largetags.mega' % gene, 'w')
    fp.write(TEMPLATE % (gene, nseqs, total_seq))

    for genome in genome_by_gene[gene]:
        fp.write("!Domain=%s property=Coding CodonStart=1;\n#%s %s\n" % (gene, genome, genome_by_gene[gene][genome]))

    fp.close()

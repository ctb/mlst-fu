#! /usr/bin/env python
import sys
sys.path.insert(0, '/u/t/dev/blastkit/lib')
import blastparser
import screed
from pygr.sequence import Sequence

seqsfile = sys.argv[1]
genome_name = seqsfile[:-3]
seqdb = screed.ScreedDB(seqsfile)

blastfile = 'large.x.' + genome_name
for record in blastparser.parse_fp(open(blastfile)):
    tagname = record.query_name ##
    for hit in record.hits:
        for match in hit:
            seq = Sequence(seqdb[hit.subject_name].sequence, tagname)
            start, end = match.subject_start, match.subject_end
            subseq = seq[start:end]

            print '>%s.%s\n%s' % (genome_name, tagname, subseq)
            break
        break

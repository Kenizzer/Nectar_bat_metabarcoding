import sys
from Bio import SeqIO
from numpy import median
from scipy import stats
import glob
import os

lengthsall=[]
path = '.'
for file in glob.glob( os.path.join(path, '*fasta') ): 
	handle = open(file, 'rU')
	lengths = map(lambda seq: len(seq.seq), SeqIO.parse(handle, 'fasta'))
	lengthsall= lengthsall + lengths
	print file
	print '# of seqs:', len(lengths)
	print 'MEAN:', sum(lengths)/float(len(lengths))
	print 'MEDIAN:', median(lengths)

#print lengthsall
print 'Totals'
print '# of seqs:', len(lengthsall)
print 'MEAN:', sum(lengthsall)/float(len(lengthsall))
print 'MEDIAN:', median(lengthsall)
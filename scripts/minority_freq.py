#!/usr/bin/env python3

import pysam 
import argparse
import numpy as np

'''
output: tab-separated file. Minority alleles on the rows and samples as columns
'''

class AlignedRead():

    def __init__(self, read):
        self.read = read

    def get_alignment_sequence(self):
        """
        Read sequenced bases, excluding soft-clipped bases and insertions
        but including deletions w.r.t reference sequence 
        """

        read = self.read
        alignment = ''
        idx = 0

        # cigartuples: cigar string encoded as a list of tuples (operation, length)
        for op, length in read.cigartuples:
            # Return read bases if they correspond to an alignment match (0), 
            # sequence match (7) or sequence mismatch (8)
            if op in [0, 7, 8]:
                alignment += read.query_sequence[idx:idx+length]
                idx += length
            # Add gap symbol '-' for deletions (2). Do not increment the index 
            # because deletions are not reported in read.query_sequence
            elif op == 2:
                alignment += ''.join(np.repeat('-', length))
            # skip read bases if they correspond to an insertion (1) or soft-
            # clipped bases (4)
            elif op in [1, 4]:
                idx += length

        return alignment

    def get_alignment_positions(self):
        
        return np.arange(self.read.reference_start, self.read.reference_end)


def parse_args():
    """ Set up the parsing of command-line arguments """
    parser = argparse.ArgumentParser(description="Script to extract minority alleles per samples")
    parser.add_argument("-r", required=True, metavar='ref', dest='ref', 
                        help="Fasta file containing the reference sequence")
    parser.add_argument("-s", "--start", required=False, default=None, metavar='locus', dest='start', 
                        help="Starting position of the region to be considered, 0-based indexing")
    parser.add_argument("-e", "--end", required=False, default=None, metavar='locus', dest='end',
                        help="Ending position of the region to be considered, 0-based indexing")
    parser.add_argument("-p", required=False, default=None, metavar='config_file', dest='frames',
                        help="Report minority aminoacids - a .config file specifying reading frames expected")
    parser.add_argument("-c", required=False, default=200000, metavar='coverage', dest='cov', 
                        help="Maximum read depth")
    parser.add_argument("-o", required=False, default="output.tsv", metavar='output_file', dest='outfile', 
                        help="Output file name") 
    parser.add_argument("FILES", nargs='+', metavar="bamfiles", help="BAM file(s)")
    
    return parser.parse_args()


def ascii2idx(bases, single=False):
    # character ascii index
    #    'A'      65    0
    #    'C'      67    1
    #    'G'      71    2
    #    'T'      84    3
    #    '-'      45    4
    charA   = ord('A') 
    charC   = ord('C')
    charG   = ord('G')
    charT   = ord('T')
    charDel = ord('-')
    sequence = np.zeros(bases.size, dtype=int)
    
    if single:
        base = bases
        if base is charA:
            return 0
        elif base is charC:
            return 1
        elif base is charG:
            return 2
        elif base is charT:
            return 3
        elif base is charDel:
            return 4  
    else:
        sequence[np.where(bases == charA)]   = 0
        sequence[np.where(bases == charC)]   = 1
        sequence[np.where(bases == charG)]   = 2
        sequence[np.where(bases == charT)]   = 3
        sequence[np.where(bases == charDel)] = 4
        return sequence
    
### MAIN
args = parse_args()

# Length of the reference sequence 
# Only one reference sequence expected 
reference = pysam.FastaFile(args.ref)
assert reference.nreferences == 1, 'Only one reference sequence expected'
region_len = reference.lengths[0]

if args.frames is None:
    # Nucleotides - Alphabet = {A, C, G, T, -}, including deletions
    alphabet = np.array(['A', 'C', 'G', 'T', '-'])
    alphabet_len = alphabet.size
else:
    alphabet = np.array(['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 
                         'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y'])
    alphabet_len = 20
 
num_samples = len(args.FILES)
#nt_freqs = np.zeros(shape=(region_len * alphabet_len, num_samples))
#coverage = np.zeros(shape=(region_len, num_samples), dtype=int)
if args.start is None:
    nt_counts = np.zeros(shape=(region_len * alphabet_len, num_samples))
else:
    region_length = args.end - args.start + 1
    nt_counts = np.zeros(shape=(region_len * alphabet_len))

for i, f in enumerate(args.FILES):

    with pysam.AlignmentFile(f, 'rb') as bamfile:

        if args.start is not None:
            # Processing a region in each bamfile
             for read in bamfile.fetch(args.reference, args.start, args.end):
                aligned_read = AlignedRead(read)
                alignment_sequence = np.array(aligned_read.get_alignment_sequence(), dtype='c').view(np.uint8)
                alignment_sequence = ascii2idx(alignment_sequence)
                alignment_positions = aligned_read.get_alignment_positions()
                # Filter bases that are not in the alphabet
                alignment_positions = np.delete(alignment_positions, np.where(alignment_sequence >= alphabet_len))
                alignment_sequence  = np.delete(alignment_sequence, np.where(alignment_sequence >= alphabet_len))
                nt_counts[alignment_positions * alphabet_len + alignment_sequence - args.start, i] += 1
        else: 
            # Processing every read in each bamfile
            for read in bamfile:
                aligned_read = AlignedRead(read)
                alignment_sequence = np.array(aligned_read.get_alignment_sequence(), dtype='c').view(np.uint8)
                alignment_sequence = ascii2idx(alignment_sequence)
                alignment_positions = aligned_read.get_alignment_positions()
                # Filter bases that are not in the alphabet
                alignment_positions = np.delete(alignment_positions, np.where(alignment_sequence >= alphabet_len))
                alignment_sequence  = np.delete(alignment_sequence, np.where(alignment_sequence >= alphabet_len)) 
                nt_counts[alignment_positions * alphabet_len + alignment_sequence, i] += 1            

        # Processing every position in the bamfile
        #for col in bamfile.pileup(reference="HXB2", start=3000, end=3010, truncate=True, max_depth=args.cov):
        #for col in bamfile.pileup(max_depth=args.cov):
        #    idx_col = col.reference_pos * alphabet_len
        #    counts = np.zeros(alphabet_len, dtype=int)

        #    for read in col.pileups:
        #        if not read.is_del and not read.is_refskip:
        #            # query position is None if is_del or is_refskip is set.
        #            base = ord(read.alignment.query_sequence[read.query_position])
        #        elif read.is_del:
        #            base = ord('-')
        #        
        #        idx = ascii2idx(base, single=True)
        #        counts[idx] += 1
        #    
        #    coverage[col.reference_pos, i] = np.sum(counts)
        #    nt_freqs[idx_col:(idx_col + alphabet_len), i] = counts / coverage[col.reference_pos, i]

coverage = np.zeros(shape=(region_len, num_samples), dtype=int)
nt_freqs = np.zeros(shape=(region_len * alphabet_len, num_samples))
for i in range(region_len):
    idx_locus = i * alphabet_len
    coverage[i, ] = np.sum(nt_counts[idx_locus:(idx_locus + alphabet_len), ], axis=0)
    # Identify position with zero coverage per sample
    mask = coverage[i, ] == 0
    nt_freqs[idx_locus:(idx_locus + alphabet_len), ~mask] = nt_counts[idx_locus:(idx_locus + alphabet_len), ~mask] / coverage[i, ~mask]

# Exclude locus for which any of the samples report counts
if args.start is None:
    loci = np.arange(region_len)
else:
    loci = np.arange(args.start, args.end)
loci = loci[np.sum(coverage, axis=1) > 0] 
variant_loci = np.zeros(shape=loci.size * alphabet_len).astype(bool)
minor_variants_freqs = np.zeros(shape=(variant_loci.size, num_samples)) 

for i, locus in enumerate(loci):
    
    # Bases counts for locus i and for all samples
    idx_locus = locus * alphabet_len
    nt_freqs_locus = nt_freqs[idx_locus:(idx_locus + alphabet_len), ]

    # Identify variants: bases reporting at least one count for one of the 
    # samples. Store 'True' if the sum of nucleotide frequencies across samples
    # is larger than 0.
    idx_locus = i * alphabet_len
    variant_loci[idx_locus:(idx_locus + alphabet_len)] = np.sum(nt_freqs_locus, axis=1) > 0
    minor_variants_freqs[idx_locus:(idx_locus + alphabet_len), ] = nt_freqs_locus
    
    # Identify samples from which current locus was not covered
    mask = coverage[locus, ] == 0
    
    # Identify the majority base per locus, and omit samples from which locus is not covered
    nt_freqs_locus = nt_freqs_locus[:, ~mask]
    idx_major = nt_freqs_locus.argmax(axis=0)
    if idx_major.size > 1:
        idx_major = np.bincount(idx_major).argmax()

    # Store 'False' for the majority variant
    variant_loci[idx_locus:(idx_locus + alphabet_len)][idx_major] = False
    

# Instatiate arrays 
minor_variants = np.tile(alphabet, loci.size)

# Exclude bases with zero counts for all samples, as well as majority bases
minor_variants = minor_variants[variant_loci] 
minor_variants_freqs = minor_variants_freqs[variant_loci, ]
loci = np.repeat(loci, alphabet_len)
loci = loci[variant_loci]

## Write to output file 
out = np.stack((loci, minor_variants))
out = np.concatenate((out.T, minor_variants_freqs), axis=1)

np.savetxt(args.outfile, out, fmt="%s", delimiter="\t", header="pos\tvariant")


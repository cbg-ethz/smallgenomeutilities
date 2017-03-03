#!/usr/bin/env python3

import pysam 
import argparse
import numpy as np

'''
input:  alignment file(s) as bam file(s) and reference sequence
output: tab-separated file. Minority alleles on the rows and samples as columns.
        Loci are reported using 0-based indexing.
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
    parser.add_argument("-r", required=True, metavar='FASTA', dest='reference', 
                        help="Either a fasta file containing the reference sequence or the reference name of the region/chromosome of interest")
    parser.add_argument("-s", "--start", required=False, default=None, metavar='INT', dest='start',
                        type=int, help="Starting position of the region of interest, 0-based indexing")
    parser.add_argument("-e", "--end", required=False, default=None, metavar='INT', dest='end',
                        type=int, help="Ending position of the region of interest, 0-based indexing")
    parser.add_argument("-p", required=False, default=None, metavar='file.config', dest='frames',
                        help="Report minority aminoacids - a .config file specifying reading frames expected")
    parser.add_argument("-c", required=False, default=200000, metavar='INT', dest='cov', 
                        help="Maximum read depth")
    parser.add_argument("-o", required=False, default="output.tsv", metavar='output.tsv', dest='outfile', 
                        help="Output file name") 
    parser.add_argument("FILES", nargs='+', metavar="bamfiles", help="BAM file(s)")
    
    return parser.parse_args()


def ascii2idx(sequence):
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

    sequence[sequence == charA]   = 0
    sequence[sequence == charC]   = 1
    sequence[sequence == charG]   = 2
    sequence[sequence == charT]   = 3
    sequence[sequence == charDel] = 4
    return sequence
    
def main():
    args = parse_args()
    
    if args.start is not None:
        assert args.end is not None, 'Minority variants are extracted from a region of interest. An ending position was expected'
    
    if args.end is not None:
        print('Starting position was expected. Setting it to 0')
        args.start = 0
    
    if args.frames is None:
        # Nucleotides - Alphabet = {A, C, G, T, -}, including deletions
        alphabet = np.array(['A', 'C', 'G', 'T', '-'])
        alphabet_len = alphabet.size
    else:
        alphabet = np.array(['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 
                             'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y'])
        alphabet_len = 20
        print("Option not implemented yet")
        raise SystemExit(0)
     
    num_samples = len(args.FILES)
    
    if args.start is None and args.end is None:
        # Length of the reference sequence 
        # Only one reference sequence expected 
        reference = pysam.FastaFile(args.reference)
        assert reference.nreferences == 1, 'Only one reference sequence expected'
        region_len = reference.lengths[0]
        reference_name = reference.references[0]
    
        nt_counts = np.zeros(shape=(region_len * alphabet_len, num_samples))
    
    else:
        region_len = args.end - args.start + 1
        reference_name = args.reference
    
        nt_counts = np.zeros(shape=(region_len * alphabet_len, num_samples))
    
    
    for i, f in enumerate(args.FILES):
    
        with pysam.AlignmentFile(f, 'rb') as bamfile:
    
            for read in bamfile.fetch(reference=reference_name, start=args.start, end=args.end):
                # Fetch returns all reads which cover an specific region. However,
                # all positions - including positions outside the region of interest - 
                # are returned
                aligned_read = AlignedRead(read)
                alignment_positions = aligned_read.get_alignment_positions()
                alignment_sequence = np.array(aligned_read.get_alignment_sequence(), dtype='c').view(np.uint8)
    
                if args.start is not None and args.end is not None:
                    # Extract region of interest
                    idxs = (alignment_positions >= args.start) & (alignment_positions <= args.end)
                    alignment_positions = alignment_positions[idxs]
                    alignment_sequence  = alignment_sequence[idxs]
    
                alignment_sequence = ascii2idx(alignment_sequence)
    
                # Filter bases that are not in the alphabet
                if (alignment_sequence >= alphabet_len).any():
                    idxs = np.where(alignment_sequence >= alphabet_len)
                    alignment_positions = np.delete(alignment_positions, idxs)
                    alignment_sequence  = np.delete(alignment_sequence, idxs)
    
                if args.start is None and args.end is None:
                    idxs_array = alignment_positions * alphabet_len + alignment_sequence
                else:
                    # Shift the indexing
                    idxs_array = (alignment_positions * alphabet_len) + alignment_sequence - (args.start * alphabet_len)
    
                nt_counts[idxs_array, i] += 1          
    
    
    coverage = np.zeros(shape=(region_len, num_samples), dtype=int)
    nt_freqs = np.zeros(shape=(region_len * alphabet_len, num_samples))
    for i in range(region_len):
        idx_locus = i * alphabet_len
        coverage[i, ] = np.sum(nt_counts[idx_locus:(idx_locus + alphabet_len), ], axis=0)
        # Identify samples with zero coverage for a given locus (needed for 
        # avoiding division by zero)
        mask = coverage[i, ] == 0
        nt_freqs[idx_locus:(idx_locus + alphabet_len), ~mask] = nt_counts[idx_locus:(idx_locus + alphabet_len), ~mask] / coverage[i, ~mask]
    
    
    if args.start is None and args.end is None:
        loci = np.arange(region_len)
    else:
        loci = np.arange(args.start, args.end+1)
    
    # Exclude loci for which any of the samples report zero counts
    loci = loci[np.sum(coverage, axis=1) > 0] 
    variant_loci = np.zeros(shape=loci.size * alphabet_len).astype(bool)
    minor_variants_freqs = np.zeros(shape=(variant_loci.size, num_samples)) 
    
    for i, locus in enumerate(loci):
        
        if args.start is not None:
            locus = locus - args.start
        
        # Counts per bases for locus i and for all samples
        idx_locus = locus * alphabet_len
        nt_freqs_locus = nt_freqs[idx_locus:(idx_locus + alphabet_len), ]
    
        # Identify variants: bases reporting at least one count for one of the 
        # samples. Store 'True' if the sum of nucleotide frequencies across samples 
        # is larger than 0.
        idx_array = i * alphabet_len
        variant_loci[idx_array:(idx_array + alphabet_len)] = np.sum(nt_freqs_locus, axis=1) > 0
        minor_variants_freqs[idx_array:(idx_array + alphabet_len), ] = nt_freqs_locus
        
        # Identify samples from which current locus was not covered
        mask = coverage[locus, ] == 0
        
        # Identify the majority base per locus, and omit samples from which locus is not covered
        nt_freqs_locus = nt_freqs_locus[:, ~mask]
        idx_major = nt_freqs_locus.argmax(axis=0)
        if idx_major.size > 1:
            idx_major = np.bincount(idx_major).argmax()
    
        # Store 'False' for the majority variant
        variant_loci[idx_array:(idx_array + alphabet_len)][idx_major] = False
        
    
    # Instantiate arrays
    minor_variants = np.tile(alphabet, loci.size)
    loci = np.repeat(loci, alphabet_len)
    
    # Exclude bases with zero counts for all samples, as well as majority bases
    minor_variants = minor_variants[variant_loci] 
    minor_variants_freqs = minor_variants_freqs[variant_loci, ]
    loci = loci[variant_loci]
    
    ## Write to output file 
    out = np.stack((loci, minor_variants))
    out = np.concatenate((out.T, minor_variants_freqs), axis=1)
    
    np.savetxt(args.outfile, out, fmt="%s", delimiter="\t", header="pos\tvariant")

if __name__ == '__main__':
    main()


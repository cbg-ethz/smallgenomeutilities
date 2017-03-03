# SmallGenomeUtilities
The SmallGenomeUtilities are a collection of scripts that is useful for dealing and manipulating NGS data of small viral genomes. They are written in Python 3 with a minimal number of dependencies.

## Dependencies
- biopython
- progress
- pysam

## Description of utilities
### convert_qr
Convert QuasiRecomb output of a transmitter and recipient set of haplotypes to a combined set of haplotypes, where gaps have been filtered. Optionally translate to peptide sequence.

### convert_reference
Perform a genomic liftover. Transform an alignment in SAM or BAM format from one reference sequence to another. Can replace `M` states by `=`/`X`

### coverage_stats
Calculate average coverage for a target region of an alignment.

### extract_sam
Extract subsequences of an alignment, with the option of converting it to peptide sequences. Can filter on the basis of subsequence frequency or gap frequencies in subsequences.

### extract_seq
Extract sequences of alignments into a FASTA file where the sequence id matches a given string.

### mapper
Determine the genomic offsets on a target contig, given an initial contig and offsets. Can be used to map between reference genomes.

### pair_sequences
Compare sequences from a multiple sequence alignment from transmitter and recipient samples in order to determine the optimal matching of transmitters to recipients.

### remove_gaps_msa
Given a multiple sequence alignment, remove loci with a gap fraction above a certain threshold.

### minority_freq
Extract frequencies of minority variants from multiple samples. A region of interest is also supported

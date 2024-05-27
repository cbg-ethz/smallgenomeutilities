#!/usr/bin/env python3

import os
import pysam
import numpy as np


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

        # cigartuples: cigar string encoded as a list of tuples (operation,
        # length)
        for op, length in read.cigartuples:
            # Return read bases if they correspond to an alignment match (0),
            # sequence match (7) or sequence mismatch (8)
            if op in [0, 7, 8]:
                alignment += read.query_sequence[idx:idx + length]
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


def ascii2idx(sequence):
    # character ascii index
    #    'A'      65    0
    #    'C'      67    1
    #    'G'      71    2
    #    'T'      84    3
    #    '-'      45    4
    charA = ord('A')
    charC = ord('C')
    charG = ord('G')
    charT = ord('T')
    charDel = ord('-')

    sequence[sequence == charA] = 0
    sequence[sequence == charC] = 1
    sequence[sequence == charG] = 2
    sequence[sequence == charT] = 3
    sequence[sequence == charDel] = 4
    return sequence


def get_aln_counts(args):

    alnfile, reference_name, start, end, region_len, alphabet_len = args

    nt_counts = np.zeros(shape=(region_len * alphabet_len))

    for read in alnfile.fetch(reference=reference_name, start=start, end=end):
        # Fetch returns all reads which cover an specific region. However,
        # all positions - including positions outside the region of interest -
        # are returned
        aligned_read = AlignedRead(read)
        alignment_positions = aligned_read.get_alignment_positions()
        alignment_sequence = np.array(
            aligned_read.get_alignment_sequence(), dtype='c').view(np.uint8)

        if start is not None and end is not None:
            # Extract region of interest
            idxs = (alignment_positions >= start) & (
                alignment_positions <= end)
            alignment_positions = alignment_positions[idxs]
            alignment_sequence = alignment_sequence[idxs]

        alignment_sequence = ascii2idx(alignment_sequence)

        # Filter bases that are not in the alphabet
        if (alignment_sequence >= alphabet_len).any():
            idxs = np.where(alignment_sequence >= alphabet_len)
            alignment_positions = np.delete(alignment_positions, idxs)
            alignment_sequence = np.delete(alignment_sequence, idxs)

        if start is None and end is None:
            idxs_array = alignment_positions * alphabet_len + alignment_sequence
        else:
            # Shift the indexing
            idxs_array = (alignment_positions * alphabet_len) + \
                alignment_sequence - (start * alphabet_len)

        nt_counts[idxs_array] += 1

    return nt_counts


def get_counts(args):

    bamfile = args[0]

    with pysam.AlignmentFile(bamfile, 'rc' if os.path.splitext(bamfile)[1] == '.cram' else 'rb') as alnfile:

        return get_aln_counts([alnfile] + list(args[1:]))


def get_cnt_matrix (alnfile, reference_name, alpha='ACGT-'):
    """
    returns:
     - 2D array with counts per positions in rows and per alphabet in columns
       for all reads in reference_name
        >  match[i,j] = (sequence[i] ?= alphabet[j])
        >  counts[position+i,j] += 1 if match[i,j]
     - readcounts
     - total template_length    ( = insert_size * reads )
     - total read bases         ( = read_len    * reads )
    """
    #tid=alnfile.get_tid(reference_name)
    region_len=alnfile.get_reference_length(reference_name)

    nt_alpha=np.array(alpha, dtype='c').view(np.uint8)
    alphabet_len=nt_alpha.shape[0] #=len(alpha)

    nt_counts = np.zeros(shape=(region_len, alphabet_len),dtype=np.uint32)
    reads=0
    insert_tot=0
    rlen_tot=0
    for read in alnfile.fetch(reference=reference_name):
        reads+=1
        insert_tot+=abs(read.template_length)
        # NOTE no real lenght (happens with primers dimers, once primers are trimmed, remaining lenght can be 0 or 1)
        if read.reference_end == read.reference_start:
            # dimers, etc.
            continue
        rlen_tot+=read.reference_end-read.reference_start
        if read.query_sequence is None:
            print(f"Warning: skipping read without sequence {reads}: {read.query_name}")
            continue
        aligned_read = AlignedRead(read)
        #alignment_positions = aligned_read.get_alignment_positions()
        alignment_sequence = np.array(
            aligned_read.get_alignment_sequence(), dtype='c').view(np.uint8)
        if alignment_sequence.size < 1:
            # dimers, etc.
            continue

        #nt_counts[alignment_positions,:] += np.equal.outer(alignment_sequence, nt_alpha)
        try:
            nt_counts[read.reference_start:read.reference_end,:] += np.equal.outer(alignment_sequence, nt_alpha)
        except ValueError:
            print(f"""
Cannot sum read to the count matrix
read number:\t{reads}
template len:\t{read.template_length}
ref start:\t{read.reference_start}
ref ends: \t{read.reference_end}""")
            print(alignment_sequence)
            print(np.equal.outer(alignment_sequence, nt_alpha))

    return nt_counts, reads, insert_tot, rlen_tot

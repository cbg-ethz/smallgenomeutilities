#!/usr/bin/env python3

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


def get_counts(args):

    bamfile, reference_name, start, end, region_len, alphabet_len = args

    nt_counts = np.zeros(shape=(region_len * alphabet_len))

    with pysam.AlignmentFile(bamfile, 'rb') as alnfile:

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

#!/usr/bin/env python3

from collections import namedtuple

import sys
import Bio.SeqIO

gRange = namedtuple("gRange", "start stop")


def convert_from_list_to_intervals(loci):
    valid_loci = sorted(set(loci))

    # add sentinel
    valid_loci.append(max(valid_loci) + 2)

    start_locus = valid_loci[0]

    result = []

    for i in range(1, len(valid_loci)):
        if valid_loci[i] > valid_loci[i - 1] + 1:
            # discontinuity, got one range
            result.append(gRange(start=start_locus,
                                 stop=valid_loci[i - 1] + 1))
            start_locus = valid_loci[i]

    return result


def convert_from_intervals_to_list(intervals):
    result = []

    for i in intervals:
        if len(i) == 1:
            # just one index
            result.append(int(i[0]))

        elif len(i) == 2:
            # a start and end index
            begin = int(i[0])
            end = int(i[1])

            if (begin < end):
                for k in range(begin, end):
                    result.append(k)
            else:
                print("'{}' represents an empty interval".format(i))
                sys.exit(1)

        else:
            # too many indices
            print("'{}' is not a proper interval".format(i))
            sys.exit(1)

    return sorted(set(result))


def find_interval_on_dest(source, dest, list_loci, offset, msa_file, verbose):
    temp_loci = list_loci.split(',')
    split_loci = []
    for i in temp_loci:
        split_loci.append(i.split('-'))

    source_intervals = convert_from_list_to_intervals(
        convert_from_intervals_to_list(split_loci))

    # Load genomes from MSA FASTA file
    genomes = {}
    for record in Bio.SeqIO.parse(msa_file, "fasta"):
        record.id = record.id.split('_', 1)[0]
        record.seq = record.seq.upper()
        genomes[record.id] = record

    # check if source contig exists in MSA
    if not source in genomes:
        print("Could not find contig '{}' in {}".format(source, msa_file))
        sys.exit(0)

    # check if destination contig exists in MSA
    if not dest in genomes:
        print("Could not find contig '{}' in {}".format(dest, msa_file))
        sys.exit(0)

    # Start parsing MSA
    source_seq = genomes[source].seq
    dest_seq = genomes[dest].seq

    if not len(source_seq) == len(dest_seq):
        print("Contigs of '{}' and '{}' are not equal in length, cannot be an MSA!".format(
            source, dest))
        sys.exit(0)

    # create SAM POS -> FASTA POS dictionary
    # for DEST contig
    sam_to_fasta_map = {}
    pos_in_sam = 0
    for i in range(0, len(dest_seq)):
        if dest_seq[i] != '-':
            sam_to_fasta_map[pos_in_sam] = i
            pos_in_sam += 1

    # create FASTA POS -> SAM POS dictionary
    # for SOURCE contig
    fasta_to_sam_map = {}
    pos_in_sam = 0
    for i in range(0, len(source_seq)):
        if source_seq[i] != '-':
            fasta_to_sam_map[i] = pos_in_sam
            pos_in_sam += 1

    # find intervals
    result = []

    for l in source_intervals:
        dest_fasta_start = sam_to_fasta_map[l.start]

        while not dest_fasta_start in fasta_to_sam_map:
            dest_fasta_start += 1
        src_sam_start = fasta_to_sam_map[dest_fasta_start]

        dest_fasta_stop = sam_to_fasta_map[l.stop - 1]
        while not dest_fasta_stop in fasta_to_sam_map:
            dest_fasta_stop -= 1
        src_sam_stop = fasta_to_sam_map[dest_fasta_stop] + 1

        if src_sam_stop > src_sam_start:
            result.append(gRange(start=src_sam_start, stop=src_sam_stop))

    # simplify list and return
    return convert_from_list_to_intervals(convert_from_intervals_to_list(result))

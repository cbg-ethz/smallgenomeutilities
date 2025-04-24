####################
smallgenomeutilities
####################


.. image:: https://img.shields.io/conda/dn/bioconda/smallgenomeutilities.svg?label=Bioconda
   :alt: Bioconda package
   :target: https://bioconda.github.io/recipes/smallgenomeutilities/README.html
.. image:: https://quay.io/repository/biocontainers/smallgenomeutilities/status
   :alt: Docker container
   :target: https://quay.io/repository/biocontainers/smallgenomeutilities
.. image:: https://github.com/cbg-ethz/smallgenomeutilities/actions/workflows/main.yaml/badge.svg
   :alt: Tests
   :target: https://github.com/cbg-ethz/smallgenomeutilities/actions/workflows/main.yaml

The smallgenomeutilities are a collection of scripts that is useful for dealing and manipulating NGS data of small viral genomes. They are written in Python 3 with a small number of dependencies.

The smallgenomeutilities are part of the `V-pipe workflow for analysing NGS data of short viral genomes <https://github.com/cbg-ethz/V-pipe>`_.


************
Dependencies
************

You can install these python modules either using pip or `bioconda <https://bioconda.github.io/>`_:

- biopython
- bcbio-gff
- numpy
- pandas
- progress
- pysam
- pysamstats
- sklearn
- matplotlib
- progress
- pyyaml
- more_itertools

In addition to the modules, frameshift_deletions_checks currently requires `mafft <https://mafft.cbrc.jp/alignment/software/>`_ being installed -- it is also `available on bioconda <https://bioconda.github.io/recipes/mafft/README.html>`_.


************
Installation
************

The recommended way to install the smallgenomeutilities is using the `bioconda package <https://bioconda.github.io/recipes/smallgenomeutilities/README.html>`_:

.. code-block:: bash

   mamba install smallgenomeutilities


Another possibility is using pip:

.. code-block:: bash

   # install from the current directory
   pip install --editable .

   # install from GitHub
   pip install git+https://github.com/cbg-ethz/smallgenomeutilities.git

   # install from Pypi
   pip install smallgenomeutilities


************************
Description of utilities
************************

aln2basecnt
-----------
extract base counts and coverage information from a single alignment file

compute_mds
-----------
Compute multidimensional scaling for visualizing distances among reconstructed haplotypes.

convert_qr
----------
Convert QuasiRecomb output of a transmitter and recipient set of haplotypes to a combined set of haplotypes, where gaps have been filtered. Optionally translate to peptide sequence.

convert_reference
-----------------
Perform a genomic liftover. Transform an alignment in SAM or BAM format from one reference sequence to another. Can replace `M` states by `=`/`X`.

coverage
--------
Calculate average coverage for a target region on a different contig.

coverage_depth_qc
-----------------
Computes 'fraction of genome covered a depth' QC metrics from coverage TSV files (made by aln2basecnt, samtools depth, etc.)

coverage_stats
--------------
Calculate average coverage for a target region of an alignment.

extract_consensus
-----------------
Build consensus sequences including either the majority base or the ambiguous bases from an alignment (BAM) file.

extract_coverage_intervals
--------------------------
Extract regions with sufficient coverage for running ShoRAH. Half-open intervals are returned, [start:end), and 0-based indexing is used.

extract_sam
-----------
Extract subsequences of an alignment, with the option of converting it to peptide sequences. Can filter on the basis of subsequence frequency or gap frequencies in subsequences.

extract_seq
-----------
Extract sequences of alignments into a FASTA file where the sequence id matches a given string.

frameshift_deletions_checks
---------------------------

.. image:: https://img.shields.io/badge/usegalaxy-.eu-brightgreen?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAASCAYAAABB7B6eAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAACXBIWXMAAAsTAAALEwEAmpwYAAACC2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx0aWZmOlJlc29sdXRpb25Vbml0PjI8L3RpZmY6UmVzb2x1dGlvblVuaXQ+CiAgICAgICAgIDx0aWZmOkNvbXByZXNzaW9uPjE8L3RpZmY6Q29tcHJlc3Npb24+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgICAgIDx0aWZmOlBob3RvbWV0cmljSW50ZXJwcmV0YXRpb24+MjwvdGlmZjpQaG90b21ldHJpY0ludGVycHJldGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KD0UqkwAAAn9JREFUOBGlVEuLE0EQruqZiftwDz4QYT1IYM8eFkHFw/4HYX+GB3/B4l/YP+CP8OBNTwpCwFMQXAQPKtnsg5nJZpKdni6/6kzHvAYDFtRUT71f3UwAEbkLch9ogQxcBwRKMfAnM1/CBwgrbxkgPAYqlBOy1jfovlaPsEiWPROZmqmZKKzOYCJb/AbdYLso9/9B6GppBRqCrjSYYaquZq20EUKAzVpjo1FzWRDVrNay6C/HDxT92wXrAVCH3ASqq5VqEtv1WZ13Mdwf8LFyyKECNbgHHAObWhScf4Wnj9CbQpPzWYU3UFoX3qkhlG8AY2BTQt5/EA7qaEPQsgGLWied0A8VKrHAsCC1eJ6EFoUd1v6GoPOaRAtDPViUr/wPzkIFV9AaAZGtYB568VyJfijV+ZBzlVZJ3W7XHB2RESGe4opXIGzRTdjcAupOK09RA6kzr1NTrTj7V1ugM4VgPGWEw+e39CxO6JUw5XhhKihmaDacU2GiR0Ohcc4cZ+Kq3AjlEnEeRSazLs6/9b/kh4eTC+hngE3QQD7Yyclxsrf3cpxsPXn+cFdenF9aqlBXMXaDiEyfyfawBz2RqC/O9WF1ysacOpytlUSoqNrtfbS642+4D4CS9V3xb4u8P/ACI4O810efRu6KsC0QnjHJGaq4IOGUjWTo/YDZDB3xSIxcGyNlWcTucb4T3in/3IaueNrZyX0lGOrWndstOr+w21UlVFokILjJLFhPukbVY8OmwNQ3nZgNJNmKDccusSb4UIe+gtkI+9/bSLJDjqn763f5CQ5TLApmICkqwR0QnUPKZFIUnoozWcQuRbC0Km02knj0tPYx63furGs3x/iPnz83zJDVNtdP3QAAAABJRU5ErkJggg==
   :alt: European Galaxy server
   :align: right
   :target: https://usegalaxy.eu/root?tool_id=smgu_frameshift_deletions_checks

Produce a report about frameshifting indels in a consensus sequences

gather_coverage
---------------
gather multiple per sample coverage information into a single unified file

mapper
------
Determine the genomic offsets on a target contig, given an initial contig and offsets. Can be used to map between reference genomes.

min_coverage
------------
find the minimum coverage in a region from an alignment

minority_freq
-------------
Extract frequencies of minority variants from multiple samples. A region of interest is also supported.

pair_sequences
--------------
Compare sequences from a multiple sequence alignment from transmitter and recipient samples in order to determine the optimal matching of transmitters to recipients.

paired_end_read_merger
----------------------
Merge paired-end reads to one merged read based on alignment.

predict_num_reads
-----------------
Predict number of reads after quality preprocessing.

prepare_primers
---------------
Starting with a primers BED file, generate the other files used by V-pipe (inserts BED file, and TSV and FASTA file of primers sequences)

remove_gaps_msa
---------------
Given a multiple sequence alignment, remove loci with a gap fraction above a certain threshold.


************************
Using the utilities
************************

After installation, all utilities are available as command-line programs. You can run any utility by simply typing its name in your terminal, followed by any required arguments:

.. code-block:: bash

   # Get help for any utility
   aln2basecnt --help
   
   # Example usage of paired_end_read_merger
   paired_end_read_merger input.sam -f reference.fasta -o output_fused.sam 

Each utility supports the ``--help`` flag which provides detailed information about its usage, required arguments, and available options.

*************
Citation
*************

If you use the ``paired_end_read_merger`` or the ``frameshift_deletions_checks``, please cite

Fuhrmann, L., Jablonski, K. P., Topolsky, I., Batavia, A. A., Borgsmueller, N., Icer Baykal, P., ... & Beerenwinkel, N. (2023). "V-pipe 3.0: a sustainable pipeline for within-sample viral genetic diversity estimation." , https://doi.org/10.1101/2023.10.16.562462

For all other scripts, please cite

Posada-Céspedes S., Seifert D., Topolsky I., Jablonski K.P., Metzner K.J., and Beerenwinkel N. 2021.
"V-pipe: a computational pipeline for assessing viral genetic diversity from high-throughput sequencing data."
*Bioinformatics*, January. https://doi.org/10.1093/bioinformatics/btab015

*************
Contributions
*************

- David Seifert	|orcdseif|_	|gitdseif|_
- Susana Posada Cespedes	|orcsposa|_	|gitsposa|_
- Ivan Blagoev Topolsky	|orcitopo|_	|gititopo|_
- Lara Fuhrmann	|orclfuhr|_	|gitlfuhr|_
- Mateo Carrara	|orcmcarr|_	|gitmcarr|_
- Michal Okoniewski	|orcmokn|_	|gitmokn|_
- Gordon J. Köhn	|orcgkoe|_	|gitgkoe|_

.. _orcdseif : https://orcid.org/0000-0003-4739-5110
.. _gitdseif : https://github.com/SoapZA
.. _orcsposa : https://orcid.org/0000-0002-7459-8186
.. _gitsposa : https://github.com/sposadac
.. _orcitopo : https://orcid.org/0000-0002-7561-0810
.. _gititopo : https://github.com/dryak
.. _orclfuhr : https://orcid.org/0000-0001-6405-0654
.. _gitlfuhr : https://github.com/LaraFuhrmann
.. _orcmcarr : https://orcid.org/0000-0002-8559-8296
.. _gitmcarr : https://github.com/mcarrara-bioinfo
.. _orcmokn : https://orcid.org/0000-0003-4722-4506
.. _gitmokn : https://github.com/michalogit
.. _orcgkoe : https://orcid.org/0000-0003-3397-7769
.. _gitgkoe : https://github.com/gordonkoehn

.. |orcdseif| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-ORICID.svg
.. |orcsposa| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-ORICID.svg
.. |orcitopo| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-ORICID.svg
.. |orclfuhr| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-ORICID.svg
.. |orcmcarr| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-ORICID.svg
.. |orcmokn| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-ORICID.svg
.. |orcgkoe| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-ORICID.svg

.. |gitdseif| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-github.svg
.. |gitsposa| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-github.svg
.. |gititopo| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-github.svg
.. |gitlfuhr| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-github.svg
.. |gitmcarr| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-github.svg
.. |gitmokn| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-github.svg
.. |gitgkoe| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-github.svg

.. |github| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-github.svg
.. |orcid| image:: https://cbg-ethz.github.io/V-pipe/assets/img/icon-ORICID.svg

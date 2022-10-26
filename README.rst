####################
smallgenomeutilities
####################


.. image:: https://img.shields.io/conda/dn/bioconda/smallgenomeutilities.svg?label=Bioconda
   :alt: Bioconda package
   :target: https://bioconda.github.io/recipes/smallgenomeutilities/README.html
.. image:: https://quay.io/repository/biocontainers/smallgenomeutilities/status
   :alt: Docker container
   :target: https://quay.io/repository/biocontainers/smallgenomeutilities


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
- yaml

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

predict_num_reads
-----------------
Predict number of reads after quality preprocessing. 

remove_gaps_msa
---------------
Given a multiple sequence alignment, remove loci with a gap fraction above a certain threshold.


*************
Contributions
*************

- David Seifert	<david.seifert@bsse.ethz.ch>	|orcdseif|_	|gitdseif|_
- Susana Posada Cespedes	<susana.posada@bsse.ethz.ch>	|orcsposa|_	|gitsposa|_
- Ivan Blagoev Topolsky	<ivan.topolsky@sib.swiss>	|orcitopo|_	|gititopo|_
- Lara Fuhrmann	<lara.fuhrmann@bsse.ethz.ch>	|orclfuhr|_	|gitlfuhr|_
- Mateo Carrara	<carrara@nexus.ethz.ch>	|orcmcarr|_	|gitmcarr|_

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

.. |orcdseif| image:: https://cbg-ethz.github.io/V-pipe/img/ORCIDiD_iconvector.svg 
.. |orcsposa| image:: https://cbg-ethz.github.io/V-pipe/img/ORCIDiD_iconvector.svg 
.. |orcitopo| image:: https://cbg-ethz.github.io/V-pipe/img/ORCIDiD_iconvector.svg 
.. |orclfuhr| image:: https://cbg-ethz.github.io/V-pipe/img/ORCIDiD_iconvector.svg 
.. |orcmcarr| image:: https://cbg-ethz.github.io/V-pipe/img/ORCIDiD_iconvector.svg 

.. |gitdseif| image:: https://cbg-ethz.github.io/V-pipe/img/mark-github.svg
.. |gitsposa| image:: https://cbg-ethz.github.io/V-pipe/img/mark-github.svg
.. |gititopo| image:: https://cbg-ethz.github.io/V-pipe/img/mark-github.svg
.. |gitlfuhr| image:: https://cbg-ethz.github.io/V-pipe/img/mark-github.svg
.. |gitmcarr| image:: https://cbg-ethz.github.io/V-pipe/img/mark-github.svg

.. |github| image:: https://cbg-ethz.github.io/V-pipe/img/mark-github.svg
.. |orcid| image:: https://cbg-ethz.github.io/V-pipe/img/ORCIDiD_iconvector.svg

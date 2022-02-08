from sys import version_info, exit
from os import path
from setuptools import setup

# Will never support Py2
if version_info[0] == 2:
    exit("Sorry, Python 2 is not supported")


# Get the long description from the README file lazily
def readme():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, "README.rst"), encoding='utf-8') as f:
        return f.read()

setup(
    name="smallgenomeutilities",
    version="0.3.6",
    author="David Seifert, Susana Posada Cespedes, Ivan Topolsky, Lara Fuhrmann",
    author_email="david.seifert@bsse.ethz.ch, susana.posada@bsse.ethz.ch, ivan.topolsky@bsse.ethz.ch, lara.fuhrmann@bsse.ethz.ch",
    description=(
        "A collection of scripts that are useful for dealing with viral RNA NGS data."),
    license="GPL2+",
    keywords="NGS SAM BAM CRAM HIV-1 SARS-CoV-2 alignment",
    url="https://github.com/cbg-ethz/smallgenomeutilities",
    packages=["smallgenomeutilities"],
    scripts=[
        "scripts/aln2basecnt",
        "scripts/compute_mds",
        "scripts/convert_qr",
        "scripts/convert_reference",
        "scripts/coverage",
        "scripts/coverage_stats",
        "scripts/extract_consensus",
        "scripts/extract_coverage_intervals",
        "scripts/extract_sam",
        "scripts/extract_seq",
        "scripts/frameshift_deletions_checks",
        "scripts/gather_coverage",
        "scripts/mapper",
        "scripts/min_coverage",
        "scripts/minority_freq",
        "scripts/pair_sequences",
        "scripts/predict_num_reads",
        "scripts/remove_gaps_msa",
    ],
    install_requires=[
        "biopython",
        "bcbio-gff",
        "pysam",
        "pysamstats",
        "pandas",
        "numpy",
        "scipy",
        "scikit-learn",
        "matplotlib",
        "progress",
        "yaml",
    ],
    include_package_data=True,
    long_description=readme(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)

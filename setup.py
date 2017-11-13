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
    version="0.2.1",
    author="David Seifert, Susana Posada Cespedes",
    author_email="david.seifert@bsse.ethz.ch, susana.posada@bsse.ethz.ch",
    description=(
        "A collection of scripts that are useful for dealing with viral RNA NGS data."),
    license="GPL2+",
    keywords="NGS SAM BAM HIV-1 alignment",
    url="https://github.com/cbg-ethz/smallgenomeutilities",
    packages=["smallgenomeutilities"],
    scripts=[
        "scripts/compute_mds",
        "scripts/convert_qr",
        "scripts/convert_reference",
        "scripts/coverage",
        "scripts/coverage_stats",
        "scripts/extract_coverage_intervals",
        "scripts/extract_sam",
        "scripts/extract_seq",
        "scripts/mapper",
        "scripts/min_coverage",
        "scripts/minority_freq",
        "scripts/pair_sequences",
        "scripts/predict_num_reads",
        "scripts/remove_gaps_msa",
    ],
    install_requires=[
        "biopython",
        "numpy",
        "progress",
        "pysam",
        "scikit-learn",
        "scipy",
        "matplotlib",
    ],
    include_package_data=True,
    long_description=readme(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)

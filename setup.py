from os import path
from setuptools import setup

# Utility function to read the README file.
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README"), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name = "SmallGenomeUtilities",
	version = "0.0.1",
	author = "David Seifert",
	author_email = "david.seifert@bsse.ethz.ch",
	description = ("A collection of scripts that are useful for dealing with viral RNA NGS data."),
	license = "GPL2+",
	keywords = "NGS SAM BAM HIV-1 alignment",
	url = "https://github.com/SoapZA/SmallGenomeUtilities",
	packages=["SmallGenomeUtilities"],
	scripts=[
		"scripts/convert_qr",
		"scripts/convert_reference",
		"scripts/extract_sam",
		"scripts/mapper"],
	install_requires=[
		"biopython",
		"progress",
		"pysam"],
	long_description=long_description,
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Topic :: Scientific/Engineering :: Bio-Informatics",
		"Topic :: Utilities",
		"License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
	],
)

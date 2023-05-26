# Stop Codon detection functions test data

The data included in this folder can be used to validate changes in the script `frameshift_deletions_checks` that may affect the stop codon detection functions.

We cover 6 main scenarios and for each of them we provide the input BAM file to use as valdation and a known good output to use as comparison.

The 6 available scenarios are:
- Normal stopgain event
- Normal stoploss event
- Stopgain event in overlap with insertions
- Stopgain event in overlap with deletions
- Stoploss event in overlap with insertions
- Stoploss event in overlap with deletions

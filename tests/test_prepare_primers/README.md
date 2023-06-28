# V-pipe primer file building functions test data

The data included in this folder can be used to validate changes in the script `prepare_primers`.

The test is based on the official ARTIC primers v5.3.2 available on github (https://github.com/quick-lab/SARS-CoV-2)

Due to the primer naming structure of this specific version, the required options are as follows:

```
./prepare_primers --primerfile SARs-CoV-2_v5.3.2_400.primer.bed --output SARS-CoV-2 --change_ref "NC_045512.2" --primer_name_sep "_" --primer_number_pos 2 --primer_side_pos 3
```

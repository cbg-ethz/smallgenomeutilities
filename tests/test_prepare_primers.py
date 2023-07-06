import subprocess
from pathlib import PurePath
import pytest


@pytest.mark.parametrize("virus", ["SARS-CoV-2"])
def test_workflow(tmp_path, virus):
    datapath = PurePath("tests/test_prepare_primers")

    # run params
    infile = datapath / f"{virus}.bed"  # input parameter
    outparam = tmp_path / virus  # output parameter
    # files
    exptsv = datapath / f"{virus}.tsv"  # expected
    outtsv = tmp_path / f"{virus}.tsv"  # current
    expfa = datapath / f"{virus}.primer.fasta"  # expected
    outfa = tmp_path / f"{virus}.primer.fasta"  # current
    expbed = datapath / f"{virus}.insert.bed"  # expected
    outbed = tmp_path / f"{virus}.insert.bed"  # current

    subprocess.check_call(
        [
            "prepare_primers",
            f"--primerfile={infile}",
            "--change_ref=NC_045512.2",
            "--primer_name_sep=_",
            "--primer_number_pos=2",
            "--primer_side_pos=3",
            f"--output={outparam}",
        ]
    )

    # check output
    print("Testing TSV...")
    assert [r for r in open(exptsv, "rt")] == [row for row in open(outtsv, "rt")]
    print("Testing FASTA...")
    assert [r for r in open(expfa, "rt")] == [row for row in open(outfa, "rt")]
    print("Testing inserts BED...")
    assert [r for r in open(expbed, "rt")] == [row for row in open(outbed, "rt")]

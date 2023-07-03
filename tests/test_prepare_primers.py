import subprocess
from pathlib import PurePath


def run_prepare_primers(datapath, tmp_path, combin):
    # run params
    infile = datapath / f'{combin}.bed' # input parameter
    outparam = tmp_path / combin # output parameter
    # files
    exptsv = datapath / f"{combin}.tsv"  # expected
    outtsv = tmp_path / f"{combin}.tsv"  # current
    expfa = datapath / f"{combin}.primer.fasta"  # expected
    outfa = tmp_path / f"{combin}.primer.fasta"  # current
    expbed = datapath / f"{combin}.insert.bed"  # expected
    outbed = tmp_path / f"{combin}.insert.bed"  # current

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


def test_workflow(tmp_path):
    # data: its handled with LFS
    datapath = PurePath("tests/test_prepare_primers")

    # test stop codons in frameshift_deletions_checks
    run_prepare_primers(
                datapath, tmp_path, "SARS-CoV-2"
            )

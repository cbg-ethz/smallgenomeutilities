import subprocess
from pathlib import PurePath


def run_frameshift_deletions_checks(datapath, tmp_path, combin):
    exp = datapath / f"{combin}.tsv"  # expected
    out = tmp_path / f"{combin}.tsv"  # current

    subprocess.check_call(
        [
            "frameshift_deletions_checks",
            f"--input={datapath / f'{combin}.cram'}",
            f"--consensus={datapath / f'{combin}.fasta'}",
            f"--reference={datapath / 'NC_045512.2.fasta'}",
            f"--genes={datapath / 'Genes_NC_045512.2.GFF3'}",
            f"--output={out}",
        ]
    )

    # check output
    assert [r for r in open(exp, "rt")] == [row for row in open(out, "rt")]


def test_workflow(tmp_path):
    # data: its handled with LFS
    datapath = PurePath("tests/test_frameshift_deletions_checks")

    # test stop codons in frameshift_deletions_checks
    for stoptype in ["gain", "loss"]:
        for variant in ["", "_with_deletions", "_with_insertions"]:
            run_frameshift_deletions_checks(
                datapath, tmp_path, f"stop{stoptype}{variant}"
            )

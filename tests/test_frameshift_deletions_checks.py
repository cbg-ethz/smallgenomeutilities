import itertools
import subprocess
from pathlib import PurePath
import pytest


# test stop codons in frameshift_deletions_checks with various combination of gain/losses and insertions/deletions
@pytest.mark.parametrize(
    "combin",
    (
        f"stop{stoptype}{ ( '_with_' + variant) if variant else '' }"
        for stoptype, variant in itertools.product(
            ["gain", "loss"], [None, "deletions", "insertions"]
        )
    ),
)
def test_workflow(tmp_path, combin):
    # data: its handled with LFS
    datapath = PurePath("tests/test_frameshift_deletions_checks")

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

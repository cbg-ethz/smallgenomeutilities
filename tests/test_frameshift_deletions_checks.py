import itertools
import subprocess
from pathlib import PurePath
import pytest

# get the functions from a script file
import importlib.machinery
import importlib.util
from pathlib import Path

# Get path to script
script_dir = Path(__file__).parent
frmdelchk_path = str(
    script_dir.joinpath("..", "scripts", "frameshift_deletions_checks")
)

# Import script as a module
loader = importlib.machinery.SourceFileLoader(
    "frameshift_deletions_checks", frmdelchk_path
)
spec = importlib.util.spec_from_loader("frameshift_deletions_checks", loader)
frameshift_deletions_checks = importlib.util.module_from_spec(spec)
loader.exec_module(frameshift_deletions_checks)


# test stop codons in frameshift_deletions_checks with various combination of gain/losses and insertions/deletions
stop_combinations = [
    f"stop{stoptype}{ ( '_with_' + variant) if variant else '' }"
    for stoptype, variant in itertools.product(
        ["gain", "loss"], [None, "deletions", "insertions"]
    )
]


@pytest.mark.parametrize(
    "combin",
    stop_combinations,
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


def bioaln2dic(aln):
    return {
        f"{i}-{'con' if i & 1 else 'ref'}-{r.id}": str(r.seq) for i, r in enumerate(aln)
    }


@pytest.mark.parametrize(
    "combin",
    stop_combinations,
)
def test_align(combin):
    datapath = PurePath("tests/test_frameshift_deletions_checks")

    ref = datapath / "NC_045512.2.fasta"
    con = datapath / f"{combin}.fasta"
    chn = datapath / f"{combin}.chain"

    with_chain = frameshift_deletions_checks.align_with_chain(ref, con, chn)
    with_mafft = frameshift_deletions_checks.align(ref, str(con))

    assert bioaln2dic(with_chain) == bioaln2dic(with_mafft)

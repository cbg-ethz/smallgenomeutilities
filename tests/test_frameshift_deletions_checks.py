import itertools
import difflib
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
            f"--chain={datapath / f'{combin}.chain'}",
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
    [
        pytest.param(
            c,
            marks=pytest.mark.xfail(reason="bcftools issue #1963: inconsistant output"),
        )
        if "stopgain_with_insertions" == c
        else c
        for c in stop_combinations
    ],
)
def test_mark_del(combin):
    datapath = PurePath("tests/test_frameshift_deletions_checks")

    ref = datapath / "NC_045512.2.fasta"
    # gaps marked as '-' in the consensus
    con_gap = datapath / f"{combin}.fasta"
    chn_gap = datapath / f"{combin}.chain"
    # gaps not marked. listed in chain file instead
    con_ngp = datapath / f"{combin}_nogap.fasta"
    chn_ngp = datapath / f"{combin}_nogap.chain"

    with_chain = frameshift_deletions_checks.align_with_chain(ref, con_gap, chn_gap)
    with_nogap = frameshift_deletions_checks.align_with_chain(ref, con_ngp, chn_ngp)

    with_chain_dict = bioaln2dic(with_chain)
    with_nogap_dict = bioaln2dic(with_nogap)

    assert with_chain_dict == with_nogap_dict


# corner cases: sometimes MAFFT produces alignment gaps that differ from what
# bcftools writes in the consensus and/or declares in .chain files.
# (e.g.: bcftools prefers codon-aligned deletions in consensus, whereas
# mafft re-shifts them left-most)
# Expected differences are expressed as difflib opcodes.
align_expect_diffs = {
    "stopgain_with_insertions": {
        #    24120     24130     24140     24150
        #      . | .  :  . |.  .| .  :  . |.  .|
        # chain: caaaagtttaacggcct------tttgccac
        #                        -     +
        # mafft: caaaagtttaacggcc------ttttgccac
        #                   \_/\_/\_/\_/\_/
        "1-con-NC_045512.2": [
            ("equal", 0, 24135, 0, 24135),
            ("delete", 24135, 24136, 24135, 24135),
            ("equal", 24136, 24145, 24135, 24144),
            ("replace", 24145, 29905, 24144, 29905),
        ],
    },
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
    with_mafft = frameshift_deletions_checks.align_with_mafft(ref, con)

    with_chain_dict = bioaln2dic(with_chain)
    with_mafft_dict = bioaln2dic(with_mafft)

    combin_diffs = align_expect_diffs.get(combin)
    if combin_diffs is None:
        # normal compare
        assert with_chain_dict == with_mafft_dict

    else:
        # handle corner cases
        assert set(with_chain_dict.keys()) == set(with_mafft_dict.keys())
        for k in with_chain_dict.keys():
            expect_diff = combin_diffs.get(k)

            if expect_diff is None:
                # normal match
                assert with_chain_dict[k] == with_mafft_dict[k]
            else:
                # expected not to match,
                # check if the *differences* are expected
                observed_diff = difflib.SequenceMatcher(
                    a=with_chain_dict[k], b=with_mafft_dict[k]
                ).get_opcodes()
                assert expect_diff == observed_diff

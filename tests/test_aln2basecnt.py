import subprocess
from pathlib import PurePath
import json
import pytest


@pytest.mark.parametrize(
    "combin",
    [
        {"first": "1", "name": "mini", "ext": "yaml"},
        {"first": "0", "name": "mini_merged", "ext": "ini"},
    ],
)
def test_aln2basecnt(tmp_path, combin):
    # micro text with file with corner cases
    minipath = PurePath("tests/mini_sam")
    datapath = PurePath("tests/test_aln2basecnt")

    # prepare data
    tmp_data = tmp_path / f"{combin['name']}.bam"
    subprocess.run(
        [
            "samtools",
            "sort",
            "-o",
            tmp_data,
            minipath / f"{combin['name']}.sam",
        ]
    )
    subprocess.run(
        [
            "samtools",
            "index",
            tmp_data,
        ]
    )

    files = {
        "bscnt": f"{combin['name']}.basecnt.tsv",
        "cov": f"{combin['name']}.coverage.tsv",
        "stat": f"{combin['name']}.stats.{combin['ext']}",
    }
    exp = {f: datapath / f for f in files.values()}  # expected
    out = {f: tmp_path / f for f in files.values()}  # current

    subprocess.check_call(
        [
            "aln2basecnt",
            "--name",
            combin["name"],
            "--first",
            combin["first"],
            "--basecnt",
            out[files["bscnt"]],
            "--coverage",
            out[files["cov"]],
            "--stats",
            out[files["stat"]],
            tmp_data,
        ]
    )

    # check output
    for f in files.values():
        with open(exp[f], "rt") as expf, open(out[f], "rt") as outf:
            assert [r for r in expf] == [row for row in outf]


@pytest.mark.parametrize(
    "combin", ["stopgain_with_deletions", "stoploss", "stoploss_with_deletions"]
)
def test_aln2basecnt_more(tmp_path, combin):
    # data on LFS
    crampath = PurePath("tests/test_frameshift_deletions_checks")
    datapath = PurePath("tests/test_aln2basecnt")

    files = {
        "bscnt": f"{combin}.basecnt.tsv",
        "cov": f"{combin}.coverage.tsv",
        "stat": f"{combin}.stats.yaml",
    }
    exp = {f: datapath / f for f in files.values()}  # expected
    out = {f: tmp_path / f for f in files.values()}  # current

    subprocess.check_call(
        [
            "aln2basecnt",
            "--first",
            "1",
            "--basecnt",
            out[files["bscnt"]],
            "--coverage",
            out[files["cov"]],
            "--stats",
            out[files["stat"]],
            crampath / f"{combin}.cram",
        ]
    )

    # check output
    for f in files.values():
        with open(exp[f], "rt") as expf, open(out[f], "rt") as outf:
            assert [r for r in expf] == [row for row in outf]

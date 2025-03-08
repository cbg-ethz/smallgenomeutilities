import subprocess
from pathlib import PurePath
import json
import pytest


def test_aln2basecnt(tmp_path):
    # micro text with file with corner cases
    minipath = PurePath("tests/test_paired_end_read_merger")
    datapath = PurePath("tests/test_aln2basecnt")

    # prepare data
    subprocess.run(
        [
            "samtools",
            "sort",
            "-o",
            tmp_path / "mini.bam",
            minipath / "mini.sam",
        ]
    )
    subprocess.run(
        [
            "samtools",
            "index",
            tmp_path / "mini.bam",
        ]
    )

    files = ["mini.basecnt.tsv", "mini.coverage.tsv", "mini.stats.yaml"]
    exp = {f: datapath / f for f in files}  # expected
    out = {f: tmp_path / f for f in files}  # current

    subprocess.check_call(
        [
            "aln2basecnt",
            "--first",
            "1",
            "--basecnt",
            out["mini.basecnt.tsv"],
            "--coverage",
            out["mini.coverage.tsv"],
            "--stats",
            out["mini.stats.yaml"],
            tmp_path / "mini.bam",
        ]
    )

    # check output
    for f in files:
        with open(exp[f], "rt") as expf, open(out[f], "rt") as outf:
            assert [r for r in expf] == [row for row in outf]

import subprocess
from pathlib import PurePath
import json
import pytest


def test_covdpqc(tmp_path):
    # micro text with pseudo files
    # - test default behavious
    # - test absolute count
    datapath = PurePath("tests/test_coverage_depth_qc")

    exp = datapath / "qc_abs.json"  # expected
    out = tmp_path / "qc_abs.json"  # current

    subprocess.check_call(
        [
            "coverage_depth_qc",
            f"--output={out}",
            datapath / "coverage.tsv",
        ]
    )

    # check output
    with open(exp, "rt") as expf, open(out, "rt") as outf:
        assert json.load(expf) == json.load(outf)


def test_covdpqc_with_namedepthsize(tmp_path):
    # micro text with pseudo files
    # - test default behavious
    # - test relative count
    # - test passing depths, with multiple parameters
    # - test passing names
    # - test more references in chromsize (a and b) than in coverage (a only)
    datapath = PurePath("tests/test_coverage_depth_qc")

    exp = datapath / "qc_rel.json"  # expected
    out = tmp_path / "qc_rel.json"  # current

    subprocess.check_call(
        [
            "coverage_depth_qc",
            f"--output={out}",
            "-f",
            datapath / "chrom.size",
            "-d" "5,10",
            "-d" "15",
            "-n",
            "got",
            "--",
            datapath / "coverage.tsv",
        ]
    )

    # check output
    with open(exp, "rt") as expf, open(out, "rt") as outf:
        assert json.load(expf) == json.load(outf)

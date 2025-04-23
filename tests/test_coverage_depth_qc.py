import subprocess
from pathlib import PurePath, Path
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


def test_covdpqc_irma(tmp_path):
    # test IRMA's coverages tables
    datapath = PurePath("tests/test_coverage_depth_qc")

    exp = datapath / "qc_irma.json"  # expected
    out = tmp_path / "qc_irma.json"  # current

    subprocess.check_call(
        [
            "coverage_depth_qc",
            f"--output={out}",
            datapath / PurePath("results/tables/A_NA_N1-coverage.txt"),
        ]
    )

    # check output
    with open(exp, "rt") as expf, open(out, "rt") as outf:
        assert json.load(expf) == json.load(outf)


def test_covdpqc_samtools(tmp_path):
    # prepare data by reusing 1 file out of frameshift's test data
    frameshift_data_path = PurePath("tests/test_frameshift_deletions_checks")
    tmp_data = tmp_path / "coverage.samtools.tsv"
    subprocess.run(
        [
            "samtools",
            "depth",
            "-a",
            "-H",
            "-J",
            "-q",
            "2",
            "-o",
            tmp_data,
            frameshift_data_path / "stoploss_with_insertions.cram",
        ]
    )

    # test samtools's depth tables
    datapath = PurePath("tests/test_coverage_depth_qc")

    exp = datapath / "qc_samtools.json"  # expected
    out = tmp_path / "qc_samtools.json"  # current

    subprocess.check_call(
        [
            "coverage_depth_qc",
            f"--output={out}",
            tmp_data,
        ]
    )

    # check output
    with open(exp, "rt") as expf, open(out, "rt") as outf:
        assert json.load(expf) == json.load(outf)

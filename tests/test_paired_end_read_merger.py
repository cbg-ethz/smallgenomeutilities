import subprocess
from pathlib import PurePath
import json
import pytest


def test_paired_end_read_merger(tmp_path):
    # micro text with file with corner cases
    datapath = PurePath("tests/test_paired_end_read_merger")

    exp = datapath / "mini_merged.sam"  # expected
    out = tmp_path / "mini_merged.sam"  # current

    subprocess.check_call(
        [
            "paired_end_read_merger",
            f"--output={out}",
            datapath / "mini.sam",
        ]
    )

    # check output
    with open(exp, "rt") as expf, open(out, "rt") as outf:
        assert [r for r in expf] == [row for row in outf]

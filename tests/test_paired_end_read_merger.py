import subprocess
from pathlib import PurePath


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


def test_paired_end_read_merger_with_unpaired_unaligned(tmp_path):
    # Test with unaligned and unpaired outputs
    datapath = PurePath("tests/test_paired_end_read_merger")
    
    # Output files
    out = tmp_path / "test.sam"
    unpaired = tmp_path / "unpaired.sam"
    unaligned = tmp_path / "unaligned.sam"
    
    # Expected files
    exp_merged = datapath / "mini_merged_with_unpaired.sam"
    exp_unpaired = datapath / "mini_unpaired.sam"
    exp_unaligned = datapath / "mini_unaligned.sam"
    
    subprocess.check_call(
        [
            "paired_end_read_merger",
            f"--output={out}",
            f"--unpaired={unpaired}",
            f"--unaligned={unaligned}",
            datapath / "mini.sam",
        ]
    )
    
    # Check main output
    with open(exp_merged, "rt") as expf, open(out, "rt") as outf:
        assert [r for r in expf] == [row for row in outf]
    
    # Check unpaired output
    with open(exp_unpaired, "rt") as expf, open(unpaired, "rt") as outf:
        assert [r for r in expf] == [row for row in outf]
    
    # Check unaligned output 
    with open(exp_unaligned, "rt") as expf, open(unaligned, "rt") as outf:
        assert [r for r in expf] == [row for row in outf]



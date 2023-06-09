__version__ = "0.0.0"

# if it wasn't patched by the installer, get the installation-time one
if __version__ == "0.0.0":
    try:
        import importlib.metadata

        __version__ = importlib.metadata.version(__package__ or __name__)
    except:
        __version__ = "0.0.0"

# if it wasn't installed, get it from git
if __version__ == "0.0.0":
    import subprocess
    import os

    try:
        __version__ = (
            subprocess.check_output(
                ["git", "describe", "--tag"],
                cwd=os.path.dirname(os.path.abspath(__file__)),
            )
            .decode("ascii")
            .strip()
        ) or "0.0.0"
    except:
        __version__ = "0.0.0"

# if it wasn't cloned, get it from the git archive substituted
if __version__ == "0.0.0":
    import yaml

    try:
        with open(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "..", ".git_archival.txt"
            ),
            "rt",
        ) as yf:
            __version__ = yaml.load(yf, Loader=yaml.CLoader).get(
                "describe-name", "0.0.0"
            )

    except:
        __version__ = "0.0.0"

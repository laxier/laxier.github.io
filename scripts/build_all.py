#!/usr/bin/env python3
"""Build all resume PDFs used by the site."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
BUILD_CV = ROOT / "scripts/build_cv.py"


def run(source: str, output: str) -> None:
    subprocess.run(
        [sys.executable, str(BUILD_CV), output, "--source", source],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    run("docs/cv/hh-template.html", "docs/cv/Тимофеев_Кирилл_Юрьевич_hh_Resume_2026-10-14.pdf")
    print("HH PDF пересобран")
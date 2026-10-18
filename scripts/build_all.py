#!/usr/bin/env python3
"""Build the canonical HH PDF and update the site from that artifact."""

from datetime import datetime
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
BUILD_CV = ROOT / "scripts/build_cv.py"
SITE = ROOT / "index.html"
PDF = ROOT / "docs/cv/Тимофеев_Кирилл_Юрьевич_hh_Resume_2026-10-14.pdf"


def run(source: str, output: Path) -> None:
    subprocess.run(
        [sys.executable, str(BUILD_CV), str(output), "--source", source],
        cwd=ROOT,
        check=True,
    )


def update_site_from_pdf(pdf: Path) -> None:
    site = SITE.read_text(encoding="utf-8")
    pdf_href = pdf.relative_to(ROOT).as_posix()
    site = re.sub(r'href="docs/cv/[^"]+\.pdf"', f'href="{pdf_href}"', site, count=1)

    months = (
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря",
    )
    generated_at = datetime.fromtimestamp(pdf.stat().st_mtime)
    date_text = f"{generated_at.day} {months[generated_at.month - 1]} {generated_at.year}"
    site = re.sub(r"(<time data-deploy-date>)[^<]*", rf"\g<1>{date_text}", site, count=1)
    SITE.write_text(site, encoding="utf-8")
    print(f"Сайт обновлён из PDF: {pdf_href}, дата: {date_text}")


if __name__ == "__main__":
    run("docs/cv/hh-template.html", PDF)
    update_site_from_pdf(PDF)
    print("HH PDF пересобран")
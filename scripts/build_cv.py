#!/usr/bin/env python3
"""Build the HH resume PDF from the canonical resume template."""

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs/cv/hh-template.html"
DEFAULT_OUTPUT = ROOT / "docs/cv/Тимофеев_Кирилл_Юрьевич_hh_Resume_2026-10-14.pdf"


def build(source: Path, output: Path) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        raise SystemExit(
            "Playwright не установлен. Установите его командой: python3 -m pip install playwright"
        ) from error

    output.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 1600},
            device_scale_factor=1,
        )
        page.goto(source.as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.pdf(
            path=str(output),
            format="A4",
            print_background=True,
            margin={"top": "12mm", "right": "12mm", "bottom": "12mm", "left": "12mm"},
        )
        browser.close()

    try:
        display_path = output.relative_to(ROOT)
    except ValueError:
        display_path = output
    print(f"Готово: {display_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Собрать HH PDF-резюме из hh-template.html")
    parser.add_argument(
        "output",
        nargs="?",
        default=DEFAULT_OUTPUT,
        type=Path,
        help="путь к выходному PDF",
    )
    parser.add_argument(
        "--source",
        default=SOURCE,
        type=Path,
        help="HTML-источник для сборки; по умолчанию docs/cv/hh-template.html",
    )
    args = parser.parse_args()
    source_path = args.source.expanduser()
    if not source_path.is_absolute():
        source_path = ROOT / source_path
    output_path = args.output.expanduser()
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    build(source_path.resolve(), output_path.resolve())
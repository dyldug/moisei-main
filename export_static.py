# export_static.py
from __future__ import annotations

import re
import shutil
from pathlib import Path

from flask import render_template

from main import app  # your Flask app instance


# Map routes -> output HTML filenames
ROUTES = [
    ("/", "index.html", "index.html"),
    ("/contact", "contact.html", "contact.html"),
    ("/gallery", "gallery.html", "gallery.html"),
    # Do NOT export base.html; it's a layout template, not a page
]

OUT_DIR = Path("site")
STATIC_SRC = Path("static")
STATIC_DST = OUT_DIR / "static"


def rewrite_for_github_pages(html: str) -> str:
    """
    GitHub Pages project sites live under /<repo>/ (e.g. /moisei-main/).
    Absolute URLs like /static/... or /contact break. Convert to relative.
    """
    # Assets: /static/... -> static/...
    html = re.sub(r'(["\'])/static/', r"\1static/", html)

    # Internal links: href="/contact" -> href="contact.html"
    html = re.sub(r'href="/contact"\b', 'href="contact.html"', html)
    html = re.sub(r'href="/gallery"\b', 'href="gallery.html"', html)
    html = re.sub(r'href="/"\b', 'href="index.html"', html)

    # If you have other absolute href="/something", we can add more rewrites.
    return html


def clean_dir(path: Path) -> None:
    if path.exists():
        for item in path.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    else:
        path.mkdir(parents=True, exist_ok=True)


def build() -> None:
    clean_dir(OUT_DIR)

    # Copy static assets
    if STATIC_SRC.exists():
        shutil.copytree(STATIC_SRC, STATIC_DST)
    else:
        print("WARN: ./static not found; skipping copy")

    # Disable Jekyll to avoid surprises
    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")

    with app.app_context():
        for route, template_name, out_name in ROUTES:
            with app.test_request_context(route):
                rendered = render_template(template_name)

            rendered = rewrite_for_github_pages(rendered)
            (OUT_DIR / out_name).write_text(rendered, encoding="utf-8")
            print(f"Rendered {route} ({template_name}) -> {OUT_DIR/out_name}")

    print("Static export complete.")


if __name__ == "__main__":
    build()
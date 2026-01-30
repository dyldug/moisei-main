# export_static.py
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

from flask import render_template

# Import your Flask app instance
# Assumes main.py contains `app = Flask(__name__)`
from main import app  # noqa: E402


PAGES = [
    # (template_name, output_filename)
    ("index.html", "index.html"),
    ("contact.html", "contact.html"),
    ("gallery.html", "gallery.html"),
]

OUT_DIR = Path("site")  # build output (we'll deploy this)
STATIC_SRC = Path("static")
STATIC_DST = OUT_DIR / "static"


def _rewrite_asset_paths(html: str) -> str:
    """
    GitHub Pages project sites live under /<repo>/.
    Absolute paths like /static/... break, so rewrite them to relative static/...
    """
    html = re.sub(r'(["\'])/static/', r"\1static/", html)  # href="/static/..." -> "static/..."
    html = re.sub(r'(["\'])/favicon\.ico', r"\1favicon.ico", html)
    return html


def build() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Clean output except keep folder itself
    for item in OUT_DIR.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    # Copy static assets
    if STATIC_SRC.exists():
        shutil.copytree(STATIC_SRC, STATIC_DST)
    else:
        print("WARN: ./static not found; skipping copy")

    # Disable Jekyll (recommended)
    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")

    # Render templates
    with app.app_context():
        for template_name, out_name in PAGES:
            # Provide a request context so url_for works if used
            with app.test_request_context("/"):
                rendered = render_template(template_name)

            rendered = _rewrite_asset_paths(rendered)
            (OUT_DIR / out_name).write_text(rendered, encoding="utf-8")
            print(f"Rendered {template_name} -> {OUT_DIR/out_name}")

    print("Static export complete.")


if __name__ == "__main__":
    build()
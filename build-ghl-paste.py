#!/usr/bin/env python3
"""Build GHL paste package from demo.html + du-images + local assets."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent  # du-deliverables
DU = ROOT.parent  # dealer-ultimate
OUT = ROOT / "ghl-paste"
MEDIA = OUT / "media"


def add(src: Path, name: str) -> None:
    if not src.exists():
        print("MISSING", src)
        return
    dest = MEDIA / name
    shutil.copy2(src, dest)


def main() -> None:
    demo_path = ROOT / "demo.html"
    demo = demo_path.read_text(encoding="utf-8")

    if OUT.exists():
        shutil.rmtree(OUT)
    MEDIA.mkdir(parents=True)

    # --- assets ---
    add(ROOT / "du-logo-mark.png", "du-logo-mark.png")
    for name in [
        "du-hero-1.png",
        "du-contact-1.png",
        "du-more-buyers-1.png",
        "du-more-inventory-1.png",
        "du-service-1.png",
        "du-service-2.png",
        "du-service-3.png",
    ]:
        add(DU / "du-images" / name, name)

    for p in sorted((ROOT / "trust-logos").glob("*.png")):
        add(p, f"trust-{p.name}")

    for p in sorted((ROOT / "testimonials").iterdir()):
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            add(p, f"testimonial-{p.name}")

    fav = ROOT / "logo" / "favicon.svg"
    if fav.exists():
        add(fav, "favicon.svg")

    html = demo
    for a, b in [
        ("../du-images/", "media/"),
        ("du-logo-mark.png", "media/du-logo-mark.png"),
        ("testimonials/", "media/testimonial-"),
        ("trust-logos/", "media/trust-"),
        ('href="logo/favicon.svg"', 'href="media/favicon.svg"'),
    ]:
        html = html.replace(a, b)
    html = html.replace("media/media/", "media/")

    html = re.sub(
        r"/\*[\s\S]*?Gotham Black[\s\S]*?\*/\s*@font-face\s*\{[\s\S]*?\}\s*",
        "/* Gotham omitted for GHL paste — display falls back to Inter */\n    ",
        html,
        count=1,
    )
    html = re.sub(
        r'@font-face\s*\{\s*font-family:\s*"Gotham Black Wordmark";[\s\S]*?\}\s*',
        "",
        html,
        count=1,
    )
    html = html.replace(
        '--display: "Gotham", "Inter", system-ui, sans-serif;',
        '--display: "Inter", system-ui, sans-serif;',
    )
    html = html.replace(
        "<title>Dealer Ultimate — Hero</title>",
        "<title>Dealer Ultimate</title>",
    )

    banner = """<!DOCTYPE html>
<!--
  Dealer Ultimate — GHL paste version
  ------------------------------------
  1. Upload everything in ./media/ to GHL Media Library (or host on your CDN).
  2. If media URLs are absolute CDN links, set DU_MEDIA_BASE below to that folder
     URL (with trailing slash), e.g.
       window.DU_MEDIA_BASE = "https://storage.googleapis.com/msgsndr/XXXX/media/";
     Leave "" to use relative media/ paths (works when HTML and media/ ship together).
  3. In GHL: blank/custom page → Custom Code / HTML element → paste this full file
     (or paste <head> CSS+JS into site header and body into a full-width code block).
  4. Wire the #leadForm submit to a GHL form / webhook when you go live.
  Built from demo.html. Rebuild: python3 du-deliverables/build-ghl-paste.py
-->
"""
    if html.startswith("<!DOCTYPE html>"):
        html = banner + html[len("<!DOCTYPE html>") :].lstrip("\n")

    rewriter = """
  <script>
    /* Set after GHL media upload if paths are not relative */
    window.DU_MEDIA_BASE = window.DU_MEDIA_BASE || "";
    window.duMediaUrl = function (path) {
      if (!path) return path;
      var base = window.DU_MEDIA_BASE || "";
      if (!base) return path;
      if (base.slice(-1) !== "/") base += "/";
      return base + String(path).replace(/^media\\//, "");
    };
    (function () {
      if (!window.DU_MEDIA_BASE) return;
      document.querySelectorAll('img[src^="media/"]').forEach(function (img) {
        img.src = window.duMediaUrl(img.getAttribute("src"));
      });
      var icon = document.querySelector('link[rel="icon"][href^="media/"]');
      if (icon) icon.href = window.duMediaUrl(icon.getAttribute("href"));
    })();
  </script>
"""
    html = html.replace("<body>", '<body class="du-ghl">\n' + rewriter, 1)

    # Prefix testimonial carousel asset paths when CDN base is set
    html = html.replace(
        "var n = people.length;",
        """if (window.duMediaUrl) {
          people.forEach(function (p) {
            p.avatar = window.duMediaUrl(p.avatar);
            p.video = window.duMediaUrl(p.video);
          });
        }
        var n = people.length;""",
    )

    out_html = OUT / "demo-ghl-paste.html"
    out_html.write_text(html, encoding="utf-8")

    readme = """# GHL paste package

Source of truth: `../demo.html`. Rebuild with:

```bash
python3 upwork/dealer-ultimate/du-deliverables/build-ghl-paste.py
```

## Contents

| Path | Role |
|------|------|
| `demo-ghl-paste.html` | Full page HTML/CSS/JS for GoHighLevel |
| `media/` | Flattened images referenced by the HTML |

## Load in GoHighLevel

1. Upload the whole `media/` folder to **Sites → Media Library** (or a CDN).
2. Paste `demo-ghl-paste.html` into a blank/custom HTML page (or full-width Custom Code).
3. If GHL gives absolute CDN URLs, set near the top of `<body>`:
   ```html
   <script>window.DU_MEDIA_BASE = "https://storage.googleapis.com/msgsndr/YOUR_ID/media/";</script>
   ```
   (Must be the folder prefix for the files you uploaded; trailing slash required.)
4. `#leadForm` is demo-only until you wire a GHL form / webhook.
5. Inter from Google Fonts; Gotham not packaged (falls back to Inter).

## Image map

| Usage | `media/` file |
|-------|----------------|
| Logo / favicon | `du-logo-mark.png`, `favicon.svg` |
| Hero | `du-hero-1.png` |
| How (buyers / inventory / sales) | `du-more-buyers-1.png`, `du-more-inventory-1.png`, `du-hero-1.png` |
| Solutions | `du-service-1.png` … `du-service-3.png` |
| Contact | `du-contact-1.png` |
| Trust strip | `trust-Group-*.png` |
| Testimonials | `testimonial-*.png` / `.jpg` |
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")
    print(f"Wrote {out_html} ({out_html.stat().st_size} bytes)")
    print(f"Media files: {len(list(MEDIA.iterdir()))}")


if __name__ == "__main__":
    main()

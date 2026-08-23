"""Download a curated set of freely-licensed sample photos from Wikimedia Commons.

Everyday subjects for the day-in-the-life labs (L4 image search, L5 multimodal
day). One image per topic. Records source URL, license, and attribution in
ro_shared_data/images/CREDITS.json.

Files that already exist are kept as-is, so a re-run only fills gaps and never
clobbers a vetted photo. Set REFRESH=1 to re-download everything.
"""
import html
import json
import os
import re
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image


def _strip_html(text):
    """Wikimedia returns HTML in metadata; keep just the human-readable name."""
    return html.unescape(re.sub(r"<[^>]+>", "", text or "")).strip()


OUT = Path("ro_shared_data/images")
OUT.mkdir(parents=True, exist_ok=True)
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "qdrant-edge-course/1.0 (educational sample; contact dylan.couzon@qdrant.com)"}
MIN_SIDE = 240  # reject thumbnails/icons

# filename stem -> Commons search term. The first six match the original set.
# 17 everyday subjects for the day-in-the-life labs.
TOPICS = {
    "sneakers": "white sneakers shoe",
    "coffee": "cappuccino cup cafe",
    "restaurant": "restaurant plate food",
    "book": "stack of books",
    "street": "busy city street cars daytime",
    "plant": "potted houseplant",
    "bakery": "croissant bakery pastry",
    "pizza": "pizza margherita plate",
    "ramen": "ramen bowl noodles",
    "laptop": "person using laptop cafe table",
    "meeting": "business people meeting conference table",
    "bicycle": "bicycle parked street",
    "train": "train station platform",
    "park": "city park green lawn sunny day",
    "gym": "gym dumbbells weights",
    "kitchen": "modern kitchen counter interior bright",
    "dog": "dog pet sitting",
}


def _get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def _download_valid(thumb):
    """Fetch bytes and confirm they decode to a big-enough image."""
    req = urllib.request.Request(thumb, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    img = Image.open(BytesIO(raw))
    img.verify()  # raises on a corrupt file
    if min(img.size) < MIN_SIDE:
        return None
    return raw


def fetch(stem, term):
    data = _get({
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": f"filetype:bitmap {term}", "gsrlimit": 8, "gsrnamespace": 6,
        "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 640,
    })
    pages = list(data.get("query", {}).get("pages", {}).values())
    pages.sort(key=lambda p: p.get("index", 99))  # keep search rank order
    for page in pages:
        info = page["imageinfo"][0]
        thumb = info.get("thumburl")
        if not thumb or not thumb.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        try:
            raw = _download_valid(thumb)
        except Exception:
            continue
        if raw is None:
            continue
        ext = ".jpg" if thumb.lower().endswith((".jpg", ".jpeg")) else ".png"
        dest = OUT / f"{stem}{ext}"
        dest.write_bytes(raw)
        meta = info.get("extmetadata", {})
        return {
            "file": dest.name, "topic": term,
            "source": info.get("descriptionurl", ""),
            "license": meta.get("LicenseShortName", {}).get("value", "see source"),
            "artist": _strip_html(meta.get("Artist", {}).get("value", "")),
        }
    return None


def main():
    refresh = os.environ.get("REFRESH") == "1"
    creds_path = OUT / "CREDITS.json"
    existing = {c["file"]: c for c in json.loads(creds_path.read_text())} \
        if creds_path.exists() else {}
    credits = dict(existing)

    for stem, term in TOPICS.items():
        have = list(OUT.glob(f"{stem}.*"))
        if have and not refresh:
            print(f"= {have[0].name:16} kept (exists)")
            continue
        try:
            c = fetch(stem, term)
            if c:
                credits[c["file"]] = c
                print(f"+ {c['file']:16} {c['license']:20} {c['source']}")
            else:
                print(f"x {stem}: no image passed validation")
        except Exception as e:
            print(f"x {stem}: {e}")

    ordered = [credits[f] for f in sorted(credits)]
    creds_path.write_text(json.dumps(ordered, indent=2))
    print(f"\n{len(ordered)} images credited in {creds_path}")


if __name__ == "__main__":
    main()

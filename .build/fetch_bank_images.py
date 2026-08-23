"""Download a bank of freely-licensed everyday-life photos for the L4 image bank.

L4 §5 lets students type any description and see the nearest photo. A wider bank
makes that feel open instead of limited to a handful of curated shots. This
fetcher pulls one photo per everyday subject from license-free pools only:

  1. Openverse, filtered to CC0 + Public Domain Mark (no attribution required).
  2. Wikimedia Commons, accepting only PD / CC0 results, as a fallback.

The license filter is hard: an image is saved only if its license is in
ALLOWED_LICENSES. Anything requiring attribution (CC BY, CC BY-SA) is skipped,
so the shipped course carries no per-image credit lines. Provenance is still
recorded in ro_shared_data/bank/CREDITS.json for our own records.

Files that already exist are kept, so a re-run only fills gaps. REFRESH=1
re-downloads. Downscales to <= MAX_SIDE px to keep the repo light.
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

OUT = Path("ro_shared_data/bank")
OUT.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "qdrant-edge-course/1.0 (educational sample; contact dylan.couzon@qdrant.com)"}
MIN_SIDE = 240        # reject thumbnails/icons
MAX_SIDE = 512        # downscale big photos; CLIP sees 224 anyway
OPENVERSE = "https://api.openverse.org/v1/images/"
COMMONS = "https://commons.wikimedia.org/w/api.php"

# License-free only. Normalized lowercase substrings that mean "no attribution".
ALLOWED_LICENSES = ("cc0", "pdm", "public domain", "publicdomain",
                    "no known copyright")

# Everyday subjects a person might photograph in a day/week. One image each.
TERMS = [
    # food & drink
    "coffee cup", "espresso", "cappuccino", "latte art", "tea cup",
    "ramen bowl", "pizza slice", "hamburger", "sushi platter", "tacos",
    "salad bowl", "sandwich", "croissant", "bagel", "donut", "cupcake",
    "chocolate cake", "ice cream cone", "pancakes", "waffles", "steak dinner",
    "fried chicken", "french fries", "pasta bowl", "soup bowl", "curry rice",
    "dumplings", "noodles", "breakfast plate", "fruit bowl", "smoothie",
    "beer glass", "red wine glass", "cocktail", "orange juice", "water bottle",
    # produce
    "apple fruit", "banana", "orange fruit", "strawberries", "grapes",
    "watermelon", "avocado", "tomato", "carrot", "broccoli", "lemon",
    "bell pepper", "mushroom", "corn cob", "potato", "onion",
    # places & scenes
    "city street", "coffee shop interior", "restaurant table", "library shelves",
    "park bench", "beach sunset", "mountain landscape", "forest trail",
    "train station", "subway platform", "airport terminal", "bus stop",
    "office desk", "kitchen counter", "living room", "bedroom", "bathroom",
    "grocery store aisle", "farmers market", "bookstore", "museum gallery",
    "gym interior", "swimming pool", "playground", "parking lot",
    "gas station", "bridge over river", "skyline at night", "snowy street",
    "rainy window", "garden flowers", "waterfall", "desert dunes", "lake",
    # objects & tech
    "laptop computer", "smartphone", "desktop monitor", "keyboard", "computer mouse",
    "headphones", "wireless earbuds", "camera", "television", "game controller",
    "wristwatch", "wall clock", "eyeglasses", "sunglasses", "umbrella",
    "backpack", "handbag", "wallet", "keys", "house keys", "notebook journal",
    "ballpoint pen", "pencil", "scissors", "stapler", "calculator",
    "coffee mug", "water glass", "wine bottle", "frying pan", "cooking pot",
    "kitchen knife", "fork and spoon", "plate", "bowl", "toaster", "blender",
    "microwave oven", "refrigerator", "washing machine", "vacuum cleaner",
    "hair dryer", "toothbrush", "soap bar", "towel", "candle", "light bulb",
    "flower vase", "potted plant", "cactus plant", "picture frame", "mirror",
    "pillow", "blanket", "chair", "wooden table", "sofa couch", "bed",
    "bookshelf", "lamp", "desk fan", "guitar", "piano", "drum kit",
    "violin", "microphone", "vinyl record", "book stack", "magazine",
    "newspaper", "map", "globe", "chess set", "playing cards", "dice",
    "soccer ball", "basketball", "tennis racket", "baseball glove",
    "dumbbell weights", "yoga mat", "skateboard", "roller skates",
    "fishing rod", "tent camping", "backpacking gear", "hiking boots",
    "running shoes", "high heels", "leather boots", "sandals", "winter coat",
    "denim jacket", "t-shirt", "baseball cap", "wool scarf", "gloves",
    "necktie", "wristband", "ring jewelry", "necklace", "earrings",
    # vehicles
    "bicycle", "motorcycle", "red car", "pickup truck", "city bus",
    "yellow taxi", "delivery van", "sailboat", "airplane", "helicopter",
    "scooter", "skateboarding", "cargo ship", "fire truck", "ambulance",
    # animals & pets
    "dog puppy", "cat", "goldfish", "parrot bird", "rabbit", "hamster",
    "horse", "cow", "sheep", "chicken hen", "duck pond", "butterfly",
    "honeybee", "squirrel", "owl", "penguin", "elephant", "lion",
    "giraffe", "dolphin", "turtle", "frog", "ladybug", "spider web",
    # nature & weather
    "autumn leaves", "cherry blossom", "sunflower", "rose flower", "tulip",
    "pine tree", "palm tree", "rainbow sky", "lightning storm", "full moon",
    "starry night sky", "snowflakes", "morning fog", "ocean waves",
    "river stream", "green hills", "wheat field", "vineyard",
    # tools & misc
    "hammer tool", "screwdriver", "wrench", "power drill", "measuring tape",
    "paint brush", "ladder", "toolbox", "garden shovel", "watering can",
    "wheelbarrow", "lawnmower", "fire extinguisher", "first aid kit",
    "traffic light", "street sign", "mailbox", "park fountain", "statue",
    "birthday balloons", "gift box", "christmas tree", "jack o lantern",
    "wedding cake", "bouquet flowers", "shopping cart", "cash register",
    "credit card", "coins money", "piggy bank", "hourglass", "compass",
    "binoculars", "telescope", "microscope", "thermometer", "stethoscope",
]


def _norm(text):
    return re.sub(r"<[^>]+>", "", html.unescape(text or "")).strip()


def _license_ok(name):
    low = (name or "").lower()
    return any(tok in low for tok in ALLOWED_LICENSES)


def _get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def _download_scaled(src):
    """Fetch, validate min size, downscale to MAX_SIDE, return JPEG bytes."""
    req = urllib.request.Request(src, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    img = Image.open(BytesIO(raw))
    img.load()
    if min(img.size) < MIN_SIDE:
        return None
    img = img.convert("RGB")
    if max(img.size) > MAX_SIDE:
        scale = MAX_SIDE / max(img.size)
        img = img.resize((round(img.width * scale), round(img.height * scale)))
    buf = BytesIO()
    img.save(buf, "JPEG", quality=85)
    return buf.getvalue()


def _from_openverse(term):
    q = urllib.parse.urlencode({
        "q": term, "license": "cc0,pdm", "page_size": 8,
        "mature": "false", "aspect_ratio": "wide,square",
    })
    data = _get_json(OPENVERSE + "?" + q)
    for res in data.get("results", []):
        if not _license_ok(res.get("license", "")):
            continue
        src = res.get("url")
        if not src:
            continue
        try:
            raw = _download_scaled(src)
        except Exception:
            continue
        if raw:
            return raw, {
                "source": res.get("foreign_landing_url") or src,
                "license": res.get("license", "cc0"),
                "creator": _norm(res.get("creator", "")),
                "via": "openverse",
            }
    return None


def _from_commons(term):
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": f"filetype:bitmap {term}", "gsrlimit": 8, "gsrnamespace": 6,
        "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 640,
    })
    data = _get_json(COMMONS + "?" + q)
    pages = list(data.get("query", {}).get("pages", {}).values())
    pages.sort(key=lambda p: p.get("index", 99))
    for page in pages:
        info = page["imageinfo"][0]
        meta = info.get("extmetadata", {})
        lic = meta.get("LicenseShortName", {}).get("value", "")
        if not _license_ok(lic):
            continue
        thumb = info.get("thumburl")
        if not thumb:
            continue
        try:
            raw = _download_scaled(thumb)
        except Exception:
            continue
        if raw:
            return raw, {
                "source": info.get("descriptionurl", ""),
                "license": lic,
                "creator": _norm(meta.get("Artist", {}).get("value", "")),
                "via": "commons",
            }
    return None


def fetch(term):
    for source in (_from_openverse, _from_commons):
        try:
            got = source(term)
        except Exception:
            got = None
        if got:
            return got
    return None


def main():
    refresh = os.environ.get("REFRESH") == "1"
    creds_path = OUT / "CREDITS.json"
    credits = {c["file"]: c for c in json.loads(creds_path.read_text())} \
        if creds_path.exists() else {}

    kept = added = missed = 0
    for term in TERMS:
        stem = re.sub(r"[^a-z0-9]+", "_", term.lower()).strip("_")
        if list(OUT.glob(f"{stem}.jpg")) and not refresh:
            kept += 1
            continue
        got = fetch(term)
        if not got:
            missed += 1
            print(f"x {stem}: no license-free image")
            continue
        raw, meta = got
        dest = OUT / f"{stem}.jpg"
        dest.write_bytes(raw)
        credits[dest.name] = {"file": dest.name, "term": term, **meta}
        added += 1
        print(f"+ {dest.name:28} {meta['license']:14} {meta['via']}")

    ordered = [credits[f] for f in sorted(credits)]
    creds_path.write_text(json.dumps(ordered, indent=2))
    print(f"\nkept {kept}, added {added}, missed {missed} "
          f"-> {len(ordered)} images in {OUT}")


if __name__ == "__main__":
    main()

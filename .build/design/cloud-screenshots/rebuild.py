"""Re-cut the appendix's cloud screenshots and print their base64 to paste in."""
import base64, json, pathlib
from PIL import Image

HERE = pathlib.Path(__file__).parent
SHOTS = {"create-cluster": "Qdrant Cloud dashboard with the Create a Free "
                           "Cluster panel: a cluster name field, the free "
                           "tier's resources, and cloud provider and region "
                           "pickers",
         "api-key": "The API Key Created dialog in Qdrant Cloud, warning "
                    "that the key cannot be read in full again, with a "
                    "copy button beside it"}


def data_uri(name):
    return ("data:image/png;base64,"
            + base64.b64encode((HERE / f"{name}.png").read_bytes()).decode())


def resize(src_dir, width=760):
    for name in SHOTS:
        im = Image.open(pathlib.Path(src_dir) / f"{name}.png").convert("RGB")
        w, h = im.size
        im.resize((width, round(h * width / w)), Image.LANCZOS).save(
            HERE / f"{name}.png", optimize=True)


if __name__ == "__main__":
    for name, alt in SHOTS.items():
        print(f"{name}: {len(data_uri(name)) // 1024} KB of base64, alt={alt[:40]}...")

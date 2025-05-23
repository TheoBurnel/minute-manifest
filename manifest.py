# generate_manifest.py
from pathlib import Path
from iiif_prezi3 import Manifest, Canvas, AnnotationPage, Annotation

# 1. dossier contenant les images, ici le dossier courant
img_dir = Path(__file__).parent

# 2. base URL brute de ton dépôt GitHub
base = "https://raw.githubusercontent.com/TheoBurnel/minute-manifest/main/"

# 3. toutes les images JPG triées par nom
images = sorted(p for p in img_dir.glob("*.jpg"))

manifest = Manifest(
    id=f"{base}manifest.json",
    label={"fr": ["Minute du registre 11 J 184"]}
)

for idx, img_path in enumerate(images, start=1):
    alto_path = img_path.with_suffix(".xml")

    canvas_id = f"{base}canvas/{idx}"
    canvas = Canvas(
        id=canvas_id,
        width=3000,
        height=4000,
        label={"fr": [f"Page {idx}"]}
    )

    image_url = f"{base}{img_path.name}"
    annotation = Annotation(
        id=f"{canvas_id}/ann",
        motivation="painting",
        body={
            "id": image_url,
            "type": "Image",
            "format": "image/jpeg",
            "width": 3000,
            "height": 4000
        },
        target=canvas_id
    )

    page = AnnotationPage(id=f"{canvas_id}/ap", items=[annotation])
    canvas.items.append(page)

    if alto_path.exists():
        canvas.seeAlso = [{
            "id": f"{base}{alto_path.name}",
            "type": "Text",
            "format": "application/xml",
            "label": {"fr": ["Fichier ALTO"]}
        }]

    manifest.items.append(canvas)

with open("manifest.json", "w") as f:
    f.write(manifest.json(indent=2))

print("✅ Manifest généré : manifest.json")
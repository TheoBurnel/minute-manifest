import os
import json
from PIL import Image

# === CONFIGURATION ===
BASE_URL = "https://raw.githubusercontent.com/TheoBurnel/minute-manifest/main"  # URL de base pour les images (à adapter)
OUTPUT_FILE = "manifest.json"
IMAGES_FOLDER = "."  # Chemin local vers tes images

# === MANIFEST IIIF v2.0 ===
manifest = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": f"{BASE_URL}/manifest.json",
    "@type": "sc:Manifest",
    "label": "Mon Manuscrit",
    "sequences": [{
        "@type": "sc:Sequence",
        "@id": f"{BASE_URL}/sequence/normal",
        "canvases": []
    }]
}

# === Génération des canvas à partir des images ===
images = sorted([f for f in os.listdir(IMAGES_FOLDER) if f.lower().endswith(".jpg")])

for idx, filename in enumerate(images):
    image_path = os.path.join(IMAGES_FOLDER, filename)
    with Image.open(image_path) as img:
        width, height = img.size

    canvas_id = f"{BASE_URL}/canvas/{idx+1}"
    image_id = f"{BASE_URL}/image/{idx+1}"
    image_url = f"{BASE_URL}/files/{filename}"

    canvas = {
        "@type": "sc:Canvas",
        "@id": canvas_id,
        "label": f"Page {idx+1}",
        "height": height,
        "width": width,
        "images": [{
            "@type": "oa:Annotation",
            "motivation": "sc:painting",
            "on": canvas_id,
            "resource": {
                "@type": "dctypes:Image",
                "@id": image_url,
                "format": "image/jpeg",
                "height": height,
                "width": width,
                "service": {
                    "@context": "http://iiif.io/api/image/2/context.json",
                    "@id": image_url.rsplit('.', 1)[0],  # URL sans .jpg
                    "profile": "http://iiif.io/api/image/2/level1.json"
                }
            }
        }]
    }

    manifest["sequences"][0]["canvases"].append(canvas)

# === Écriture du fichier JSON ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"✅ Manifest IIIF v2.0 généré avec succès : {OUTPUT_FILE}")
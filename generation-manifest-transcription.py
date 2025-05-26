import os
import json
from PIL import Image

# === CONFIGURATION ===
BASE_URL = "https://raw.githubusercontent.com/TheoBurnel/minute-manifest/main"
OUTPUT_FILE = "manifest.json"
IMAGES_FOLDER = "."  # Dossier local contenant les .jpg et .xml
LABEL = "Minute du registre 11 J 184"

# === INIT MANIFEST IIIF v2.0 ===
manifest = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": f"{BASE_URL}/manifest.json",
    "@type": "sc:Manifest",
    "label": LABEL,
    "sequences": [{
        "@type": "sc:Sequence",
        "@id": f"{BASE_URL}/manifest.json/sequence/normal",
        "canvases": []
    }]
}

# === LISTE DES IMAGES JPG ===
images = sorted([f for f in os.listdir(IMAGES_FOLDER) if f.lower().endswith(".jpg")])

# === BOUCLE DE CRÉATION DES CANVASES ===
for idx, img_filename in enumerate(images):
    base_name = os.path.splitext(img_filename)[0]  # ex: 11_J_184_0023
    xml_filename = f"{base_name}.xml"

    img_path = os.path.join(IMAGES_FOLDER, img_filename)
    with Image.open(img_path) as img:
        width, height = img.size

    canvas_id = f"{BASE_URL}/canvas/{idx+1}"
    annotation_id = f"{canvas_id}/ann"
    img_url = f"{BASE_URL}/{img_filename}"
    xml_url = f"{BASE_URL}/{xml_filename}"

    canvas = {
        "@id": canvas_id,
        "@type": "sc:Canvas",
        "label": f"Page {idx+1}",
        "height": height,
        "width": width,
        "images": [{
            "@type": "oa:Annotation",
            "motivation": "sc:painting",
            "@id": annotation_id,
            "resource": {
                "@id": img_url,
                "@type": "dctypes:Image",
                "format": "image/jpeg",
                "height": height,
                "width": width
            },
            "on": canvas_id
        }]
    }

    # Ajout du seeAlso si le fichier XML existe localement
    if os.path.exists(os.path.join(IMAGES_FOLDER, xml_filename)):
        canvas["seeAlso"] = [{
            "@id": xml_url,
            "format": "application/xml",
            "label": "OCR text",
            "profile": "http://www.loc.gov/standards/alto/ns-v4#"
        }]

    manifest["sequences"][0]["canvases"].append(canvas)

# === ÉCRITURE DU FICHIER JSON ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"✅ Manifest IIIF v2.0 généré avec succès : {OUTPUT_FILE}")
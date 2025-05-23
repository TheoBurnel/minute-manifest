import json
import requests
from lxml import etree
from io import BytesIO

# Charger le manifeste IIIF
url_manifest = "https://raw.githubusercontent.com/TheoBurnel/minute-manifest/main/manifest.json"
manifest = requests.get(url_manifest).json()

# Parcourir les canvas
for canvas in manifest.get("items", []):
    see_also = canvas.get("seeAlso", [])
    annotation_page = canvas["items"][0]
    
    for see in see_also:
        if see["format"] == "application/xml":
            alto_url = see["id"]
            alto_response = requests.get(alto_url)
            tree = etree.parse(BytesIO(alto_response.content))

            # Extraire le texte ligne à ligne
            ns = {"alto": "http://www.loc.gov/standards/alto/ns-v4#"}
            lines = tree.xpath("//alto:String", namespaces=ns)
            words = [line.attrib.get("CONTENT", "") for line in lines]
            transcription = " ".join(words)

            # Ajouter une annotation de transcription
            annotation = {
                "id": canvas["id"] + "/alto-annotation",
                "type": "Annotation",
                "motivation": "supplementing",
                "body": {
                    "type": "TextualBody",
                    "value": transcription,
                    "format": "text/plain",
                    "language": "fr"
                },
                "target": canvas["id"]
            }

            annotation_page["items"].append(annotation)

# Sauvegarder le nouveau manifeste enrichi
with open("manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("✅ Manifeste enrichi généré : manifest.json")
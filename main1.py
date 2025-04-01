# -*- coding: utf-8 -*-
"""Batch processing of receipts from a directory

Required libraries: mistralai, rapidfuzz, pandas
"""

# Installer les bibliothèques requises
#!pip install mistralai rapidfuzz pandas python-dotenv

import base64
import json
import os
import time
import re
import datetime
from pathlib import Path
import pandas as pd
from rapidfuzz import fuzz
from mistralai import Mistral
from dotenv import load_dotenv  # Importer dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
api_key = os.getenv("API_KEY")

# Vérifier si la clé API est chargée correctement
if not api_key:
    raise ValueError("La clé API n'est pas définie dans le fichier .env.")

# Initialiser le client Mistral avec la clé API
client = Mistral(api_key=api_key)
model = "pixtral-12b-2409"

# Fonction pour encoder l'image en base64
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# Fonction pour extraire les données du reçu
def extract_receipt_data(image_path, retries=3, delay=5):
    base64_img = encode_image(image_path)
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """Tu es un assistant intelligent. Lis ce reçu bancaire (image) et renvoie uniquement les informations suivantes dans un objet JSON clair avec les clés exactes suivantes :
{
  "date": "...",
  "amount": ...,
  "currency": "...",
  "vendor": "..."
}
Le champ 'amount' doit être un nombre (pas une chaîne)."""
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_img}"
                }
            ]
        }
    ]

    for attempt in range(1, retries + 1):
        try:
            print(f"🧠 Tentative {attempt} d’analyse OCR...")
            response = client.chat.complete(model=model, messages=messages)
            content = response.choices[0].message.content
            print("🔍 Réponse brute :", content)

            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                json_text = match.group(0)
                data = json.loads(json_text)

                # Normalisation de la date
                date_formats = [
                    "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y", "%d %b %Y", "%d %B %Y"
                ]
                for fmt in date_formats:
                    try:
                        parsed_date = datetime.datetime.strptime(data["date"], fmt)
                        data["date"] = parsed_date.strftime("%Y-%m-%d")
                        break
                    except Exception:
                        continue
                else:
                    print("Format de date non reconnu :", data["date"])

                return data
            else:
                raise ValueError("Aucun JSON valide trouvé dans la réponse.")

        except Exception as e:
            print(f"Échec tentative {attempt} : {e}")
            if attempt < retries:
                print(f"🔁 Nouvelle tentative dans {delay} secondes...")
                time.sleep(delay)
            else:
                print("Abandon après plusieurs échecs.")
                return None

# Fonction pour traiter un lot d'images dans un répertoire
def process_images_in_directory(directory_path, batch_size=10, delay=60):
    # Liste toutes les images dans le répertoire
    image_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    print(f"📁 Trouvé {len(image_paths)} images dans le répertoire '{directory_path}'.")

    results = []

    # Diviser les images en lots de batch_size (par défaut 10)
    for i in range(0, len(image_paths), batch_size):
        batch = image_paths[i:i+batch_size]
        print(f"🔄 Traitement du lot {i//batch_size + 1}...")

        # Traiter chaque image du lot
        for image_path in batch:
            print(f"📸 Traitement de l'image : {image_path}")
            result = extract_receipt_data(image_path)
            if result:
                results.append(result)
            else:
                print(f"❌ Aucune donnée extraite pour l'image {image_path}")

        # Sauvegarder les résultats après chaque lot
        if results:
            with open(f"recu_extrait_batch_{i//batch_size + 1}.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"✅ Fichier 'recu_extrait_batch_{i//batch_size + 1}.json' généré avec succès.")

        # Attendre le délai avant de traiter le prochain lot
        if i + batch_size < len(image_paths):
            print(f"⏳ Attente de {delay} secondes avant le traitement du prochain lot...")
            time.sleep(delay)

    return results

# Spécifie le chemin du répertoire contenant les images
directory_path = 'receipts'  # Change ce chemin par le répertoire contenant tes images

# Traiter les images par lots depuis le répertoire
results = process_images_in_directory(directory_path)

# Si des résultats ont été extraits, les afficher
if results:
    print("✅ Résultats extraits :")
    print(json.dumps(results, indent=2))
else:
    print("❌ Aucune donnée extraite.")

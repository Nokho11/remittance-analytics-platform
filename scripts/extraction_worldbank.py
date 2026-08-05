"""
EXTRACTION - Banque Mondiale (contexte annuel)
Poids des matieres premieres dans les exportations, par pays.
Sert a ponderer la dimension d'exposition (section 6 de la note).

Source : DBnomics (api.db.nomics.world), qui reprend les donnees
World Bank/WDI. Utilise ce chemin plutot que api.worldbank.org
directement, ce dernier etant inaccessible depuis certains reseaux.
"""

import os
import json
import requests

RAW_DIR = "raw/worldbank"
DBNOMICS_URL = "https://api.db.nomics.world/v22/series/WB/WDI"

os.makedirs(RAW_DIR, exist_ok=True)

# Pays ou les societes suivies (section 4 de la note) exploitent des sites
COUNTRIES = ["SEN", "GHA", "MLI", "CIV", "BFA", "GIN", "MRT", "NER", "NGA", "ZAF"]

# Poids des grandes categories de matieres premieres dans les exportations
INDICATORS = {
    "poids_export_agricole": "TX.VAL.AGRI.ZS.UN",
    "poids_export_energie": "TX.VAL.FUEL.ZS.UN",
    "poids_export_metaux": "TX.VAL.MMTL.ZS.UN",
}


def extract_indicator(nom, code):
    """Recupere un indicateur World Bank (dataset WDI) via DBnomics."""
    dimensions = json.dumps({"country": COUNTRIES, "indicator": [code]})
    params = {"dimensions": dimensions, "observations": 1, "format": "json"}

    try:
        response = requests.get(DBNOMICS_URL, params=params, timeout=(10, 60))
        response.raise_for_status()
        payload = response.json()
    except requests.exceptions.RequestException as e:
        print(f"[Banque Mondiale] ECHEC {nom} ({code}) : {e}")
        return None

    series = payload.get("series", {}).get("docs", [])
    if not series:
        print(f"[Banque Mondiale] Aucune donnee pour {nom} ({code})")
        return None

    out_path = f"{RAW_DIR}/{nom}.json"
    with open(out_path, "w") as f:
        json.dump(series, f, indent=2)
    print(f"[Banque Mondiale] {len(series)} series ({nom}) -> {out_path}")
    return series


if __name__ == "__main__":
    for nom, code in INDICATORS.items():
        extract_indicator(nom, code)
    print()
    print("Extraction Banque Mondiale terminee.")

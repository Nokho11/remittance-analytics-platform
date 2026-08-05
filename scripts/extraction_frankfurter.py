"""
EXTRACTION - Frankfurter (Banque Centrale Europeenne)
15 devises : ancrage fixe XOF, flottantes, references.
Source : API REST publique (aucune cle requise).

Ecrit dans raw/frankfurter/ :
- rates_du_jour.json    : taux du jour (extraction quotidienne, appelee par le DAG)
- dim_devise.json       : dimension devise clef en main (nom, symbole...)
- rates_historique.json : backfill ponctuel sur une plage de dates (--backfill)
"""

import os
import sys
import json
import requests

RAW_DIR = "raw/frankfurter"
RATES_URL = "https://api.frankfurter.dev/v2/rates"
CURRENCIES_URL = "https://api.frankfurter.dev/v2/currencies"
HISTORICAL_URL = "https://api.frankfurter.dev/v1"

os.makedirs(RAW_DIR, exist_ok=True)

DEVISES_FLOTTANTES = ["MRU", "NGN", "GHS", "GMD", "CVE"]
DEVISES_REFERENCE = ["USD", "GBP", "JPY", "CNY", "ZAR", "MAD", "EGP", "KES", "CAD"]
# CAD requis pour convertir l'instrument "endeavour" (cf. fact_cotation.sql) ;
# absent de la liste d'origine, ce qui faussait silencieusement sa conversion EUR.
# XOF = ancrage fixe a l'euro, inclus separement


def extract_rates():
    """Recupere les taux du jour, EUR vers les 14 devises suivies."""
    quotes = ["XOF"] + DEVISES_FLOTTANTES + DEVISES_REFERENCE
    params = {"base": "EUR", "quotes": ",".join(quotes)}

    response = requests.get(RATES_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    out_path = f"{RAW_DIR}/rates_du_jour.json"
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[Frankfurter] {len(data)} taux recuperes -> {out_path}")
    return data


def extract_currencies():
    """Recupere la dimension devise clef en main (nom, symbole, code ISO)."""
    response = requests.get(CURRENCIES_URL, timeout=30)
    response.raise_for_status()
    data = response.json()

    out_path = f"{RAW_DIR}/dim_devise.json"
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[Frankfurter] Dimension devise ({len(data)} devises) -> {out_path}")
    return data


def extract_historical(start_date, end_date):
    """Backfill ponctuel sur [start_date, end_date] (AAAA-MM-JJ), pour combler
    l'historique manquant a cause de l'ancien WRITE_TRUNCATE quotidien.

    L'endpoint historique (v1) ne couvre que les devises de reference ECB
    (USD, GBP, JPY, CNY, ZAR, CAD...) : XOF et les devises ouest-africaines
    flottantes (MRU, NGN, GHS, GMD, CVE), ainsi que MAD/EGP/KES, ne sont
    disponibles qu'en taux du jour via /v2/rates. Elles ne seront jamais
    backfillables sur cette API gratuite ; leur historique ne s'accumulera
    qu'a partir des extractions quotidiennes a venir.
    """
    quotes = ["XOF"] + DEVISES_FLOTTANTES + DEVISES_REFERENCE
    params = {"symbols": ",".join(quotes)}

    response = requests.get(f"{HISTORICAL_URL}/{start_date}..{end_date}", params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    records = [
        {"date": date, "base": data["base"], "quote": devise, "rate": taux}
        for date, taux_du_jour in data["rates"].items()
        for devise, taux in taux_du_jour.items()
    ]

    out_path = f"{RAW_DIR}/rates_historique.json"
    with open(out_path, "w") as f:
        json.dump(records, f, indent=2)
    devises_couvertes = sorted({r["quote"] for r in records})
    print(f"[Frankfurter] {len(records)} taux historiques ({start_date}..{end_date}) -> {out_path}")
    print(f"[Frankfurter] Devises couvertes par le backfill : {', '.join(devises_couvertes)}")
    manquantes = sorted(set(quotes) - set(devises_couvertes))
    if manquantes:
        print(f"[Frankfurter] Non backfillables (indisponibles en historique) : {', '.join(manquantes)}")
    return records


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--backfill":
        extract_historical(sys.argv[2], sys.argv[3])
    else:
        extract_rates()
        extract_currencies()
        print()
        print("Extraction Frankfurter terminee.")

"""
EXTRACTION - Yahoo Finance
41 instruments : matieres premieres, actions, indices.
Source : librairie yfinance (aucune cle requise).

Ecrit un fichier CSV par instrument dans raw/yfinance/.
"""

import os
import time
import yfinance as yf

RAW_DIR = "raw/yfinance"
os.makedirs(RAW_DIR, exist_ok=True)

INSTRUMENTS = {
    # Matieres premieres - Agricoles
    "cacao": "CC=F", "cafe": "KC=F", "sucre": "SB=F",
    "coton": "CT=F", "jus_orange": "OJ=F",
    # Matieres premieres - Cereales
    "ble": "ZW=F", "mais": "ZC=F", "soja": "ZS=F",
    "riz": "ZR=F", "avoine": "ZO=F",
    # Matieres premieres - Energie
    "brent": "BZ=F", "wti": "CL=F", "gaz_naturel": "NG=F",
    "essence": "RB=F", "fioul": "HO=F",
    # Matieres premieres - Metaux precieux
    "or": "GC=F", "argent": "SI=F", "platine": "PL=F", "palladium": "PA=F",
    # Matieres premieres - Metaux industriels
    "cuivre": "HG=F", "minerai_fer": "TIO=F", "aluminium": "ALI=F",
    # Matieres premieres - Elevage
    "bovins": "LE=F",
    # Actions - Hydrocarbures
    "kosmos": "KOS", "bp": "BP", "woodside": "WDS",
    "totalenergies": "TTE", "shell": "SHEL", "exxon": "XOM",
    # Actions - Mines
    "kinross": "KGC", "endeavour": "EDV.TO", "barrick": "GOLD",
    "newmont": "NEM", "glencore": "GLEN.L", "anglo_american": "AGL.JO",
    # Actions - Telecoms
    "orange_sa": "ORA.PA",
    # Indices
    "sp500": "^GSPC", "cac40": "^FCHI", "ftse100": "^FTSE",
    "nikkei": "^N225", "vix": "^VIX",
}


def extract_instrument(nom, ticker):
    """Recupere l'historique quotidien d'un instrument (10 derniers jours)."""
    try:
        data = yf.Ticker(ticker).history(period="10d", interval="1d")
    except Exception as e:
        print(f"[Yahoo Finance] ECHEC {nom} ({ticker}) : {e}")
        return None

    if data.empty:
        print(f"[Yahoo Finance] Aucune donnee pour {nom} ({ticker})")
        return None

    out_path = f"{RAW_DIR}/{nom}.csv"
    data.to_csv(out_path)
    print(f"[Yahoo Finance] {len(data)} lignes ({nom} / {ticker}) -> {out_path}")
    return data


if __name__ == "__main__":
    echecs = []
    for nom, ticker in INSTRUMENTS.items():
        if extract_instrument(nom, ticker) is None:
            echecs.append((nom, ticker))
        time.sleep(0.5)  # eviter de surcharger l'API

    print()
    print(f"Termine : {len(INSTRUMENTS) - len(echecs)}/{len(INSTRUMENTS)} instruments recuperes.")
    if echecs:
        print("Echecs :", echecs)

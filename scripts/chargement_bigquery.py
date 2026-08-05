"""
CHARGEMENT - raw/ vers BigQuery
Copie les fichiers extraits (CSV et JSON) vers le dataset "raw"
de BigQuery, tels quels, sans transformation (regle d'or du projet).

Avant de lancer ce script :
1. Le fichier de cle JSON du compte de service doit exister sur ton Mac
2. Copie .env.example en .env a la racine du repo et adapte si besoin
   (par defaut, pointe vers ~/.gcp/remittance-analytics-platform-sa.json)
"""

import os
import json
import glob
import pandas as pd
from google.cloud import bigquery

CREDENTIALS_PATH = os.environ.get(
    "REMITTANCE_KEYFILE",
    os.path.expanduser("~/.gcp/remittance-analytics-platform-sa.json"),
)
PROJECT_ID = os.environ.get("REMITTANCE_PROJECT", "remittance-analytics-platform")
DATASET = "raw"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
client = bigquery.Client(project=PROJECT_ID)


def load_csv_folder(folder, table_prefix):
    """Charge tous les CSV d'un dossier, un fichier = une table BigQuery."""
    for filepath in glob.glob(f"{folder}/*.csv"):
        nom_fichier = os.path.splitext(os.path.basename(filepath))[0]
        table_id = f"{PROJECT_ID}.{DATASET}.{table_prefix}_{nom_fichier}"

        df = pd.read_csv(filepath)
        job = client.load_table_from_dataframe(
            df, table_id,
            job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"),
        )
        job.result()  # attend la fin du chargement
        print(f"[BigQuery] {len(df)} lignes -> {table_id}")


def load_frankfurter(folder):
    """Charge le dossier Frankfurter : dim_devise.json est une photo (WRITE_TRUNCATE,
    toujours l'etat courant), rates_du_jour.json et l'eventuel backfill
    rates_historique.json s'accumulent dans la meme table (WRITE_APPEND). Avant, tout
    etait en WRITE_TRUNCATE : le taux du jour precedent etait perdu a chaque run, donc
    fact_cotation ne pouvait convertir en EUR que la cotation du jour meme."""
    dim_path = f"{folder}/dim_devise.json"
    if os.path.exists(dim_path):
        table_id = f"{PROJECT_ID}.{DATASET}.frankfurter_dim_devise"
        df = pd.read_json(dim_path)
        job = client.load_table_from_dataframe(
            df, table_id,
            job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"),
        )
        job.result()
        print(f"[BigQuery] {len(df)} lignes -> {table_id}")

    table_id = f"{PROJECT_ID}.{DATASET}.frankfurter_rates_du_jour"
    for nom_fichier in ("rates_historique.json", "rates_du_jour.json"):
        filepath = f"{folder}/{nom_fichier}"
        if not os.path.exists(filepath):
            continue
        df = pd.read_json(filepath)
        job = client.load_table_from_dataframe(
            df, table_id,
            job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND"),
        )
        job.result()
        print(f"[BigQuery] {len(df)} lignes -> {table_id} (append)")


def load_json_folder_as_raw_string(folder, table_prefix):
    """Charge des JSON a structure imbriquee (listes, types mixtes) en gardant
    chaque element tel quel dans une colonne texte, plutot que d'essayer de
    l'aplatir (ce qui echoue si les types ne sont pas homogenes). C'est dbt
    qui decomposera ce JSON proprement a l'etape suivante."""
    for filepath in glob.glob(f"{folder}/*.json"):
        nom_fichier = os.path.splitext(os.path.basename(filepath))[0]
        table_id = f"{PROJECT_ID}.{DATASET}.{table_prefix}_{nom_fichier}"

        with open(filepath) as f:
            elements = json.load(f)

        df = pd.DataFrame({"raw_json": [json.dumps(e) for e in elements]})
        job = client.load_table_from_dataframe(
            df, table_id,
            job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"),
        )
        job.result()
        print(f"[BigQuery] {len(df)} lignes (JSON brut) -> {table_id}")


if __name__ == "__main__":
    print("Chargement yfinance...")
    load_csv_folder("raw/yfinance", "yfinance")

    print()
    print("Chargement Frankfurter...")
    load_frankfurter("raw/frankfurter")

    print()
    print("Chargement Banque Mondiale...")
    load_json_folder_as_raw_string("raw/worldbank", "worldbank")

    print()
    print("Chargement termine.")

# remittance-analytics-platform

Pipeline de cotations de marché (matières premières, actions, indices) avec conversion EUR, et suivi de 15 devises (dont l'ancrage XOF) via Frankfurter/BCE.

```
Yahoo Finance   ┐
Frankfurter     ├─► Airflow ─► BigQuery.raw ─► dbt ─► BigQuery.marts
Banque Mondiale ┘
```

## Structure

- `airflow/dags/pipeline_marches.py` — DAG (extraction → chargement BigQuery → dbt run/test), planifié 7h en semaine
- `scripts/` — extraction (Yahoo Finance, Frankfurter, Banque Mondiale) et chargement vers `BigQuery.raw`
- `dbt_pipeline/` — modèles dbt (`raw` → `marts`), profil `pipeline_marches`

## Config

```bash
cp .env.example .env   # adapter REMITTANCE_KEYFILE si besoin
```

Le compte de service doit avoir accès au projet GCP `remittance-analytics-platform` (BigQuery). Le projet tourne actuellement en mode sandbox (facturation désactivée) : pas de DML/MERGE, tables inactives supprimées après 60 jours.

## Lancer

```bash
cd scripts && python3 extraction_yfinance.py && python3 extraction_frankfurter.py && python3 extraction_worldbank.py && python3 chargement_bigquery.py
cd ../dbt_pipeline && dbt run && dbt test
```

## Notes

- `scripts/extraction_frankfurter.py --backfill AAAA-MM-JJ AAAA-MM-JJ` : backfill ponctuel de l'historique des taux de change (endpoint Frankfurter v1). Ne couvre que les devises de référence ECB (USD, GBP, JPY, CNY, ZAR, CAD...) — XOF et les devises ouest-africaines flottantes (MRU, NGN, GHS, GMD, CVE), ainsi que MAD/EGP/KES, ne sont disponibles qu'en taux du jour et ne peuvent pas être backfillées sur l'API gratuite.
- `raw.frankfurter_rates_du_jour` s'accumule en `WRITE_APPEND` (historique des taux) ; `raw.frankfurter_dim_devise` reste en `WRITE_TRUNCATE` (dimension, toujours l'état courant).

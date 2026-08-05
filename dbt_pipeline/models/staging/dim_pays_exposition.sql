select
    pays,
    categorie,
    annee as derniere_annee_disponible,
    valeur as poids_export
from {{ ref('stg_worldbank_all') }}
where valeur is not null
qualify row_number() over (
    partition by pays, categorie
    order by annee desc
) = 1
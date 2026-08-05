{% set categories = ['agricole', 'energie', 'metaux'] %}

with
{% for categorie in categories %}
base_{{ categorie }} as (
    select
        JSON_EXTRACT_SCALAR(raw_json, '$.dimensions.country') as pays,
        JSON_EXTRACT_SCALAR(raw_json, '$.dimensions.indicator') as indicateur,
        '{{ categorie }}' as categorie,
        JSON_EXTRACT_ARRAY(raw_json, '$.period') as annees,
        JSON_EXTRACT_ARRAY(raw_json, '$.value') as valeurs
    from {{ source('raw', 'worldbank_poids_export_' ~ categorie) }}
){% if not loop.last %},{% endif %}
{% endfor %}

{% for categorie in categories %}
select
    pays,
    indicateur,
    categorie,
    cast(JSON_EXTRACT_SCALAR(annee) as int64) as annee,
    safe_cast(JSON_EXTRACT_SCALAR(valeur) as float64) as valeur
from base_{{ categorie }},
    unnest(annees) as annee with offset pos1,
    unnest(valeurs) as valeur with offset pos2
where pos1 = pos2
{% if not loop.last %}union all{% endif %}
{% endfor %}
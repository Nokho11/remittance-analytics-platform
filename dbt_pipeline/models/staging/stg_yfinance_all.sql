{% set instruments = [
    'or', 'argent', 'platine', 'palladium', 'cuivre', 'minerai_fer', 'aluminium',
    'cacao', 'cafe', 'sucre', 'coton', 'jus_orange',
    'ble', 'mais', 'soja', 'riz', 'avoine',
    'brent', 'wti', 'gaz_naturel', 'essence', 'fioul',
    'bovins',
    'kosmos', 'bp', 'woodside', 'totalenergies', 'shell', 'exxon',
    'kinross', 'endeavour', 'barrick', 'newmont', 'glencore', 'anglo_american',
    'orange_sa',
    'sp500', 'cac40', 'ftse100', 'nikkei', 'vix'
] %}

{% for instrument in instruments %}
select
    date(timestamp(Date)) as date_cotation,
    '{{ instrument }}' as instrument,
    Open as ouverture,
    High as plus_haut,
    Low as plus_bas,
    Close as cloture,
    Volume as volume
from {{ source('raw', 'yfinance_' ~ instrument) }}
{% if not loop.last %}union all{% endif %}
{% endfor %}
-- distinct : la table raw s'accumule desormais en WRITE_APPEND, donc une relance du
-- DAG le meme jour peut deposer deux fois le meme (date, devise) avec le meme taux.
select distinct
    date as date_cotation,
    base as devise_base,
    quote as devise_cible,
    rate as taux_change
from {{ source('raw', 'frankfurter_rates_du_jour') }}
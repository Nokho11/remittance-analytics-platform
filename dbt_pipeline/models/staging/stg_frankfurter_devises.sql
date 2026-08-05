select
    iso_code as code_devise,
    name as nom_devise,
    symbol as symbole_devise
from {{ source('raw', 'frankfurter_dim_devise') }}
select
    code_devise,
    nom_devise,
    symbole_devise
from {{ ref('stg_frankfurter_devises') }}
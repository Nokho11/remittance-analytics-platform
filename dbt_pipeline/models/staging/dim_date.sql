select
    date_jour,
    extract(year from date_jour) as annee,
    extract(month from date_jour) as mois,
    extract(quarter from date_jour) as trimestre,
    extract(dayofweek from date_jour) as jour_semaine,
    format_date('%B', date_jour) as nom_mois
from unnest(
    generate_date_array('2015-01-01', current_date(), interval 1 day)
) as date_jour
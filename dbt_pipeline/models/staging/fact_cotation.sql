with devise_par_instrument as (
    select * from unnest([
        struct('glencore' as instrument, 'GBP' as devise, 100 as diviseur),
        struct('anglo_american' as instrument, 'ZAR' as devise, 100 as diviseur),
        struct('endeavour' as instrument, 'CAD' as devise, 1 as diviseur),
        struct('orange_sa' as instrument, 'EUR' as devise, 1 as diviseur),
        struct('totalenergies' as instrument, 'EUR' as devise, 1 as diviseur),
        struct('cac40' as instrument, 'EUR' as devise, 1 as diviseur),
        struct('ftse100' as instrument, 'GBP' as devise, 1 as diviseur),
        struct('nikkei' as instrument, 'JPY' as devise, 1 as diviseur)
    ])
),

cotations as (
    select
        c.date_cotation,
        c.instrument,
        coalesce(dpi.devise, 'USD') as devise_cotation,
        coalesce(dpi.diviseur, 1) as diviseur,
        c.ouverture,
        c.plus_haut,
        c.plus_bas,
        c.cloture,
        c.volume
    from {{ ref('stg_yfinance_all') }} c
    left join devise_par_instrument dpi
        on c.instrument = dpi.instrument
),

-- taux le plus recent <= date_cotation : stg_frankfurter_rates ne garde qu'un
-- instantane (raw.frankfurter_rates_du_jour est ecrase chaque jour), une egalite
-- stricte sur la date ne matchait donc quasiment jamais et retombait sur le
-- taux par defaut de 1, faussant silencieusement cloture_eur. BigQuery n'autorise
-- pas de sous-requete correlee sur une inegalite, d'ou ce join + fenetre.
fx_asof as (
    select
        besoin.date_cotation,
        besoin.devise_cotation,
        fx.taux_change,
        row_number() over (
            partition by besoin.date_cotation, besoin.devise_cotation
            order by fx.date_cotation desc
        ) as rn
    from (select distinct date_cotation, devise_cotation from cotations) besoin
    left join {{ ref('stg_frankfurter_rates') }} fx
        on fx.devise_cible = besoin.devise_cotation
        and fx.date_cotation <= besoin.date_cotation
    qualify rn = 1
)

select
    c.date_cotation,
    c.instrument,
    c.devise_cotation,
    c.ouverture,
    c.plus_haut,
    c.plus_bas,
    c.cloture,
    c.volume,
    (c.cloture / c.diviseur) / coalesce(fx.taux_change, 1) as cloture_eur
from cotations c
left join fx_asof fx
    on fx.date_cotation = c.date_cotation
    and fx.devise_cotation = c.devise_cotation
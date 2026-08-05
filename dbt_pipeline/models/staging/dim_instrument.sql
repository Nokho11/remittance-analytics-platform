select
    instrument,
    categorie,
    sous_categorie
from unnest([
    struct('cacao' as instrument, 'matiere_premiere' as categorie, 'agricole' as sous_categorie),
    struct('cafe' as instrument, 'matiere_premiere' as categorie, 'agricole' as sous_categorie),
    struct('sucre' as instrument, 'matiere_premiere' as categorie, 'agricole' as sous_categorie),
    struct('coton' as instrument, 'matiere_premiere' as categorie, 'agricole' as sous_categorie),
    struct('jus_orange' as instrument, 'matiere_premiere' as categorie, 'agricole' as sous_categorie),

    struct('ble' as instrument, 'matiere_premiere' as categorie, 'cereale' as sous_categorie),
    struct('mais' as instrument, 'matiere_premiere' as categorie, 'cereale' as sous_categorie),
    struct('soja' as instrument, 'matiere_premiere' as categorie, 'cereale' as sous_categorie),
    struct('riz' as instrument, 'matiere_premiere' as categorie, 'cereale' as sous_categorie),
    struct('avoine' as instrument, 'matiere_premiere' as categorie, 'cereale' as sous_categorie),

    struct('brent' as instrument, 'matiere_premiere' as categorie, 'energie' as sous_categorie),
    struct('wti' as instrument, 'matiere_premiere' as categorie, 'energie' as sous_categorie),
    struct('gaz_naturel' as instrument, 'matiere_premiere' as categorie, 'energie' as sous_categorie),
    struct('essence' as instrument, 'matiere_premiere' as categorie, 'energie' as sous_categorie),
    struct('fioul' as instrument, 'matiere_premiere' as categorie, 'energie' as sous_categorie),

    struct('or' as instrument, 'matiere_premiere' as categorie, 'metal_precieux' as sous_categorie),
    struct('argent' as instrument, 'matiere_premiere' as categorie, 'metal_precieux' as sous_categorie),
    struct('platine' as instrument, 'matiere_premiere' as categorie, 'metal_precieux' as sous_categorie),
    struct('palladium' as instrument, 'matiere_premiere' as categorie, 'metal_precieux' as sous_categorie),

    struct('cuivre' as instrument, 'matiere_premiere' as categorie, 'metal_industriel' as sous_categorie),
    struct('minerai_fer' as instrument, 'matiere_premiere' as categorie, 'metal_industriel' as sous_categorie),
    struct('aluminium' as instrument, 'matiere_premiere' as categorie, 'metal_industriel' as sous_categorie),

    struct('bovins' as instrument, 'matiere_premiere' as categorie, 'elevage' as sous_categorie),

    struct('kosmos' as instrument, 'action' as categorie, 'hydrocarbure' as sous_categorie),
    struct('bp' as instrument, 'action' as categorie, 'hydrocarbure' as sous_categorie),
    struct('woodside' as instrument, 'action' as categorie, 'hydrocarbure' as sous_categorie),
    struct('totalenergies' as instrument, 'action' as categorie, 'hydrocarbure' as sous_categorie),
    struct('shell' as instrument, 'action' as categorie, 'hydrocarbure' as sous_categorie),
    struct('exxon' as instrument, 'action' as categorie, 'hydrocarbure' as sous_categorie),

    struct('kinross' as instrument, 'action' as categorie, 'mine' as sous_categorie),
    struct('endeavour' as instrument, 'action' as categorie, 'mine' as sous_categorie),
    struct('barrick' as instrument, 'action' as categorie, 'mine' as sous_categorie),
    struct('newmont' as instrument, 'action' as categorie, 'mine' as sous_categorie),
    struct('glencore' as instrument, 'action' as categorie, 'mine' as sous_categorie),
    struct('anglo_american' as instrument, 'action' as categorie, 'mine' as sous_categorie),

    struct('orange_sa' as instrument, 'action' as categorie, 'telecom' as sous_categorie),

    struct('sp500' as instrument, 'indice' as categorie, 'indice' as sous_categorie),
    struct('cac40' as instrument, 'indice' as categorie, 'indice' as sous_categorie),
    struct('ftse100' as instrument, 'indice' as categorie, 'indice' as sous_categorie),
    struct('nikkei' as instrument, 'indice' as categorie, 'indice' as sous_categorie),
    struct('vix' as instrument, 'indice' as categorie, 'indice' as sous_categorie)
])
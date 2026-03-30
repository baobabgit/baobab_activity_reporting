"""Module des identifiants de schéma pour les données consolidées."""


class ConsolidatedDataSchema:
    """Noms de sources préparées et colonnes canoniques attendues.

    Centralise les libellés utilisés par les extracteurs CSV et les
    pipelines de standardisation afin d'aligner le calcul des KPI.

    :Example:
        >>> ConsolidatedDataSchema.SOURCE_INCOMING_CALLS
        'appels_entrants'
    """

    SOURCE_INCOMING_CALLS: str = "appels_entrants"
    SOURCE_OUTGOING_CALLS: str = "appels_sortants"
    SOURCE_TICKETS: str = "tickets"

    COL_DATE: str = "Date"
    COL_TIME: str = "Heure"
    COL_AGENT: str = "Agent"
    COL_SITE: str = "Site"
    COL_DURATION: str = "Durée"
    COL_STATUS: str = "Statut"
    COL_DESTINATION: str = "Destination"
    COL_CHANNEL: str = "Canal"
    COL_CATEGORY: str = "Catégorie"

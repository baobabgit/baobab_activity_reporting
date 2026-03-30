# Chaîne complète : import → KPI → rapport

Ce document décrit l’enchaînement **import des sources**, **calcul des
indicateurs** et **génération éditoriale** avec la façade
`ReportingService` ou la CLI `baobab-reporting`.

## Prérequis

- Python 3.10+
- Fichiers CSV alignés avec les extracteurs (entrants, sortants, tickets) ;
  voir les en-têtes des fichiers dans `tests/fixtures/`.
- Une base SQLite (fichier ou `:memory:`) : le schéma est créé à l’ouverture.

## Ordre des opérations

1. **Import** — lecture CSV, enregistrement en `raw_data` et `prepared_data`
   (clés `appels_entrants`, `appels_sortants`, `tickets`). Le contenu précédent
   pour chaque clé est remplacé.
2. **Calcul** — `KpiComputationPipeline` filtre sur la période, calcule les KPI
   et les insère dans `kpi_data`. Option `--clear-period` (CLI) ou
   `clear_existing_for_period=True` pour éviter les doublons sur une rejoue.
3. **Génération** — chargement des KPI dont `period_start` / `period_end`
   correspondent à la période du rapport, construction du `ReportModel` puis
   export Markdown et/ou DOCX si des chemins sont fournis.

Les bornes de période du rapport doivent **cohérentes** avec celles utilisées
lors du calcul (mêmes dates ISO que dans `kpi_data`).

## Exemple Python

```python
from datetime import date

from baobab_activity_reporting import (
    ReportDefinition,
    ReportingPeriod,
    ReportingService,
)

svc = ReportingService("mon_rapport.db")
try:
    svc.import_sources(
        "chemin/vers/incoming.csv",
        "chemin/vers/outgoing.csv",
        "chemin/vers/tickets.csv",
    )
    period = ReportingPeriod(date(2026, 3, 1), date(2026, 3, 31))
    svc.compute_metrics(period, clear_existing_for_period=True)
    svc.generate_report(
        period,
        ReportDefinition.activity_telephony(),
        markdown_path="sortie.md",
    )
finally:
    svc.close()
```

## Exemple CLI

Voir la section « Interface en ligne de commande » du `README.md`. Les
sous-commandes acceptent `--log-level` et impriment un résumé JSON sur la sortie
standard.

## Types de rapport (`--report-type`)

| Valeur               | Fabrique `ReportDefinition`   |
|----------------------|-------------------------------|
| `activity_telephony` | Synthèse téléphonie + canaux  |
| `activity_by_site` | Indicateurs par site          |
| `activity_by_agent`| Indicateurs par agent         |

Toute autre valeur lève une `ConfigurationException` (résolveur
`resolve_report_definition`).

# Types de rapports planifiables

Les gabarits sont fournis par la classe ``ReportDefinition`` (fabriques de
classe). Chaque type définit un titre (modèle avec ``{period_start}`` et
``{period_end}``) et des sections ordonnées avec prérequis KPI.

## `activity_telephony`

Rapport synthèse **téléphonie** et **canaux de tickets** sur la période.

| Section | Code | Prérequis (préfixes KPI) |
|---------|------|--------------------------|
| Synthèse téléphonique | `telephony_overview` | `telephony.` |
| Répartition tickets par canal | `ticket_channels` | `tickets.channel.` |

Les sections sans donnée correspondante sont **exclues** automatiquement du plan.

## `activity_by_site`

Une section agrégée **par site** : `site_breakdown`, prérequis `site.`.

## `activity_by_agent`

Une section **par agent** : `agent_breakdown`, prérequis `agent.`.

## Modèle produit

La classe ``ReportModel`` contient :

- un titre formaté, les bornes de période ;
- des narratifs liminaires ;
- pour chaque section retenue : titres, blocs narratifs, tableaux sémantiques
  (`headers` / `rows`), insights métier, statut d'éligibilité.

Ce modèle est **indépendant** de tout format DOCX, Markdown ou HTML ; les writers
ultérieurs consommeront ``ReportModel.to_document_tree()``.

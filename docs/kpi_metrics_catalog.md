# Catalogue des KPI produits par le pipeline de calcul

Les codes ci-dessous sont persistés dans `kpi_data` avec les bornes de période
(`period_start`, `period_end`) et, le cas échéant, les dimensions `site`,
`agent`, `channel`.

## Téléphonie (période globale)

| Code | Description |
|------|-------------|
| `telephony.incoming.count` | Nombre d'appels entrants |
| `telephony.outgoing.count` | Nombre d'appels sortants |
| `telephony.incoming.duration_seconds.sum` | Somme des durées entrantes (s) |
| `telephony.outgoing.duration_seconds.sum` | Somme des durées sortantes (s) |
| `telephony.incoming.duration_seconds.avg` | Durée moyenne entrante (s) |
| `telephony.outgoing.duration_seconds.avg` | Durée moyenne sortante (s) |

## Par site

| Modèle de code | Description |
|----------------|-------------|
| `site.<libellé>.telephony.incoming.*` | Compteurs et durées entrants par site |
| `site.<libellé>.telephony.outgoing.*` | Compteurs et durées sortants par site |
| `site.<libellé>.tickets.by_channel.<canal>.count` | Tickets par canal et par site |

## Par agent

| Modèle de code | Description |
|----------------|-------------|
| `agent.<id>.telephony.incoming.*` | Métriques téléphoniques entrantes par agent |
| `agent.<id>.telephony.outgoing.*` | Métriques téléphoniques sortantes par agent |
| `agent.<id>.tickets.count` | Nombre de tickets par agent |

## Canaux de tickets (période globale)

| Modèle de code | Description |
|----------------|-------------|
| `tickets.channel.<libellé>.count` | Volume par canal (ex. EFI, EDI) sur la période |

Les libellés de site et d'agent proviennent des colonnes normalisées
(`Site`, `Agent`) ; les canaux de la colonne `Canal` des tickets.

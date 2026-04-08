# Feature 11 — Définitions éditoriales de rapport et rapports hebdomadaires

## Identifiant

`11_editorial_report_definitions`

## Objectif

Remplacer les définitions de rapport limitées au triplet `(code, titre, préfixes KPI)` par un **modèle éditorial** capable de porter objectif rédactionnel, jeux de données attendus, règles d’affichage, style et politique de tableaux, tout en conservant une intégration fluide avec le planificateur et le constructeur existants.

## Choix de modélisation

### `EditorialSectionDefinition`

Une section est décrite par une dataclass immuable (`frozen=True`, `slots=True`) avec :

- **`section_code`** / **`section_title`** : identifiants stables pour le moteur et l’affichage.
- **`section_objective`** : intention rédactionnelle ; consommée par `NarrativeBuilder` pour introduire la section.
- **`required_data`** / **`optional_data`** : libellés sémantiques de « fentes » de données (documentation et évolution future) ; le filtrage effectif des KPI reste piloté par **`SectionVisibilityRule`** et les préfixes KPI.
- **`display_rules`** : par exemple affichage ou non des tableaux de métriques (`show_metric_tables`).
- **`writing_style`** : ton, personne, verbosité — porteur pour des évolutions du narratif.
- **`visibility_rule`** : `kpi_prefixes` + `mandatory_in_report`. Préfixes vides ⇒ section toujours éligible ; données absentes + obligatoire ⇒ section **dégradée** (conservée, KPI vides, message explicite) ; sinon **exclue**.
- **`table_policy`** : tri, nombre max de lignes, dimensions optionnelles pour `TableBuilder`.

La validation minimale (code et titre non vides) lève `ReportGenerationError`, cohérent avec les erreurs de génération existantes.

### `ReportDefinition`

- Champ principal **`editorial_sections`** : tuple ordonné de `EditorialSectionDefinition`.
- La propriété **`sections`** conserve une vue **legacy** `(code, titre, frozenset préfixes)` pour les appels qui s’appuient encore sur l’ancien contrat.
- Les rapports historiques sont adaptés via **`_editorial_from_legacy`** (objectif vide, règles par défaut).
- Les fabriques **`weekly_activity_by_agent`** et **`weekly_activity_by_site`** chargent des modules dédiés via **`importlib`** pour éviter les imports circulaires et les lignes trop longues ; le typage est assuré par **`cast(ReportDefinition, …)`** après construction.

### Plan commun hebdomadaire (six sections)

1. Synthèse hebdomadaire (`weekly_synthesis`)
2. Activité téléphonique (`weekly_telephony`)
3. Activité de traitement (`weekly_ticket_processing`)
4. **Agent** : contribution de l’agent (`weekly_agent_contribution`) — **Site** : répartition de la charge (`weekly_site_workload`)
5. Points d’attention (`weekly_attention_points`)
6. Conclusion (`weekly_conclusion`, tableaux désactivés via `DisplayRules`)

### Intégration

- **`SectionEligibilityEvaluator.evaluate_editorial_section`** : règles obligatoire / conditionnelle / retrait.
- **`ReportPlanner`** : itère les sections éditoriales et produit des décisions typées.
- **`ReportBuilder`** : narratif d’introduction à partir de l’objectif, KPI filtrés selon le statut (dégradé ⇒ liste vide), insights regroupés par familles de codes (constantes module `_INSIGHT_*` pour limiter la complexité pylint).

## Fichiers principaux

- `src/baobab_activity_reporting/reporting/editorial/` — un type par fichier.
- `weekly_activity_by_agent_report_definition.py`, `weekly_activity_by_site_report_definition.py`.
- Tests miroir sous `tests/baobab_activity_reporting/reporting/editorial/` et tests d’intégration plan / builder.

## Critères de done

- `black`, `pylint`, `mypy`, `flake8`, `bandit` (`-c pyproject.toml`), `pytest` avec couverture ≥ 90 %.

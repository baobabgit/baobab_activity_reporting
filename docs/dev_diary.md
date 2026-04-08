# Journal de développement — baobab-activity-reporting

## 2026-04-07 20:00:00

### Modifications

- Package ``reporting/presentation/`` : ``DurationFormatter``, ``VolumeFormatter``,
  ``PercentageFormatter``, ``BusinessNumericRounding``, ``TechnicalLabelSanitizer``,
  ``DimensionAnomalyChecker``, ``KpiValuePresentationFormatter``,
  ``SectionKpiTableProjector``.
- ``TableLayoutKind``, ``TablePolicy`` enrichie (``layout_kind``, ``max_rows`` par
  défaut) ; ``TableBuilder`` / ``ReportBuilder`` branchés sur la projection et le
  formatage métier ; définitions hebdo agent/site avec politiques par section.
- Tests unitaires miroir sous ``tests/.../presentation/`` ; scénarios
  ``test_report_builder`` / ``test_table_builder`` (alertes ``[Données]``,
  ventilation site).

### Buts

- Rendre les rapports lisibles : durées humaines, pas de codes KPI en tableau,
  tableaux courts et omis s’ils n’apportent pas de lecture ; signaler les
  dimensions manquantes ou placeholders.

### Impact

- Writers inchangés sur le principe : la couche présentation prépare déjà textes
  et lignes de tableau métier.

## 2026-04-08 01:00:00

### Modifications

- Éligibilité des sections : garde-fous métier (téléphonie entrée/sortie, volumes
  tickets canaux, ventilation agent/site ≥ 2 entités, signaux vigilance avec
  seuils, conclusion conditionnée aux sections exploitables).
- Nouveaux types ``SectionEligibilityDetail``, ``SectionAttentionAssessment``,
  ``SectionEligibilityCodes`` ; ``SectionDecision.detail`` optionnel.
- Classes dédiées : ``KpiValueAssessor``, portes téléphonie / tickets / breakdown,
  ``SectionAttentionSignalAnalyzer``, ``ExploitableSectionCatalog``.
- ``ReportPlanner`` : évaluation de ``weekly_conclusion`` après les autres
  sections avec ``peer_exploitable_included``.
- ``ReportBuilder`` : champs ``eligibility_signals`` / ``eligibility_notes`` si
  détail présent.
- Tests miroir et scénarios ``test_section_eligibility_hardening``.

### Buts

- Ne plus inclure une section sur la seule présence d'un code KPI : exiger des
  données minimales exploitables et des signaux réels pour la vigilance.

### Impact

- Rapports hebdo sans KPI : synthèse seule, sans conclusion ; rapports site/agent
  nécessitent deux sites/agents pour la répartition.

## 2026-04-07 23:30:00

### Modifications

- Package ``reporting/editorial/`` : ``DisplayRules``, ``TablePolicy``, ``WritingStyle``,
  ``SectionVisibilityRule``, ``EditorialSectionDefinition`` (validation via
  ``ReportGenerationError``).
- ``ReportDefinition`` : ``editorial_sections``, propriété legacy ``sections``,
  adaptation ``_editorial_from_legacy``, fabriques ``weekly_activity_by_agent`` /
  ``weekly_activity_by_site`` (chargement dynamique pour éviter les cycles).
- Rapports hebdo agent / site : plan en six sections (synthèse, téléphonie,
  traitement, contribution ou charge, points d’attention, conclusion).
- ``SectionEligibilityEvaluator.evaluate_editorial_section`` ; ``ReportPlanner`` et
  ``ReportBuilder`` branchés sur le modèle éditorial ; ``NarrativeBuilder`` et
  ``TableBuilder`` enrichis (objectif, ``table_policy``).
- Résolution CLI / ``resolve_report_definition`` pour les nouveaux types.
- Tests unitaires miroir et note ``docs/features/11_editorial_report_definitions.md``.

### Buts

- Ne plus se limiter à un export d’indicateurs : porter un plan éditorial
  normalisé et des métadonnées rédactionnelles exploitables par le pipeline.

### Impact

- Compatibilité conservée pour les définitions existantes via la vue legacy et
  les valeurs par défaut des champs éditoriaux.

## 2026-03-30 22:00:00

### Modifications

- Sous-packages ``application/`` (cas d'usage import, calcul KPI, génération)
  et ``cli/`` (argparse, JSON stdout) ; script d'entrée ``baobab-reporting``.
- ``ReportingService`` compose les use cases sur une ``DatabaseSessionManager``.
- ``KpiRepository.load_for_period`` ; ``BaseExtractor.load_dataframe`` et
  ``extraction_result_from_dataframe`` pour l'import sans relecture du fichier.
- Documentation ``docs/end_to_end_pipeline.md`` ; README (façade + CLI) ;
  version 0.9.0.

### Buts

- Exposer le moteur existant par des intentions métier explicites et une CLI
  opérationnelle, sans API HTTP.

### Impact

- Parcours bout-en-bout documenté ; les règles métier restent dans les couches
  domaine / processing / reporting — les use cases orchestrent seulement.

## 2026-03-30 20:00:00

### Modifications

- Sous-package ``reporting/writers/`` : ``AbstractWriter`` (contrat),
  ``DocxWriter`` (python-docx : titres, paragraphes, tableaux, puces),
  ``MarkdownWriter`` (GFM, UTF-8).
- Encapsulation des erreurs dans ``WriterError`` ; aucune logique KPI ni
  planification dans les writers.
- Dépendance ``python-docx`` ; configuration mypy ``ignore_missing_imports``
  pour le module ``docx``.
- Documentation ``docs/document_writers.md``, README et CHANGELOG ; version
  0.8.0.

### Buts

- Rendre le ``ReportModel`` exploitable en DOCX et Markdown de façon
  interchangeable.

### Impact

- Le pipeline peut enchaîner ``ReportBuilder`` puis un writer sans dupliquer
  la sémantique métier.

## 2026-03-30 18:00:00

### Modifications

- Sous-package `reporting/` : définitions de rapport (`ReportDefinition`),
  contexte KPI + période (`ReportContext`), évaluation d'éligibilité des
  sections (`SectionEligibilityEvaluator`, réutilise `SectionDecision`),
  planification (`ReportPlanner`), construction de narratifs, tableaux et
  insights (`NarrativeBuilder`, `TableBuilder`, `InsightBuilder`),
  orchestrateur `ReportBuilder`, livrable `ReportModel` avec export
  `to_document_tree()` sans dépendance au format documentaire.
- Erreurs via `ReportGenerationError` lorsque aucune section n'est éligible.
- Documentation `docs/report_types.md` ; exports racine du package.
- Passage en version 0.7.0.

### Buts

- Transformer les KPI en structure éditoriale exploitable par des writers
  ultérieurs (hors périmètre : DOCX/Markdown).

### Impact

- Sections sans données requises sont exclues automatiquement ; téléphonie,
  site et agent sont couverts par des fabriques dédiées.

## 2026-03-30 12:00:00

### Modifications

- Sous-package `processing/kpi/` : agrégation par période (`PeriodAggregator`),
  par site, agent et canal (`ActivityAggregator`), calculateurs
  `TelephonyKpiCalculator`, `SiteKpiCalculator`, `AgentKpiCalculator`, pipeline
  rejouable `KpiComputationPipeline` branché sur `PreparedDataRepository` et
  `KpiRepository`.
- Schéma SQLite : colonnes optionnelles `site`, `agent`, `channel` sur
  `kpi_data`, migration automatique pour les bases existantes, méthode
  `delete_for_period` sur `KpiRepository`.
- Exception `KpiComputationError` ; classe `ConsolidatedDataSchema` pour les
  noms de sources et colonnes canoniques.
- Catalogue documenté des KPI : `docs/kpi_metrics_catalog.md`.
- Passage en version 0.6.0 ; couverture de tests globale environ 95 %.

### Buts

- Calculer et persister les indicateurs à partir des données préparées sans
  logique de rendu ni writers.
- Permettre le recalcul idempotent sur une même période.

### Impact

- Les rapports futurs peuvent s'appuyer sur des métriques structurées et
  filtrables par dimension.

## 2026-03-26 15:45:00

### Modifications

- Création du sous-package `storage/sqlite/` avec `DatabaseSessionManager` :
  gestion de connexion SQLite, initialisation automatique du schéma (4 tables),
  mode WAL, fermeture propre, support `:memory:` et fichier.
- Création du sous-package `storage/repositories/` avec :
  - `RawDataRepository` : persistance des données brutes (save/load/count/delete).
  - `PreparedDataRepository` : persistance des données nettoyées/normalisées.
  - `KpiRepository` : persistance des indicateurs calculés avec période.
  - `ReportDataRepository` : persistance des sections de rapport générées.
- Schéma SQLite minimal : `raw_data`, `prepared_data`, `kpi_data`, `report_data`.
- Sérialisation JSON des lignes DataFrame pour le stockage row-level.
- Ajout de 43 tests unitaires sur base SQLite en mémoire (`:memory:`).
- Configuration bandit : skip B608 (f-strings avec noms de tables constantes).
- Passage en version 0.5.0.

### Buts

- Mettre en place une couche de persistance abstraite adossée à SQLite,
  séparant données brutes, préparées et métriques.
- Permettre le stockage intermédiaire entre les étapes du pipeline pour
  faciliter l'audit, le recalcul et la traçabilité.

### Impact

- Les données extraites, standardisées et les KPI calculés peuvent
  désormais être persistés en SQLite et relus.
- Toute erreur SQLite est encapsulée dans `PersistenceError`.
- Le domaine ne dépend pas directement des détails SQLite : les
  repositories abstraient l'accès aux données.
- La couverture de code reste à 97 %.

## 2026-03-26 14:15:00

### Modifications

- Création du sous-package `processing/normalization/` avec :
  - `ColumnMapper` : renommage de colonnes via un dictionnaire de mapping.
  - `DataTypeNormalizer` : conversion de colonnes vers datetime, int, float.
  - `ValueStandardizer` : normalisation des valeurs textuelles (espaces,
    accents, casse) pour harmoniser les libellés d'agents et de sites.
  - `StandardizationPipeline` : orchestrateur enchaînant mapping, nettoyage,
    normalisation des types et standardisation des valeurs.
- Création du sous-package `processing/cleaning/` avec :
  - `DataCleaner` : strip des espaces, normalisation de casse (lower, upper,
    title) sur les colonnes texte.
- Création du sous-package `processing/validation/` avec :
  - `ValidationRule` : règle abstraite applicable à un DataFrame.
  - `ColumnPresenceRule` : vérifie la présence de colonnes obligatoires.
  - `NullRatioRule` : vérifie le taux de valeurs nulles par colonne.
  - `SchemaRegistry` : registre de schémas attendus par type de source,
    générant automatiquement les règles de validation.
  - `DatasetValidator` : exécute séquentiellement les règles et agrège
    les résultats dans un `ValidationResult`.
- Ajout de 75 tests unitaires pour la standardisation et la validation.
- Passage en version 0.4.0.

### Buts

- Rendre les données extraites homogènes, typées et exploitables
  avant toute règle de rapprochement métier.
- Permettre la détection précoce d'anomalies structurelles et de qualité.

### Impact

- Les données issues des extracteurs CSV peuvent maintenant être
  nettoyées, renommées, typées et validées de manière systématique.
- Les erreurs de conversion sont encapsulées dans `StandardizationError`.
- Les contrôles de validation distinguent erreurs bloquantes et
  avertissements via `ValidationResult`.
- La couverture de code reste à 100 %.

## 2026-03-26 11:10:00

### Modifications

- Création du sous-package `ingestion/extractors/` pour la couche d'ingestion.
- Création de `CsvExtractionConfiguration` : objet de configuration de lecture
  CSV (séparateur, encodage, colonnes attendues, lignes à ignorer, libellé).
- Création de `BaseExtractor` : extracteur abstrait implémentant la lecture
  CSV via pandas, la vérification d'existence du fichier, la détection des
  colonnes manquantes et la journalisation via `logging`.
- Création de `CsvIncomingCallsExtractor` : extracteur spécialisé pour les
  fichiers d'appels entrants avec colonnes attendues prédéfinies.
- Création de `CsvOutgoingCallsExtractor` : extracteur spécialisé pour les
  fichiers d'appels sortants.
- Création de `CsvTicketExtractor` : extracteur spécialisé pour les fichiers
  de tickets (EFI, EDI, téléphone).
- Ajout de `pandas>=2.1.0,<3.0.0` comme dépendance de production et
  `pandas-stubs>=2.1.0` comme dépendance de développement.
- Création de fixtures CSV de test dans `tests/fixtures/` (appels entrants,
  appels sortants, tickets, fichier vide, fichier malformé, colonnes
  manquantes).
- Création de `tests/conftest.py` avec la fixture `fixtures_dir`.
- Ajout de 35 tests unitaires couvrant toutes les classes d'ingestion.
- Désactivation de `duplicate-code` dans pylint (similarité structurelle
  attendue entre extracteurs).
- Mise à jour de `README.md`, `CHANGELOG.md` et passage en version 0.3.0.

### Buts

- Fournir une couche d'ingestion propre capable de lire les fichiers CSV
  métiers en renvoyant des résultats d'extraction structurés.
- Séparer strictement la lecture de fichier de toute logique métier.
- Permettre aux features suivantes (standardisation, validation) de
  s'appuyer sur des `ExtractionResult` fiables.

### Impact

- Les fichiers CSV d'appels entrants, sortants et de tickets peuvent
  être lus avec des extracteurs spécialisés.
- Toute erreur de lecture (fichier absent, encodage invalide, etc.) est
  encapsulée dans une `ExtractionError` du projet.
- Les colonnes manquantes sont signalées en warning sans bloquer
  l'extraction.
- La couverture de code reste à 100 %.

## 2026-03-26 10:15:00

### Modifications

- Création du sous-package `domain/models/` contenant `ReportingPeriod`, `Agent`,
  `Site` et `Kpi`.
- Création du sous-package `domain/results/` contenant `ExtractionResult`,
  `ValidationResult` (avec `Severity` et `ValidationMessage`), `SectionDecision`
  (avec `SectionStatus`) et `DataAvailability`.
- Création de la hiérarchie d'exceptions métier : `ReportingError` (parente
  directe de `ApplicationException`) puis `ExtractionError`, `ValidationError`,
  `StandardizationError`, `ResolutionError`, `PersistenceError`,
  `ReportGenerationError` et `WriterError`.
- Mise à jour des exports dans tous les `__init__.py` du package racine,
  de `exceptions/`, `domain/models/` et `domain/results/`.
- Ajout de 175 tests unitaires couvrant toutes les nouvelles classes.
- Mise à jour de `README.md`, `CHANGELOG.md` et passage en version 0.2.0.
- Ajustement de pylint (`max-args`, `max-positional-arguments`) dans
  `pyproject.toml` pour autoriser 6 paramètres.

### Buts

- Poser le vocabulaire métier et technique du projet pour découpler le
  domaine des `DataFrame`.
- Standardiser la gestion des erreurs avec une hiérarchie d'exceptions
  cohérente couvrant chaque couche du pipeline.

### Impact

- Chaque couche du pipeline (extraction, standardisation, validation,
  résolution, persistance, génération de rapport, rendu) dispose
  désormais de sa propre exception dédiée.
- Les modèles métier (`Agent`, `Site`, `Kpi`, `ReportingPeriod`)
  permettent de manipuler des objets typés plutôt que des `DataFrame`.
- Les objets de résultat (`ExtractionResult`, `ValidationResult`,
  `SectionDecision`, `DataAvailability`) standardisent le transport
  des métadonnées entre les couches.
- La couverture de code reste à 100 %.

## 2026-03-26 09:00:00

### Modifications

- Création de l'arborescence du projet : `src/baobab_activity_reporting/`, `tests/`, `docs/`.
- Création du fichier `pyproject.toml` avec toute la configuration centralisée.
- Ajout des dépendances de production (aucune pour l'instant) et de développement
  (black, pylint, mypy, flake8, Flake8-pyproject, bandit, pytest, pytest-cov, coverage).
- Création de la classe `ApplicationException` : exception de base du projet.
- Création de la classe `ConfigurationException` : exception technique héritant
  de `ApplicationException`.
- Création de la classe `PackageMetadata` : accès centralisé au nom et à la version
  du package.
- Création des fichiers `__init__.py` avec les exports publics.
- Création du `README.md`, du `CHANGELOG.md` et de ce journal de développement.
- Création des tests unitaires pour les trois classes.

### Buts

- Mettre en place le socle du projet : dépôt installable, ossature du package,
  outils de qualité, base documentaire, hiérarchie d'exceptions racine.
- Permettre à toute feature future de s'appuyer sur une base saine et testée.

### Impact

- Le package est installable via `pip install -e ".[dev]"`.
- Les outils de qualité (black, pylint, mypy, flake8, bandit) sont configurés
  et opérationnels.
- La couverture de code est mesurée et ses rapports sont générés dans
  `docs/tests/coverage`.
- La hiérarchie d'exceptions est en place : toute exception future du projet
  héritera de `ApplicationException`.
- `PackageMetadata` centralise l'accès aux métadonnées du package.

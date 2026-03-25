# Cahier des charges — baobab_activity_reporting

## 1. Présentation du projet

### 1.1. Nom du projet
`baobab_activity_reporting`

### 1.2. Description courte
API Python de génération de rapports d’activité à partir de fichiers sources. Elle extrait, nettoie, rapproche, calcule et stocke les données, puis produit des rapports structurés par période, site ou agent, avec export documentaire.

### 1.3. Finalité
Le projet a pour objectif de fournir une API Python capable de produire automatiquement des rapports d’activité à partir de données issues de plusieurs exports métiers.

L’application devra :
- lire des fichiers sources hétérogènes ;
- standardiser et fiabiliser les données ;
- appliquer des règles métier de rapprochement ;
- calculer des indicateurs consolidés ;
- stocker les données préparées et les métriques ;
- construire des rapports adaptés aux données réellement disponibles ;
- exporter les rapports dans un format documentaire exploitable.

---

## 2. Contexte fonctionnel

Le projet vise à industrialiser la production de rapports d’activité à partir de fichiers de suivi d’activité, notamment :
- appels entrants ;
- appels sortants ;
- tickets ou exports d’activité ;
- autres fichiers similaires à intégrer ultérieurement.

Le système doit permettre de produire plusieurs familles de rapports, avec une granularité variable :
- journalière ;
- hebdomadaire ;
- mensuelle.

Les rapports devront pouvoir être produits selon plusieurs axes :
- rapport global d’activité ;
- rapport par site ;
- rapport par agent ;
- rapport d’activité téléphonique technique pour professionnels.

Le système doit également intégrer des règles métier spécifiques au domaine, notamment :
- la distinction entre site de répartition et site réellement propriétaire ;
- la notion de propriété par qualification de l’agent ;
- la distinction entre EFI et EDI pour les formulaires ;
- le rapprochement entre tickets et appels via l’identité de l’agent.

---

## 3. Objectifs du projet

## 3.1. Objectifs principaux
Le projet doit permettre de :
- automatiser la chaîne de production des rapports ;
- fiabiliser les chiffres et les indicateurs ;
- expliciter les règles métier utilisées ;
- produire des rapports homogènes et réutilisables ;
- permettre l’évolution future du système sans refonte globale.

## 3.2. Objectifs techniques
Le projet doit fournir :
- une API Python claire et testable ;
- une architecture en couches ;
- une séparation stricte entre extraction, transformation, calcul, stockage et rendu ;
- une base SQLite dans un premier temps ;
- une capacité d’évolution vers une base serveur ultérieurement ;
- une capacité d’export documentaire.

## 3.3. Objectifs qualité
Le projet doit être :
- maintenable ;
- testable ;
- extensible ;
- documenté ;
- typé ;
- compatible avec un développement piloté ou assisté par IA.

---

## 4. Périmètre

## 4.1. Inclus dans le périmètre
Le projet couvre :
- la lecture de fichiers sources ;
- l’extraction des données via `pandas` ;
- le nettoyage et la normalisation ;
- la validation de structure et de qualité ;
- l’application des règles métier de rapprochement ;
- le calcul d’indicateurs ;
- le stockage en SQLite ;
- la récupération des données calculées ;
- la génération d’un modèle de rapport ;
- l’export du rapport ;
- la prise en charge de rapports périodiques ;
- la prise en charge de rapports par agent et par site.

## 4.2. Hors périmètre initial
Ne sont pas prioritaires dans la première version :
- la mise en place d’une base PostgreSQL ou équivalent ;
- l’interface web utilisateur complète ;
- l’orchestration distribuée ;
- le versionning documentaire complexe ;
- l’analyse assistée par IA générative ;
- l’OCR ;
- la gestion d’un volume massif multi-instance.

---

## 5. Principes d’architecture

L’architecture devra respecter les principes suivants :
- séparation stricte des responsabilités ;
- faible couplage entre les couches ;
- logique métier indépendante des formats de fichiers ;
- logique de rédaction indépendante du moteur de rendu ;
- persistance abstraite ;
- capacité de test unitaire et d’intégration ;
- règles métier centralisées ;
- extensibilité du système.

L’architecture cible reposera sur la chaîne suivante :

ingestion → standardisation → validation → résolution métier → calcul KPI → persistance → planification éditoriale → rédaction → rendu

---

## 6. Architecture fonctionnelle

## 6.1. Vue d’ensemble
Le système devra être organisé en couches fonctionnelles distinctes :

- couche d’ingestion ;
- couche de standardisation ;
- couche de validation ;
- couche de résolution métier ;
- couche de calcul et d’agrégation ;
- couche de persistance ;
- couche de préparation éditoriale ;
- couche de rédaction métier ;
- couche de rendu documentaire.

---

## 7. Couche d’ingestion

## 7.1. Rôle
Lire les sources et transformer les fichiers en structures tabulaires brutes.

## 7.2. Responsabilités
- lecture des fichiers CSV ;
- gestion des encodages ;
- gestion des séparateurs ;
- vérification de présence de fichier ;
- chargement en `pandas.DataFrame` ;
- traçabilité de l’extraction.

## 7.3. Contraintes
Cette couche ne doit pas :
- contenir de logique métier ;
- calculer d’indicateurs ;
- écrire le rapport ;
- contenir de logique de persistance avancée.

## 7.4. Composants attendus
- `BaseExtractor`
- `CsvIncomingCallsExtractor`
- `CsvOutgoingCallsExtractor`
- `CsvTicketExtractor`
- `ExtractionResult`

## 7.5. Contrat attendu
Entrée :
- chemin du fichier ;
- configuration de lecture.

Sortie :
- `ExtractionResult` contenant au minimum :
  - `dataframe`
  - `source_name`
  - `row_count`
  - `column_names`
  - `warnings`
  - `errors`

---

## 8. Couche de standardisation

## 8.1. Rôle
Transformer les données brutes en données exploitables, homogènes et cohérentes.

## 8.2. Responsabilités
- renommage des colonnes ;
- harmonisation des valeurs ;
- normalisation des types ;
- conversion des dates ;
- nettoyage des chaînes ;
- traitement des valeurs manquantes ;
- homogénéisation des noms d’agents ;
- homogénéisation des noms de sites ;
- préparation des champs utiles au rapprochement.

## 8.3. Contraintes
Cette couche ne doit pas :
- contenir la logique éditoriale ;
- produire directement les rapports ;
- contenir le calcul final des KPI ;
- dépendre du moteur de rendu.

## 8.4. Composants attendus
- `ColumnMapper`
- `DataCleaner`
- `DataTypeNormalizer`
- `ValueStandardizer`
- `StandardizationPipeline`

## 8.5. Exemples de transformations
- uniformiser la casse des noms ;
- supprimer les espaces parasites ;
- gérer les accents si nécessaire ;
- convertir les dates vers un format unique ;
- harmoniser les libellés de site ;
- identifier les tickets issus de formulaire ;
- distinguer EFI et EDI.

---

## 9. Couche de validation

## 9.1. Rôle
Vérifier que les données sont structurellement et fonctionnellement exploitables.

## 9.2. Responsabilités
- contrôle des colonnes obligatoires ;
- contrôle des types attendus ;
- contrôle des dates ;
- détection d’anomalies ;
- détection de valeurs incohérentes ;
- production de résultats de validation ;
- remontée d’erreurs bloquantes ou d’avertissements.

## 9.3. Composants attendus
- `DatasetValidator`
- `ValidationRule`
- `ValidationResult`
- `SchemaRegistry`

## 9.4. Niveaux de validation
- validation structurelle ;
- validation de qualité ;
- validation métier simple.

## 9.5. Résultats attendus
La validation doit permettre de savoir :
- si le fichier est exploitable ;
- quelles colonnes sont absentes ;
- quelles données sont invalides ;
- si le chargement doit être bloqué ;
- si le traitement peut continuer avec avertissements.

---

## 10. Couche de résolution métier

## 10.1. Rôle
Appliquer les règles métier qui permettent de relier plusieurs jeux de données entre eux.

## 10.2. Responsabilités
- identifier l’agent ;
- identifier le site métier ;
- déterminer la propriété du ticket ;
- relier appels et tickets ;
- enrichir les données avec des clés techniques ;
- préparer les données pour l’agrégation.

## 10.3. Composants attendus
- `AgentIdentityResolver`
- `TicketOwnershipResolver`
- `TicketCallLinker`
- `SiteResolver`
- `BusinessResolutionPipeline`

## 10.4. Règles métier à intégrer
Le système devra intégrer les règles suivantes :

### 10.4.1. Site propriétaire du ticket
Le site propriétaire d’un ticket n’est pas uniquement le site de répartition.  
La propriété métier doit être déterminée à partir du `Site Agent Qualification`.

### 10.4.2. Rapprochement appels / tickets
La jointure entre les données d’appels et de tickets se fait via le nom et le prénom de l’agent.

### 10.4.3. Tickets issus de formulaire
Les tickets issus de formulaire doivent être distingués selon :
- `EFI`
- `EDI`

### 10.4.4. Tickets issus du téléphone
Les tickets arrivés par téléphone doivent, lorsque cela est possible, être rapprochés de l’activité d’appel.

## 10.5. Point d’attention
La jointure par nom et prénom est fragile.  
Le système doit donc prévoir :
- une normalisation forte des identités ;
- une gestion des accents ;
- une gestion des espaces ;
- une harmonisation de la casse ;
- un mécanisme d’alias ou de correspondance manuelle.

## 10.6. Référentiels recommandés
- `agent_reference`
- `agent_alias`

---

## 11. Couche de calcul et d’agrégation

## 11.1. Rôle
Calculer les indicateurs consolidés utilisés dans les rapports.

## 11.2. Responsabilités
- agrégation par période ;
- agrégation par site ;
- agrégation par agent ;
- agrégation par canal ;
- calcul de volumétrie ;
- calcul de répartitions ;
- calcul d’évolutions ;
- production de données prêtes pour le reporting.

## 11.3. Composants attendus
- `PeriodAggregator`
- `ActivityAggregator`
- `SiteKpiCalculator`
- `AgentKpiCalculator`
- `TelephonyKpiCalculator`
- `KpiComputationPipeline`

## 11.4. Indicateurs attendus
Selon les jeux de données disponibles, l’application devra pouvoir calculer notamment :
- nombre d’appels entrants ;
- nombre d’appels sortants ;
- nombre de tickets ;
- nombre d’activités par site ;
- nombre d’activités par agent ;
- répartition par canal ;
- répartition EFI / EDI ;
- évolution d’une période à l’autre ;
- charge par canal ;
- part relative de chaque catégorie.

## 11.5. Contraintes
Les calculateurs doivent être :
- testables indépendamment ;
- découplés du stockage ;
- découplés du writer ;
- réutilisables selon le type de rapport.

---

## 12. Couche de persistance

## 12.1. Rôle
Stocker les données brutes, préparées et calculées.

## 12.2. Base de données initiale
La persistance devra être assurée par SQLite dans la première version.

## 12.3. Contraintes
La couche de persistance doit être conçue de façon à permettre une migration ultérieure vers une base serveur sans remettre en cause le cœur métier.

## 12.4. Composants attendus
- `DatabaseSessionManager`
- `RawDataRepository`
- `PreparedDataRepository`
- `KpiRepository`
- `ReportDataRepository`

## 12.5. Niveaux de stockage
Le stockage devra distinguer au minimum trois niveaux :

### 12.5.1. `raw`
Copie des données sources chargées.

### 12.5.2. `prepared`
Données nettoyées, normalisées et enrichies.

### 12.5.3. `metrics`
Indicateurs calculés et prêts à être interrogés.

## 12.6. Objectifs
Cette séparation doit permettre :
- l’audit d’un chiffre ;
- le recalcul après évolution d’une règle ;
- la traçabilité des traitements ;
- le diagnostic des anomalies.

---

## 13. Couche de préparation éditoriale

## 13.1. Rôle
Déterminer quelles sections doivent apparaître dans le rapport final.

## 13.2. Responsabilités
- sélectionner le bon type de rapport ;
- déterminer les sections pertinentes ;
- retirer les sections sans données suffisantes ;
- produire un plan cohérent ;
- adapter le rapport à la réalité des données disponibles.

## 13.3. Composants attendus
- `ReportDefinition`
- `ReportPlanner`
- `SectionEligibilityEvaluator`
- `SectionDecision`
- `ReportContext`

## 13.4. Règle clé
Si une section ne dispose pas des données minimales nécessaires, elle doit :
- être retirée ;
- ou être remplacée par une variante plus adaptée ;
- ou être déclarée non publiable.

## 13.5. Exemple
Une section d’analyse EFI / EDI ne doit pas apparaître si la période ne contient pas de données exploitables permettant cette distinction.

---

## 14. Couche de rédaction métier

## 14.1. Rôle
Construire le contenu métier du rapport à partir des données consolidées.

## 14.2. Responsabilités
- générer les titres ;
- générer les sous-titres ;
- construire les paragraphes analytiques ;
- produire les tableaux ;
- formuler les insights ;
- construire un objet de rapport indépendant du format final.

## 14.3. Composants attendus
- `NarrativeBuilder`
- `TableBuilder`
- `InsightBuilder`
- `ReportBuilder`
- `ReportModel`

## 14.4. Principe
La rédaction métier ne doit pas dépendre du format DOCX, PDF, HTML ou Markdown.

Le résultat de cette couche doit être un objet structuré contenant au minimum :
- les métadonnées du rapport ;
- le titre ;
- la période ;
- les sections ;
- les sous-sections ;
- les paragraphes ;
- les tableaux ;
- les indicateurs affichés ;
- les remarques éventuelles.

---

## 15. Couche de rendu documentaire

## 15.1. Rôle
Transformer le `ReportModel` en document final.

## 15.2. Responsabilités
- appliquer les styles ;
- écrire les titres ;
- écrire les paragraphes ;
- écrire les tableaux ;
- gérer la mise en page ;
- exporter le document.

## 15.3. Composants attendus
- `AbstractWriter`
- `DocxWriter`
- `MarkdownWriter`
- `HtmlWriter`

## 15.4. Contraintes
Le writer ne doit pas :
- contenir la logique métier ;
- faire des calculs de KPI ;
- piloter les règles de visibilité des sections.

---

## 16. Modèle métier

Le système ne doit pas reposer exclusivement sur des `DataFrame`.  
Il doit également s’appuyer sur des objets métier explicites.

## 16.1. Entités métier principales
- `ReportingPeriod`
- `Agent`
- `Site`
- `CallRecord`
- `TicketRecord`
- `PreparedCallActivity`
- `PreparedTicketActivity`
- `Kpi`
- `ReportSection`
- `ReportDefinition`
- `ReportModel`

## 16.2. Objets techniques utiles
- `ExtractionResult`
- `ValidationResult`
- `SectionDecision`
- `NarrativeBlock`
- `DataAvailability`
- `QueryFilter`

---

## 17. API applicative cible

Avant toute API HTTP, le projet devra proposer une API Python stable.

## 17.1. Méthodes attendues
Le système devra pouvoir exposer une façade de type :
- `import_sources(...)`
- `compute_metrics(...)`
- `generate_report(...)`
- `export_report(...)`

## 17.2. Objectif
La façade applicative doit :
- simplifier l’usage du moteur ;
- exposer des cas d’usage clairs ;
- masquer la complexité interne ;
- servir de base à une future couche HTTP ou CLI.

---

## 18. API HTTP future

Une API HTTP pourra être ajoutée dans un second temps, idéalement avec FastAPI.

## 18.1. Endpoints cibles possibles
- `POST /imports`
- `POST /metrics/compute`
- `POST /reports/generate`
- `POST /reports/export`
- `GET /reports/{id}`

## 18.2. Principe
La couche HTTP devra uniquement exposer les cas d’usage applicatifs.  
Elle ne devra pas contenir le cœur métier.

---

## 19. Types de rapports à produire

## 19.1. Rapport d’activité téléphonique technique
Déclinaisons :
- journalier ;
- hebdomadaire ;
- mensuel.

## 19.2. Rapport par agent
Déclinaisons :
- journalier ;
- hebdomadaire ;
- mensuel.

## 19.3. Rapport par site
Déclinaisons :
- journalier ;
- hebdomadaire ;
- mensuel.

## 19.4. Conséquence de conception
Le type de rapport devra être porté par une définition configurable indiquant :
- les sections attendues ;
- les KPI requis ;
- les règles de visibilité ;
- les variantes ;
- le gabarit rédactionnel.

---

## 20. Gestion des sections conditionnelles

Chaque section devra pouvoir déclarer :
- ses données minimales nécessaires ;
- ses KPI obligatoires ;
- ses KPI optionnels ;
- sa règle de visibilité ;
- ses variantes éventuelles.

## 20.1. Objectif
Permettre la génération d’un rapport cohérent même lorsque certaines données manquent.

## 20.2. Règles attendues
Une section ne doit pas apparaître si :
- les KPI requis sont absents ;
- les données minimales sont insuffisantes ;
- la section n’est pas pertinente pour le type de rapport demandé.

---

## 21. Gestion des règles métier

Les règles métier ne doivent pas être dispersées dans l’ensemble du code.

## 21.1. Principe
Elles doivent être regroupées dans des modules dédiés et documentés.

## 21.2. Exemples de fichiers attendus
- `ticket_ownership_rules.py`
- `agent_matching_rules.py`
- `ticket_channel_rules.py`
- `section_visibility_rules.py`

## 21.3. Avantages attendus
- meilleure lisibilité ;
- meilleure testabilité ;
- meilleure maintenabilité ;
- évolution facilitée.

---

## 22. Structure de projet recommandée

La structure cible recommandée est la suivante :

    baobab_activity_reporting/
      src/
        baobab_activity_reporting/
          application/
            use_cases/
          domain/
            models/
            rules/
            services/
          ingestion/
            extractors/
            schemas/
          processing/
            cleaning/
            normalization/
            validation/
            resolution/
            aggregation/
          storage/
            sqlite/
            repositories/
          reporting/
            builders/
            definitions/
            writers/
          interfaces/
            cli/
            api/
      tests/
        unit/
        integration/
        fixtures/
      docs/
      pyproject.toml
      README.md

---

## 23. Exigences fonctionnelles détaillées

## 23.1. Extraction
Le système doit :
- lire des fichiers CSV ;
- gérer plusieurs types de source ;
- remonter les erreurs de lecture ;
- produire des résultats structurés.

## 23.2. Nettoyage et normalisation
Le système doit :
- uniformiser les colonnes ;
- convertir les types ;
- nettoyer les libellés ;
- standardiser les dates ;
- préparer les données pour le rapprochement.

## 23.3. Validation
Le système doit :
- vérifier la présence des colonnes obligatoires ;
- détecter les anomalies majeures ;
- distinguer erreurs bloquantes et avertissements.

## 23.4. Rapprochement métier
Le système doit :
- rapprocher les données tickets et appels ;
- déterminer la propriété du ticket ;
- consolider les activités par agent et par site.

## 23.5. Calcul des indicateurs
Le système doit :
- calculer les indicateurs par période ;
- calculer les indicateurs par site ;
- calculer les indicateurs par agent ;
- préparer les données pour le reporting.

## 23.6. Persistance
Le système doit :
- stocker les données brutes ;
- stocker les données préparées ;
- stocker les indicateurs calculés ;
- permettre la lecture efficace de ces données.

## 23.7. Génération de rapport
Le système doit :
- sélectionner le bon plan de rapport ;
- retirer les sections non exploitables ;
- construire le contenu analytique ;
- produire un document final exportable.

## 23.8. Export
Le système doit permettre au minimum :
- l’export DOCX ;
- éventuellement l’export Markdown ;
- éventuellement l’export HTML.

---

## 24. Exigences non fonctionnelles

## 24.1. Maintenabilité
Le code doit être organisé de façon claire, modulaire et documentée.

## 24.2. Testabilité
Chaque couche critique doit être testable indépendamment.

## 24.3. Typage
Le code doit être typé autant que raisonnablement possible.

## 24.4. Observabilité
Le système doit produire des logs explicites.

## 24.5. Extensibilité
L’ajout d’un nouveau type de source ou d’un nouveau type de rapport ne doit pas imposer une refonte du cœur applicatif.

## 24.6. Robustesse
Le système doit échouer proprement avec des erreurs spécifiques lorsqu’une étape critique échoue.

---

## 25. Gestion des erreurs

Le projet doit utiliser des exceptions spécifiques.

## 25.1. Exceptions attendues
- `ReportingError`
- `ExtractionError`
- `ValidationError`
- `StandardizationError`
- `ResolutionError`
- `PersistenceError`
- `ReportGenerationError`
- `WriterError`

## 25.2. Règle
Toute erreur métier ou technique propre au projet doit faire l’objet d’une exception dédiée.

---

## 26. Journalisation et traçabilité

Le système doit journaliser au minimum :
- début et fin des imports ;
- nombre de lignes lues ;
- anomalies de validation ;
- rapprochements effectués ;
- nombre d’enregistrements persistés ;
- lancement des calculs ;
- sections retenues ;
- sections retirées ;
- génération du document final.

---

## 27. Tests attendus

## 27.1. Tests unitaires
À prévoir sur :
- extracteurs ;
- normalisation ;
- validation ;
- règles métier ;
- calculateurs ;
- planificateur ;
- builders ;
- writers ;
- repositories.

## 27.2. Tests d’intégration
À prévoir sur :
- pipeline complet import → calcul → rapport ;
- persistance SQLite ;
- génération documentaire ;
- règles de suppression de sections ;
- rapprochement appels / tickets.

## 27.3. Jeux de données de test
Prévoir des fixtures représentatives pour :
- cas nominal ;
- colonnes manquantes ;
- dates invalides ;
- homonymies agents ;
- données partielles ;
- absence de tickets ;
- absence d’appels ;
- absence de distinction EFI / EDI ;
- sections à retirer.

---

## 28. Contraintes de développement

Le développement devra respecter les contraintes suivantes :
- Python moderne ;
- architecture modulaire ;
- typage ;
- docstrings sur les éléments publics ;
- code testé ;
- exceptions spécifiques au projet ;
- absence de logique métier dans les extracteurs au-delà de leur responsabilité ;
- absence de logique métier dans les writers ;
- séparation claire entre métier, stockage et rendu.

---

## 29. Séquence d’implémentation recommandée

## 29.1. Lot 1 — Socle
- initialisation du projet ;
- structure du dépôt ;
- exceptions ;
- logging ;
- extracteurs ;
- standardisation minimale ;
- persistance SQLite.

## 29.2. Lot 2 — Validation et résolution métier
- validateurs ;
- normalisation avancée ;
- résolution agent ;
- résolution site ;
- rapprochement tickets / appels.

## 29.3. Lot 3 — Calculs
- calculateurs de KPI ;
- agrégations ;
- persistance des métriques.

## 29.4. Lot 4 — Reporting
- définitions de rapports ;
- évaluateur de sections ;
- planificateur ;
- builders ;
- modèle de rapport.

## 29.5. Lot 5 — Export
- writer abstrait ;
- writer DOCX ;
- éventuels writers secondaires.

## 29.6. Lot 6 — Exposition
- façade applicative ;
- CLI ;
- API HTTP éventuelle.

---

## 30. Critères d’acceptation

Le projet sera considéré conforme lorsque :
- les fichiers sources sont lisibles et traitables ;
- les données sont nettoyées et validées ;
- les règles métier sont appliquées correctement ;
- les KPI sont calculés et persistés ;
- les rapports sont générés avec les bonnes sections ;
- les sections sans données sont automatiquement retirées ;
- les exports documentaires fonctionnent ;
- les tests essentiels sont en place ;
- l’architecture reste modulaire et maintenable.

---

## 31. Livrables attendus

Les livrables attendus sont :
- le code source du projet ;
- le fichier `pyproject.toml` ;
- le `README.md` ;
- la documentation d’architecture ;
- la documentation des règles métier ;
- les tests unitaires ;
- les tests d’intégration ;
- les fixtures de test ;
- les writers documentaires ;
- les exemples de génération de rapport.

---

## 32. Résumé

`baobab_activity_reporting` doit être une API Python modulaire de génération de rapports d’activité fondée sur une architecture en couches.

Le système devra :
- extraire ;
- nettoyer ;
- valider ;
- rapprocher ;
- calculer ;
- stocker ;
- planifier ;
- rédiger ;
- exporter.

Le tout devra être conçu pour produire des rapports robustes, traçables, maintenables et extensibles, tout en intégrant explicitement les règles métier nécessaires à la fiabilité des analyses.

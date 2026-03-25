# baobab_activity_reporting

## 1. Objet du projet

Développer une API Python capable de :

1. extraire des données issues de plusieurs fichiers sources ;
2. nettoyer, normaliser et valider ces données ;
3. appliquer des règles métier pour relier les données entre elles ;
4. calculer des indicateurs d’activité ;
5. stocker les données calculées dans une base SQLite dans un premier temps ;
6. récupérer les indicateurs consolidés pour une période donnée ;
7. générer un rapport d’activité rédigé, structuré et exportable.

L’architecture doit permettre de produire plusieurs types de rapports, notamment :

- rapport d’activité téléphonique technique pour professionnels ;
- rapport par site ;
- rapport par agent ;

sur plusieurs périodicités :

- journalière ;
- hebdomadaire ;
- mensuelle.

---

## 2. Principes d’architecture

L’application doit être conçue selon les principes suivants :

- séparation stricte des responsabilités ;
- architecture en couches ;
- logique métier indépendante du format des fichiers ;
- logique de rédaction indépendante du moteur de rendu documentaire ;
- persistance abstraite pour permettre le passage ultérieur de SQLite à une base serveur ;
- forte testabilité ;
- extensibilité pour accueillir de nouvelles sources, de nouveaux indicateurs, de nouveaux types de rapports et de nouveaux formats d’export.

---

## 3. Vision globale du pipeline

Sources fichiers  
→ Extractors  
→ Normalizers / Cleaners  
→ Validators  
→ Resolvers métier  
→ Aggregators / KPI Calculators  
→ Repositories SQLite  
→ Report Data Query Services  
→ Section Eligibility Evaluator  
→ Report Planner  
→ Narrative Builder  
→ Report Model  
→ Writer DOCX / Markdown / HTML

---

## 4. Couches de l’architecture

## 4.1. Couche d’ingestion

### Rôle
Lire les fichiers sources et produire des structures tabulaires brutes.

### Responsabilités
- lecture des fichiers CSV ;
- gestion des encodages ;
- gestion des séparateurs ;
- contrôle de présence du fichier ;
- chargement en `pandas.DataFrame`.

### Contraintes
- aucune logique métier dans cette couche ;
- aucun calcul d’indicateur dans cette couche ;
- aucun rendu documentaire dans cette couche.

### Composants
- `BaseExtractor`
- `CsvIncomingCallsExtractor`
- `CsvOutgoingCallsExtractor`
- `CsvTicketExtractor`
- `ExtractionResult`

### Contrat attendu
**Entrée :**
- chemin vers un fichier ;
- configuration de lecture.

**Sortie :**
- `ExtractionResult` contenant :
  - `dataframe`
  - `source_name`
  - `row_count`
  - `column_names`
  - erreurs ou avertissements éventuels

---

## 4.2. Couche de standardisation

### Rôle
Transformer les données brutes en données exploitables et homogènes.

### Responsabilités
- renommage des colonnes ;
- normalisation des types ;
- nettoyage des chaînes ;
- harmonisation des formats de date ;
- uniformisation des valeurs métier ;
- gestion des valeurs manquantes ;
- normalisation des noms d’agents et des sites ;
- distinction des canaux ou catégories métier.

### Contraintes
- pas de persistance ;
- pas de rédaction du rapport ;
- pas de calcul des KPI finaux.

### Composants
- `ColumnMapper`
- `DataCleaner`
- `DataTypeNormalizer`
- `ValueStandardizer`
- `StandardizationPipeline`

### Exemples de règles
- uniformiser les noms et prénoms des agents ;
- homogénéiser les libellés de sites ;
- convertir les dates ;
- distinguer les tickets issus de formulaire :
  - `EFI`
  - `EDI`
- distinguer les tickets issus du téléphone si le champ source le permet.

---

## 4.3. Couche de validation

### Rôle
Vérifier que les données sont exploitables et conformes aux attentes minimales.

### Responsabilités
- contrôle de présence des colonnes obligatoires ;
- contrôle des types attendus ;
- détection des valeurs anormales ;
- détection de taux de données manquantes ;
- émission d’erreurs bloquantes ou d’avertissements.

### Composants
- `DatasetValidator`
- `ValidationRule`
- `ValidationResult`
- `SchemaRegistry`

### Types de validation
- validation structurelle ;
- validation de qualité ;
- validation métier simple.

---

## 4.4. Couche de résolution métier

### Rôle
Appliquer les règles métier qui relient les jeux de données entre eux.

### Responsabilités
- rattacher un ticket au bon agent ;
- rattacher un ticket au bon site métier ;
- faire les rapprochements entre appels et tickets ;
- qualifier les données selon les règles métier propres au domaine ;
- enrichir les données avec des clés de rapprochement.

### Composants
- `AgentIdentityResolver`
- `TicketOwnershipResolver`
- `TicketCallLinker`
- `SiteResolver`
- `BusinessResolutionPipeline`

### Règles métier identifiées
- le site propriétaire d’un ticket ne dépend pas uniquement du site de répartition ;
- la propriété métier du ticket doit être déduite du `Site Agent Qualification` ;
- la jointure entre les données tickets et appels se fait via le nom et prénom de l’agent ;
- pour les tickets issus de formulaire, il faut distinguer `EFI` et `EDI` ;
- les tickets arrivés par téléphone doivent être rapprochés de l’activité d’appel lorsque cela est possible.

### Point d’attention
La jointure par nom/prénom est fragile. Il faut prévoir :
- normalisation forte ;
- suppression des espaces parasites ;
- gestion des accents ;
- casse homogène ;
- système d’alias ou de correspondance manuelle si nécessaire.

### Extension recommandée
Prévoir un référentiel :
- `agent_reference`
- `agent_alias`

---

## 4.5. Couche de calcul et d’agrégation

### Rôle
Calculer les indicateurs consolidés pour les différents rapports.

### Responsabilités
- agrégation par période ;
- agrégation par site ;
- agrégation par agent ;
- agrégation par canal ;
- calcul des volumes ;
- calcul des répartitions ;
- calcul des évolutions ;
- préparation des données prêtes pour le reporting.

### Composants
- `PeriodAggregator`
- `ActivityAggregator`
- `SiteKpiCalculator`
- `AgentKpiCalculator`
- `TelephonyKpiCalculator`
- `KpiComputationPipeline`

### Exemples d’indicateurs
- nombre d’appels entrants ;
- nombre d’appels sortants ;
- nombre de tickets ;
- répartition par canal ;
- répartition formulaire `EFI / EDI` ;
- activité par agent ;
- activité par site ;
- évolution sur la période ;
- indicateurs de charge ou de volumétrie ;
- part relative des canaux.

---

## 4.6. Couche de persistance

### Rôle
Stocker les données préparées et les indicateurs calculés.

### Responsabilités
- écrire en SQLite ;
- lire les données calculées ;
- isoler les accès aux données derrière des interfaces ;
- permettre une migration future vers PostgreSQL ou autre.

### Composants
- `DatabaseSessionManager`
- `RawDataRepository`
- `PreparedDataRepository`
- `KpiRepository`
- `ReportDataRepository`

### Niveaux de stockage
- `raw` : copie fidèle des données sources chargées ;
- `prepared` : données nettoyées, normalisées, enrichies ;
- `metrics` : indicateurs calculés, prêts à être utilisés par le reporting.

### Justification
Cette séparation facilite :
- l’audit d’un chiffre ;
- le recalcul après ajustement d’une règle métier ;
- la traçabilité ;
- l’investigation en cas d’anomalie.

---

## 4.7. Couche de préparation éditoriale

### Rôle
Déterminer ce qui doit apparaître dans le rapport et dans quel ordre.

### Responsabilités
- déterminer le type de rapport ;
- sélectionner les sections pertinentes ;
- retirer les sections sans données suffisantes ;
- préparer un plan de rapport final ;
- produire un modèle éditorial indépendant du format de sortie.

### Composants
- `ReportDefinition`
- `ReportPlanner`
- `SectionEligibilityEvaluator`
- `SectionDecision`
- `ReportContext`

### Règle clé
Si une donnée nécessaire à une section est absente ou insuffisante, la section concernée doit être :
- soit retirée ;
- soit remplacée par une variante adaptée ;
- soit marquée comme non publiable.

---

## 4.8. Couche de rédaction métier

### Rôle
Construire le contenu du rapport à partir des données calculées et du plan éditorial.

### Responsabilités
- générer les titres et sous-titres ;
- construire les tableaux ;
- formuler les paragraphes analytiques ;
- injecter les indicateurs dans les phrases ;
- produire un objet de rapport indépendant du moteur d’export.

### Composants
- `NarrativeBuilder`
- `TableBuilder`
- `InsightBuilder`
- `ReportBuilder`
- `ReportModel`

### Principe clé
La rédaction métier ne doit pas dépendre directement du format DOCX ou PDF.

Le résultat doit être un objet structuré, par exemple :
- métadonnées du rapport ;
- titre ;
- période ;
- sections ;
- sous-sections ;
- paragraphes ;
- tableaux ;
- listes d’indicateurs ;
- remarques.

---

## 4.9. Couche de rendu documentaire

### Rôle
Convertir le `ReportModel` en document final.

### Responsabilités
- appliquer les styles ;
- écrire les titres ;
- écrire les paragraphes ;
- écrire les tableaux ;
- gérer la mise en forme selon le format cible ;
- exporter le document.

### Composants
- `AbstractWriter`
- `DocxWriter`
- `MarkdownWriter`
- `HtmlWriter`

### Principes
- `AbstractWriter` définit le contrat de rendu ;
- chaque implémentation gère ses propres styles ;
- la logique de contenu ne doit pas être dans le writer.

---

## 5. Modèle métier recommandé

Le projet ne doit pas reposer uniquement sur des `DataFrame`. Il doit s’appuyer sur des objets métier explicites.

### Entités principales
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

### Objets techniques utiles
- `ExtractionResult`
- `ValidationResult`
- `SectionDecision`
- `NarrativeBlock`
- `DataAvailability`
- `QueryFilter`

---

## 6. Contrats de classes principales

### 6.1. Extracteur

    class BaseExtractor(ABC):
        @abstractmethod
        def extract(self, source_path: str) -> ExtractionResult:
            ...

### 6.2. Standardisation

    class StandardizationPipeline:
        def run(self, dataframe: pd.DataFrame) -> pd.DataFrame:
            ...

### 6.3. Validation

    class DatasetValidator:
        def validate(self, dataframe: pd.DataFrame) -> ValidationResult:
            ...

### 6.4. Résolution métier

    class AgentIdentityResolver:
        def resolve(self, dataframe: pd.DataFrame) -> pd.DataFrame:
            ...

### 6.5. Calcul KPI

    class KpiCalculator(ABC):
        @abstractmethod
        def compute(self, period: ReportingPeriod) -> list[Kpi]:
            ...

### 6.6. Planification du rapport

    class ReportPlanner:
        def build_plan(self, context: ReportContext) -> ReportDefinition:
            ...

### 6.7. Rédaction

    class ReportBuilder:
        def build(self, definition: ReportDefinition, context: ReportContext) -> ReportModel:
            ...

### 6.8. Rendu

    class AbstractWriter(ABC):
        @abstractmethod
        def write(self, report: ReportModel, output_path: str) -> None:
            ...

---

## 7. Structure de projet recommandée

    baobab_dgfip_activity_reporting/
      src/
        baobab_dgfip_activity_reporting/
          application/
            use_cases/
              import_sources.py
              compute_period_metrics.py
              generate_report.py

          domain/
            models/
              agent.py
              site.py
              reporting_period.py
              kpi.py
              report_model.py
            rules/
              ticket_ownership_rules.py
              agent_matching_rules.py
              section_visibility_rules.py
            services/
              report_planner.py
              section_eligibility_evaluator.py
              narrative_builder.py

          ingestion/
            extractors/
              base_extractor.py
              incoming_calls_csv_extractor.py
              outgoing_calls_csv_extractor.py
              tickets_csv_extractor.py
            schemas/
              source_schema_registry.py

          processing/
            cleaning/
              data_cleaner.py
            normalization/
              column_mapper.py
              type_normalizer.py
              value_standardizer.py
            validation/
              dataset_validator.py
              validation_rule.py
            resolution/
              agent_identity_resolver.py
              site_resolver.py
              ticket_call_linker.py
              ticket_ownership_resolver.py
            aggregation/
              period_aggregator.py
              activity_aggregator.py
              kpi_calculators.py

          storage/
            sqlite/
              connection.py
              models.py
              migrations.py
            repositories/
              raw_data_repository.py
              prepared_data_repository.py
              kpi_repository.py
              report_data_repository.py

          reporting/
            builders/
              report_builder.py
              table_builder.py
              insight_builder.py
            definitions/
              report_definitions.py
            writers/
              abstract_writer.py
              docx_writer.py
              markdown_writer.py
              html_writer.py

          interfaces/
            cli/
              main.py
            api/
              fastapi_app.py
              routes/

      tests/
        unit/
        integration/
        fixtures/

      docs/
        architecture.md
        business_rules.md
        report_definitions.md

      pyproject.toml
      README.md

---

## 8. Cas d’usage applicatifs

### 8.1. Importer des sources
**Objectif :**
Lire les fichiers, les valider, les nettoyer et stocker les données préparées.

**Use case :**
`ImportSourcesUseCase`

**Entrées :**
- chemins des fichiers ;
- type de source ;
- configuration éventuelle.

**Sorties :**
- rapport d’import ;
- nombre de lignes importées ;
- erreurs et avertissements ;
- données persistées.

### 8.2. Calculer les indicateurs d’une période
**Objectif :**
Consolider les données d’une période et produire les KPI.

**Use case :**
`ComputePeriodMetricsUseCase`

**Entrées :**
- période ;
- type de rapport ;
- périmètre éventuel (site, agent).

**Sorties :**
- jeux d’indicateurs persistés ;
- synthèse de calcul.

### 8.3. Générer un rapport
**Objectif :**
Produire un rapport prêt à être exporté.

**Use case :**
`GenerateReportUseCase`

**Entrées :**
- type de rapport ;
- période ;
- format de sortie ;
- filtre éventuel sur un agent ou un site.

**Sorties :**
- `ReportModel` ;
- document exporté.

---

## 9. Types de rapports à prévoir

### 9.1. Rapport d’activité téléphonique technique
Déclinaisons :
- journalier ;
- hebdomadaire ;
- mensuel.

### 9.2. Rapport par agent
Déclinaisons :
- journalier ;
- hebdomadaire ;
- mensuel.

### 9.3. Rapport par site
Déclinaisons :
- journalier ;
- hebdomadaire ;
- mensuel.

### Conséquence architecturale
Le type de rapport doit être porté par une définition configurable :
- sections attendues ;
- règles de visibilité ;
- indicateurs requis ;
- gabarit rédactionnel.

---

## 10. Gestion des sections conditionnelles

Chaque section du rapport doit pouvoir déclarer :
- les données minimales nécessaires ;
- les indicateurs obligatoires ;
- les règles de visibilité ;
- les variantes éventuelles.

### Exemple conceptuel

    @dataclass
    class SectionDefinition:
        code: str
        title: str
        required_kpis: list[str]
        optional_kpis: list[str]
        visibility_rule: str

### Règle métier
Une section ne doit pas apparaître si :
- les KPI requis sont absents ;
- les données disponibles sont insuffisantes ;
- la section n’est pas pertinente pour le type de rapport demandé.

---

## 11. Gestion des règles métier

Les règles métier ne doivent pas être dispersées dans les extracteurs ni dans les writers.

Elles doivent être centralisées dans des modules dédiés.

### Exemples de fichiers de règles
- `ticket_ownership_rules.py`
- `agent_matching_rules.py`
- `ticket_channel_rules.py`
- `section_visibility_rules.py`

### Avantages
- meilleure lisibilité ;
- meilleure testabilité ;
- adaptation plus simple si les règles changent ;
- réduction du couplage.

---

## 12. API applicative cible

Avant de proposer une API HTTP, l’application doit exposer une API Python propre, par exemple :

    service.import_sources(...)
    service.compute_metrics(...)
    service.generate_report(...)
    service.export_report(...)

### Exemple de façade

    class ReportingService:
        def import_sources(self, sources: list[str]) -> None:
            ...

        def compute_metrics(self, period: ReportingPeriod) -> None:
            ...

        def generate_report(self, report_type: str, period: ReportingPeriod, scope: dict) -> ReportModel:
            ...

        def export_report(self, report: ReportModel, output_format: str, output_path: str) -> None:
            ...

---

## 13. API HTTP future

Une API HTTP pourra être ajoutée dans un second temps, idéalement avec FastAPI.

### Endpoints possibles
- `POST /imports`
- `POST /metrics/compute`
- `POST /reports/generate`
- `POST /reports/export`
- `GET /reports/{id}`

### Règle
L’API HTTP doit être une couche d’exposition, pas le cœur métier.

---

## 14. Gestion des erreurs

Le projet doit utiliser des exceptions spécifiques.

### Exceptions recommandées
- `ReportingError`
- `ExtractionError`
- `ValidationError`
- `StandardizationError`
- `ResolutionError`
- `PersistenceError`
- `ReportGenerationError`
- `WriterError`

### Principe
Toute erreur métier ou technique importante propre au projet doit faire l’objet d’une exception spécifique.

---

## 15. Journalisation et traçabilité

Le projet doit journaliser au minimum :
- début et fin des imports ;
- nombre de lignes lues ;
- anomalies de validation ;
- règles de rapprochement appliquées ;
- nombre d’enregistrements persistés ;
- lancement des calculs ;
- sections retenues et sections retirées ;
- génération du document final.

### Objectifs
- audit ;
- débogage ;
- explicabilité des rapports produits.

---

## 16. Tests attendus

### 16.1. Tests unitaires
À prévoir sur :
- extracteurs ;
- normalisation ;
- validation ;
- règles métier ;
- calculateurs ;
- planification éditoriale ;
- builders ;
- writers.

### 16.2. Tests d’intégration
À prévoir sur :
- pipeline complet import → calcul → rapport ;
- persistance SQLite ;
- génération documentaire ;
- règles de suppression de sections ;
- cohérence des rapprochements entre appels et tickets.

### 16.3. Jeux de données de test
Prévoir des fixtures représentatives :
- cas nominal ;
- colonnes manquantes ;
- dates invalides ;
- homonymies agents ;
- données partielles ;
- cas sans EFI/EDI ;
- cas sans appels ;
- cas sans tickets ;
- cas avec sections à retirer.

---

## 17. Exigences de qualité

Le développement doit respecter les principes suivants :
- code typé ;
- séparation stricte des couches ;
- docstrings sur les classes et méthodes publiques ;
- tests unitaires et d’intégration ;
- architecture orientée maintenabilité ;
- composants remplaçables ;
- absence de logique métier dans les classes de rendu ;
- absence de logique de persistance dans les classes métier ;
- absence de logique métier lourde dans les extracteurs.

---

## 18. Séquence d’implémentation recommandée

### Lot 1 — Socle
- structure du projet ;
- modèles métier de base ;
- exceptions ;
- logging ;
- extracteurs CSV ;
- pipeline minimal de standardisation ;
- persistance SQLite.

### Lot 2 — Résolution métier
- normalisation avancée ;
- résolution agent ;
- résolution site ;
- règles de rapprochement appels / tickets.

### Lot 3 — Calculs
- calculateurs d’indicateurs ;
- agrégations par période ;
- stockage des KPI.

### Lot 4 — Reporting
- définitions de rapports ;
- évaluateur de sections ;
- planificateur ;
- builder rédactionnel ;
- `ReportModel`.

### Lot 5 — Export
- `AbstractWriter` ;
- `DocxWriter` ;
- éventuellement `MarkdownWriter`.

### Lot 6 — Exposition
- façade applicative ;
- CLI ;
- API HTTP FastAPI si nécessaire.

---

## 19. Décisions d’architecture à entériner

### Conservées
- usage de `pandas` pour extraction et transformation ;
- SQLite dans un premier temps ;
- writer abstrait ;
- prise en compte des sections conditionnelles.

### Modifiées par rapport à l’idée initiale
- le nettoyage n’est pas porté par `DataExtractor` ;
- la logique métier de rapprochement est sortie des extracteurs ;
- la préparation éditoriale est séparée du rendu ;
- le “vérificateur” devient :
  - `SectionEligibilityEvaluator`
  - `ReportPlanner`

### Supprimées
- classe unique qui fait extraction + nettoyage + calcul + enregistrement ;
- writer directement responsable de la logique métier du contenu.

---

## 20. Résumé de l’architecture cible

L’architecture cible repose sur la chaîne suivante :

**ingestion → standardisation → validation → résolution métier → calcul KPI → persistance → planification éditoriale → rédaction → rendu**

Cette architecture doit permettre :
- de fiabiliser les calculs ;
- d’expliciter les règles métier ;
- de produire des rapports robustes ;
- d’adapter facilement le contenu aux données réellement disponibles ;
- de faire évoluer le système sans remettre en cause les fondations.

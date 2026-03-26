# Feature 08 — Planification éditoriale et construction du modèle de rapport

    ## Identifiant
    `08_report_planning_and_builder`

    ## Branche recommandée
    `feature/report-planning-and-builder`

    ## Objectif
    Transformer les KPI en un modèle éditorial structuré, avec sections conditionnelles et contenu métier indépendant du format de sortie.

    ## Contraintes de développement à respecter
    Le développement doit respecter strictement les contraintes suivantes :
- code source dans `src/baobab_activity_reporting/` ;
- tests dans `tests/` avec une arborescence miroir du code ;
- documentation de développement dans `docs/` ;
- une classe par fichier ;
- programmation orientée classe ;
- noms de classes en `PascalCase`, modules en `snake_case` ;
- exceptions spécifiques au projet, héritant d’une exception de base ;
- annotations de type sur tous les paramètres, retours et attributs publics ;
- docstrings sur toutes les classes, méthodes et fonctions publiques ;
- configuration centralisée dans `pyproject.toml` pour black, pylint, mypy, flake8, bandit, pytest et coverage ;
- lignes limitées à 100 caractères ;
- couverture de tests minimale à 90 % ;
- fichiers de couverture dans `docs/tests/coverage` ;
- journal de développement dans `docs/dev_diary.md` ;
- versioning sémantique ;
- séparation des dépendances de production et de développement ;
- workflow Git avec une branche dédiée par feature, commits de type Conventional Commits, PR puis merge sur `main`.

    ## Périmètre inclus
- définitions de rapports
- contexte de génération
- évaluation d’éligibilité des sections
- planification du rapport
- construction des titres, tableaux, blocs narratifs et insights
- production d’un `ReportModel`

## Hors périmètre
- écriture DOCX ou Markdown
- API HTTP

## Classes ou composants attendus
- `ReportDefinition`
- `ReportContext`
- `SectionEligibilityEvaluator`
- `ReportPlanner`
- `NarrativeBuilder`
- `TableBuilder`
- `InsightBuilder`
- `ReportBuilder`
- `ReportModel`

## Exigences fonctionnelles détaillées
- la feature doit être autonome et testable indépendamment ;
- les erreurs métier ou techniques attendues doivent être représentées par des exceptions du projet ;
- les composants doivent être conçus pour être réutilisables dans le pipeline global ;
- la journalisation doit permettre de comprendre ce qui a été fait et ce qui a échoué.

## Exigences techniques détaillées
- une classe par fichier ;
- docstrings reStructuredText sur les éléments publics ;
- annotations de type complètes ;
- imports propres et API publique maîtrisée ;
- aucune logique hors responsabilité de la feature ;
- mise à jour du `docs/dev_diary.md` ;
- respect de la longueur maximale de 100 caractères par ligne.

## Tests attendus
- un fichier de tests par classe ;
- une classe de tests par fichier de tests ;
- cas nominaux ;
- cas d’erreur ;
- cas limites réalistes ;
- lorsque pertinent, tests d’intégration couvrant l’enchaînement de la feature dans le pipeline.

## Livrables attendus
- moteur de planification éditoriale
- moteur de construction du `ReportModel`
- tests de sections conditionnelles
- documentation des types de rapports

## Critères d’acceptation
- les sections sans données requises sont retirées automatiquement
- les rapports activité téléphonique, site et agent sont pris en charge
- la sortie est indépendante du format documentaire

## Dépendances
`07_kpi_computation`

## Vérifications finales attendues
- `black`, `pylint`, `mypy`, `flake8`, `bandit` et `pytest` passent ;
- la couverture de tests respecte le seuil minimal ;
- le code est prêt à être proposé en Pull Request.

## Fin de tâche attendue
La feature doit être développée dans la branche indiquée, avec des commits de type
Conventional Commits. Lorsque tous les tests et contrôles qualité sont au vert, il faut créer
une Pull Request puis la merger sur `main`.

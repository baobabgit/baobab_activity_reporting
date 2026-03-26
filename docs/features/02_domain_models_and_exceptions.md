# Feature 02 — Modèles métier fondamentaux et hiérarchie d’exceptions

    ## Identifiant
    `02_domain_models_and_exceptions`

    ## Branche recommandée
    `feature/domain-models-and-exceptions`

    ## Objectif
    Poser le vocabulaire métier et technique du projet afin de découpler le domaine des `DataFrame` et de standardiser la gestion des erreurs.

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
- création des modèles métier de base
- création des objets de résultat techniques
- création de la hiérarchie d’exceptions métier et techniques
- exports de packages utiles

## Hors périmètre
- lecture de fichiers
- persistance
- writers

## Classes ou composants attendus
- `ReportingPeriod`
- `Agent`
- `Site`
- `Kpi`
- `ExtractionResult`
- `ValidationResult`
- `SectionDecision`
- `DataAvailability`
- `ReportingError`
- `ExtractionError`
- `ValidationError`
- `StandardizationError`
- `ResolutionError`
- `PersistenceError`
- `ReportGenerationError`
- `WriterError`

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
- modèles métier importables
- exceptions dédiées par domaine
- tests unitaires par classe
- mise à jour de la documentation de domaine

## Critères d’acceptation
- chaque exception hérite de l’exception racine
- les modèles sont typés et documentés
- les cas de construction invalides sont testés
- aucune erreur mypy ni pylint

## Dépendances
`01_project_bootstrap`

## Vérifications finales attendues
- `black`, `pylint`, `mypy`, `flake8`, `bandit` et `pytest` passent ;
- la couverture de tests respecte le seuil minimal ;
- le code est prêt à être proposé en Pull Request.

## Fin de tâche attendue
La feature doit être développée dans la branche indiquée, avec des commits de type
Conventional Commits. Lorsque tous les tests et contrôles qualité sont au vert, il faut créer
une Pull Request puis la merger sur `main`.

# Journal de développement — baobab-activity-reporting

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

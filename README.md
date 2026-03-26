# baobab-activity-reporting

API Python de reporting d'activité pour Baobab.

## Description

Ce projet fournit une API Python capable de :

1. extraire des données issues de plusieurs fichiers sources ;
2. nettoyer, normaliser et valider ces données ;
3. appliquer des règles métier pour relier les données entre elles ;
4. calculer des indicateurs d'activité ;
5. stocker les données calculées ;
6. générer un rapport d'activité structuré et exportable.

## Installation

### Prérequis

- Python 3.10 ou supérieur

### Installation en mode développement

```bash
pip install -e ".[dev]"
```

## Utilisation

```python
from baobab_activity_reporting import PackageMetadata

meta = PackageMetadata()
print(meta.summary())
```

## Outils de qualité

Le projet utilise les outils suivants, tous configurés dans `pyproject.toml` :

| Outil   | Rôle                          |
|---------|-------------------------------|
| black   | Formatage automatique         |
| pylint  | Analyse statique              |
| flake8  | Vérification PEP 8            |
| mypy    | Vérification des types        |
| bandit  | Détection de vulnérabilités   |
| pytest  | Exécution des tests           |
| coverage| Couverture de code            |

### Lancer les vérifications

```bash
black --check src/ tests/
pylint src/
flake8 src/ tests/
mypy src/
bandit -r src/ -c pyproject.toml
pytest
```

## Structure du projet

```
src/
  baobab_activity_reporting/
    __init__.py
    core/
      __init__.py
      package_metadata.py
    exceptions/
      __init__.py
      application_exception.py
      configuration_exception.py
tests/
  baobab_activity_reporting/
    core/
      test_package_metadata.py
    exceptions/
      test_application_exception.py
      test_configuration_exception.py
docs/
  dev_diary.md
  tests/
    coverage/
```

## Versioning

Ce projet suit le [Semantic Versioning](https://semver.org/) (SemVer).

## Licence

MIT

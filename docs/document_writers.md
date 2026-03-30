# Writers documentaires

Les classes ``AbstractWriter``, ``DocxWriter`` et ``MarkdownWriter`` exportent
un ``ReportModel`` vers un fichier sans recalculer ni interpréter les règles
métier.

## Usage

```python
from pathlib import Path

from baobab_activity_reporting import ReportModel
from baobab_activity_reporting.reporting.writers.docx_writer import DocxWriter
from baobab_activity_reporting.reporting.writers.markdown_writer import (
    MarkdownWriter,
)

model = ReportModel(...)  # construit par ReportBuilder
DocxWriter().write(model, Path("sortie.docx"))
MarkdownWriter().write(model, Path("sortie.md"))
```

## Formats

| Writer | Extension | Dépendance |
|--------|-----------|------------|
| ``DocxWriter`` | ``.docx`` | ``python-docx`` (production) |
| ``MarkdownWriter`` | ``.md`` | aucune (stdlib) |

## Structure rendue

- **DOCX** : style titre (niveau 0), période en italique, préambule, sections en
  titre 1, tableaux avec grille Word, points saillants en liste à puces.
- **Markdown** : titre ``#``, sections ``##``, tableaux GFM, insights en liste
  ``-`` ; pipes des cellules échappés par ``\\|``.

## Erreurs

Les échecs d'I/O ou de rendu sont levés comme ``WriterError`` (format
``output_format`` renseigné).

## Limites

- Styles Word dépendants du gabarit par défaut de ``python-docx``.
- Pas de personnalisation de charte graphique dans cette version.

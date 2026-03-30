"""Module contenant la classe abstraite des writers documentaires."""

from abc import ABC, abstractmethod
from pathlib import Path

from baobab_activity_reporting.reporting.report_model import ReportModel


class AbstractWriter(ABC):
    """Contrat commun pour exporter un :class:`ReportModel` vers un fichier.

    Les implémentations ne doivent contenir aucune règle métier : uniquement
    la projection structurelle (titres, paragraphes, tableaux) vers le format
    cible.

    :Example:
        >>> from pathlib import Path
        >>> from baobab_activity_reporting.reporting.report_model import (
        ...     ReportModel,
        ... )
        >>> class DummyWriter(AbstractWriter):
        ...     @property
        ...     def output_format(self) -> str:
        ...         return "dummy"
        ...     def write(self, model: ReportModel, output_path: Path | str) -> None:
        ...         Path(output_path).write_text(model.title, encoding="utf-8")
        >>> w = DummyWriter()
        >>> isinstance(w.output_format, str)
        True
    """

    @property
    @abstractmethod
    def output_format(self) -> str:
        """Identifiant du format produit (ex. ``docx``, ``markdown``).

        :return: Nom court du format.
        :rtype: str
        """

    @abstractmethod
    def write(self, model: ReportModel, output_path: Path | str) -> None:
        """Sérialise ``model`` dans le fichier ``output_path``.

        :param model: Contenu éditorial à rendre.
        :type model: ReportModel
        :param output_path: Chemin de sortie (créé ou écrasé selon le format).
        :type output_path: Path | str
        :raises WriterError: En cas d'échec d'écriture ou de rendu.
        """

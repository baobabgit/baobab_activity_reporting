"""Module contenant l'extracteur abstrait."""

import logging
from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

from baobab_activity_reporting.domain.results.extraction_result import (
    ExtractionResult,
)
from baobab_activity_reporting.exceptions.extraction_error import (
    ExtractionError,
)
from baobab_activity_reporting.ingestion.extractors.csv_extraction_configuration import (
    CsvExtractionConfiguration,
)

logger = logging.getLogger(__name__)


class BaseExtractor(ABC):
    """Extracteur abstrait de fichiers CSV.

    Définit le contrat d'extraction et fournit la logique
    commune de lecture CSV. Les sous-classes doivent fournir
    leur propre :class:`CsvExtractionConfiguration`.

    :param configuration: Configuration de lecture CSV.
    :type configuration: CsvExtractionConfiguration

    :Example:
        >>> class MyExtractor(BaseExtractor):
        ...     def _build_configuration(self) -> CsvExtractionConfiguration:
        ...         return CsvExtractionConfiguration()
    """

    def __init__(self, configuration: CsvExtractionConfiguration) -> None:
        """Initialise l'extracteur avec sa configuration.

        :param configuration: Configuration de lecture CSV.
        :type configuration: CsvExtractionConfiguration
        """
        self.configuration: CsvExtractionConfiguration = configuration

    @abstractmethod
    def _build_configuration(self) -> CsvExtractionConfiguration:
        """Construit la configuration par défaut de l'extracteur.

        :return: Configuration de lecture CSV.
        :rtype: CsvExtractionConfiguration
        """

    def extract(self, source_path: str) -> ExtractionResult:
        """Extrait les données d'un fichier CSV.

        Lit le fichier indiqué par ``source_path`` en utilisant
        la configuration de l'extracteur, puis retourne un
        :class:`ExtractionResult` contenant les métadonnées.

        :param source_path: Chemin vers le fichier CSV.
        :type source_path: str
        :return: Résultat de l'extraction.
        :rtype: ExtractionResult
        :raises ExtractionError: Si le fichier est introuvable
            ou si la lecture échoue.
        """
        path = Path(source_path)
        source_name = path.name
        config = self.configuration

        logger.info(
            "Début extraction : %s (label=%s)",
            source_name,
            config.source_label,
        )

        if not path.exists():
            raise ExtractionError(
                "Fichier introuvable",
                source_name=source_name,
                details=str(path),
            )

        if not path.is_file():
            raise ExtractionError(
                "Le chemin ne désigne pas un fichier",
                source_name=source_name,
                details=str(path),
            )

        try:
            dataframe = pd.read_csv(
                path,
                sep=config.separator,
                encoding=config.encoding,
                skiprows=config.skip_rows,
            )
        except Exception as exc:
            raise ExtractionError(
                "Échec de lecture du fichier CSV",
                source_name=source_name,
                details=str(exc),
            ) from exc

        warnings: list[str] = []
        column_names = list(dataframe.columns.astype(str))

        if config.expected_columns:
            missing = set(config.expected_columns) - set(column_names)
            if missing:
                sorted_missing = sorted(missing)
                warnings.append(f"Colonnes attendues manquantes : {sorted_missing}")
                logger.warning(
                    "Colonnes manquantes dans %s : %s",
                    source_name,
                    sorted_missing,
                )

        row_count = len(dataframe)

        logger.info(
            "Extraction terminée : %s — %d lignes, %d colonnes",
            source_name,
            row_count,
            len(column_names),
        )

        return ExtractionResult(
            source_name=source_name,
            row_count=row_count,
            column_names=column_names,
            warnings=warnings if warnings else None,
        )

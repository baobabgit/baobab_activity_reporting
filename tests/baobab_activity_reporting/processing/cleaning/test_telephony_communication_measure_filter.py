"""Tests du filtre mesure « Durée de communication »."""

import pandas as pd

from baobab_activity_reporting.processing.cleaning.telephony_communication_measure_filter import (
    filter_communication_duration_rows,
)
from baobab_activity_reporting.processing.kpi.consolidated_data_schema import (
    ConsolidatedDataSchema,
)


class TestFilterCommunicationDurationRows:
    """Tests pour :func:`filter_communication_duration_rows`."""

    def test_keeps_only_communication_rows(self) -> None:
        """Ne conserve que les lignes dont la mesure est communication."""
        col = ConsolidatedDataSchema.COL_MEASURE_NAMES
        df = pd.DataFrame(
            {
                col: [
                    "Durée de mise en garde",
                    "Durée de communication",
                    "Durée de communication",
                ],
                "x": [1, 2, 3],
            },
        )
        out, excluded = filter_communication_duration_rows(df)
        assert len(out) == 2
        assert excluded == 1
        assert list(out["x"]) == [2, 3]

    def test_strips_whitespace(self) -> None:
        """Égalité après strip sur le libellé de mesure."""
        col = ConsolidatedDataSchema.COL_MEASURE_NAMES
        df = pd.DataFrame({col: ["  Durée de communication  "], "x": [1]})
        out, excluded = filter_communication_duration_rows(df)
        assert len(out) == 1
        assert excluded == 0

    def test_empty_frame(self) -> None:
        """DataFrame vide."""
        df = pd.DataFrame()
        out, excluded = filter_communication_duration_rows(df)
        assert len(out) == 0
        assert excluded == 0

    def test_missing_column_noop(self) -> None:
        """Sans colonne de mesure, pas de filtrage."""
        df = pd.DataFrame({"a": [1, 2]})
        out, excluded = filter_communication_duration_rows(df)
        assert len(out) == 2
        assert excluded == 0

"""Tests pour NarrativeKpiAccessor."""

from baobab_activity_reporting.reporting.narrative_kpi_accessor import (
    NarrativeKpiAccessor,
)


class TestNarrativeKpiAccessor:
    """Tests unitaires pour NarrativeKpiAccessor."""

    def test_is_global_telephony_code(self) -> None:
        """Exclusion agent et site dans le filtre global."""
        assert NarrativeKpiAccessor.is_global_telephony_code("telephony.incoming.count")
        assert not NarrativeKpiAccessor.is_global_telephony_code("agent.A.telephony.incoming.count")
        assert not NarrativeKpiAccessor.is_global_telephony_code(
            "site.Paris.telephony.incoming.count"
        )

    def test_channel_label_and_volume(self) -> None:
        """Extraction libellé / volume canal."""
        row = {"code": "tickets.channel.EFI.count", "label": "Espace EFI", "value": 12.0}
        pair = NarrativeKpiAccessor.channel_label_and_volume(row)
        assert pair is not None
        assert pair[0] == "Espace EFI"
        assert pair[1] == 12.0

    def test_dimension_totals_agent(self) -> None:
        """Agrégation par agent."""
        rows = [
            {"code": "agent.Jean.telephony.incoming.count", "value": 2.0},
            {"code": "agent.Jean.tickets.count", "value": 3.0},
            {"code": "agent.Marie.telephony.incoming.count", "value": 4.0},
        ]
        totals = NarrativeKpiAccessor.dimension_totals(rows, "agent.")
        assert totals[0][0] == "Jean"
        assert totals[0][1] == 5.0
        assert totals[1][0] == "Marie"
        assert totals[1][1] == 4.0

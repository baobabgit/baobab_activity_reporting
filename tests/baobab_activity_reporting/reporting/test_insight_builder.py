"""Tests unitaires pour InsightBuilder."""

from baobab_activity_reporting.reporting.insight_builder import InsightBuilder


class TestInsightBuilder:
    """Tests pour la classe InsightBuilder."""

    def test_telephony_balance(self) -> None:
        """Vérifie l'insight de répartition."""
        kpis = [
            {"code": "telephony.incoming.count", "value": 10.0},
            {"code": "telephony.outgoing.count", "value": 10.0},
        ]
        out = InsightBuilder().telephony_balance_insights(kpis)
        assert len(out) >= 1
        assert "%" in out[0]

    def test_channel_mix(self) -> None:
        """Vérifie le mix canaux."""
        kpis = [
            {"code": "tickets.channel.EFI.count", "value": 30.0},
            {"code": "tickets.channel.EDI.count", "value": 70.0},
        ]
        lines = InsightBuilder().channel_mix_insights(kpis)
        assert len(lines) == 2

    def test_generic_highlights(self) -> None:
        """Liste les valeurs numériques."""
        kpis = [{"code": "a.b", "label": "L", "value": 2.0, "unit": "x"}]
        g = InsightBuilder().generic_numeric_highlights(kpis)
        assert any("L" in s for s in g)

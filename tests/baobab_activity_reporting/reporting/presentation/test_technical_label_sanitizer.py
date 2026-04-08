"""Tests pour TechnicalLabelSanitizer."""

from baobab_activity_reporting.reporting.presentation.technical_label_sanitizer import (
    TechnicalLabelSanitizer,
)


class TestTechnicalLabelSanitizer:
    """Nettoyage des libellés."""

    def test_whitespace_collapsed(self) -> None:
        """Espaces normalisés."""
        assert TechnicalLabelSanitizer.sanitize("  a  b  ") == "a b"

    def test_short_from_code(self) -> None:
        """Fallback sans libellé."""
        text = TechnicalLabelSanitizer.short_indicator_from_code("telephony.incoming.count")
        assert "volume" in text.lower() or "incoming" in text.lower()

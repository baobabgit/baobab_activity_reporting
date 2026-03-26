"""Tests unitaires pour ValidationResult et classes associées."""

from baobab_activity_reporting.domain.results.validation_result import (
    Severity,
    ValidationMessage,
    ValidationResult,
)


class TestSeverity:
    """Tests pour l'énumération Severity."""

    def test_error_value(self) -> None:
        """Vérifie la valeur de ERROR."""
        assert Severity.ERROR.value == "error"

    def test_warning_value(self) -> None:
        """Vérifie la valeur de WARNING."""
        assert Severity.WARNING.value == "warning"

    def test_info_value(self) -> None:
        """Vérifie la valeur de INFO."""
        assert Severity.INFO.value == "info"


class TestValidationMessage:
    """Tests pour la classe ValidationMessage."""

    def test_creation(self) -> None:
        """Vérifie la création d'un message."""
        msg = ValidationMessage(Severity.ERROR, "COL_MISS", "Colonne absente")
        assert msg.severity == Severity.ERROR
        assert msg.code == "COL_MISS"
        assert msg.text == "Colonne absente"

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        msg = ValidationMessage(Severity.WARNING, "W001", "Texte")
        result = repr(msg)
        assert "ValidationMessage(" in result
        assert "W001" in result


class TestValidationResult:
    """Tests pour la classe ValidationResult."""

    def test_creation_empty(self) -> None:
        """Vérifie la création sans messages."""
        result = ValidationResult()
        assert result.messages == []

    def test_creation_with_messages(self) -> None:
        """Vérifie la création avec des messages."""
        msgs = [ValidationMessage(Severity.INFO, "I001", "Info")]
        result = ValidationResult(messages=msgs)
        assert len(result.messages) == 1

    def test_is_valid_empty(self) -> None:
        """Vérifie is_valid sans messages."""
        result = ValidationResult()
        assert result.is_valid is True

    def test_is_valid_with_warnings_only(self) -> None:
        """Vérifie is_valid avec seulement des warnings."""
        result = ValidationResult()
        result.add_warning("W001", "Avertissement")
        assert result.is_valid is True

    def test_is_valid_false_with_error(self) -> None:
        """Vérifie is_valid=False avec une erreur."""
        result = ValidationResult()
        result.add_error("E001", "Erreur")
        assert result.is_valid is False

    def test_add_error(self) -> None:
        """Vérifie l'ajout d'une erreur."""
        result = ValidationResult()
        result.add_error("E001", "Texte erreur")
        assert len(result.errors) == 1
        assert result.errors[0].severity == Severity.ERROR
        assert result.errors[0].code == "E001"

    def test_add_warning(self) -> None:
        """Vérifie l'ajout d'un avertissement."""
        result = ValidationResult()
        result.add_warning("W001", "Texte warning")
        assert len(result.warning_list) == 1
        assert result.warning_list[0].severity == Severity.WARNING

    def test_add_info(self) -> None:
        """Vérifie l'ajout d'une info."""
        result = ValidationResult()
        result.add_info("I001", "Texte info")
        assert len(result.messages) == 1
        assert result.messages[0].severity == Severity.INFO

    def test_errors_filter(self) -> None:
        """Vérifie le filtre des erreurs."""
        result = ValidationResult()
        result.add_error("E001", "Err")
        result.add_warning("W001", "Warn")
        result.add_info("I001", "Info")
        assert len(result.errors) == 1

    def test_warning_list_filter(self) -> None:
        """Vérifie le filtre des warnings."""
        result = ValidationResult()
        result.add_error("E001", "Err")
        result.add_warning("W001", "Warn")
        result.add_warning("W002", "Warn2")
        assert len(result.warning_list) == 2

    def test_messages_is_copy(self) -> None:
        """Vérifie que la liste initiale est une copie."""
        msgs = [ValidationMessage(Severity.INFO, "I", "t")]
        result = ValidationResult(messages=msgs)
        msgs.append(ValidationMessage(Severity.ERROR, "E", "e"))
        assert len(result.messages) == 1

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        result = ValidationResult()
        result.add_error("E001", "Err")
        text = repr(result)
        assert "ValidationResult(" in text
        assert "is_valid=False" in text
        assert "message_count=1" in text

    def test_multiple_errors_all_returned(self) -> None:
        """Vérifie que toutes les erreurs sont retournées."""
        result = ValidationResult()
        result.add_error("E001", "Err1")
        result.add_error("E002", "Err2")
        assert len(result.errors) == 2
        assert result.is_valid is False

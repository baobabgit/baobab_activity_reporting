"""Module contenant le résultat de validation."""

from enum import Enum


class Severity(Enum):
    """Niveau de sévérité d'un message de validation.

    :cvar ERROR: Erreur bloquante.
    :cvar WARNING: Avertissement non bloquant.
    :cvar INFO: Information.
    """

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationMessage:
    """Message individuel de validation.

    :param severity: Niveau de sévérité.
    :type severity: Severity
    :param code: Code du contrôle.
    :type code: str
    :param text: Texte descriptif.
    :type text: str
    """

    def __init__(
        self,
        severity: Severity,
        code: str,
        text: str,
    ) -> None:
        """Initialise un message de validation.

        :param severity: Niveau de sévérité.
        :type severity: Severity
        :param code: Code du contrôle.
        :type code: str
        :param text: Texte descriptif.
        :type text: str
        """
        self.severity: Severity = severity
        self.code: str = code
        self.text: str = text

    def __repr__(self) -> str:
        """Retourne une représentation technique du message.

        :return: Représentation technique.
        :rtype: str
        """
        return (
            f"ValidationMessage("
            f"severity={self.severity!r}, "
            f"code={self.code!r}, "
            f"text={self.text!r})"
        )


class ValidationResult:
    """Résultat agrégé d'une opération de validation.

    Regroupe l'ensemble des messages de validation
    et offre un accès rapide au verdict global.

    :param messages: Liste des messages de validation.
    :type messages: list[ValidationMessage]

    :Example:
        >>> result = ValidationResult()
        >>> result.add_error("COL_MISSING", "Colonne 'date' absente")
        >>> print(result.is_valid)
        False
    """

    def __init__(
        self,
        messages: list[ValidationMessage] | None = None,
    ) -> None:
        """Initialise le résultat de validation.

        :param messages: Liste initiale de messages.
        :type messages: list[ValidationMessage] | None
        """
        self.messages: list[ValidationMessage] = list(messages) if messages is not None else []

    @property
    def is_valid(self) -> bool:
        """Indique si la validation est passée sans erreur bloquante.

        :return: ``True`` si aucun message de sévérité ``ERROR``.
        :rtype: bool
        """
        return not any(m.severity == Severity.ERROR for m in self.messages)

    @property
    def errors(self) -> list[ValidationMessage]:
        """Retourne les messages d'erreur.

        :return: Liste des messages de sévérité ``ERROR``.
        :rtype: list[ValidationMessage]
        """
        return [m for m in self.messages if m.severity == Severity.ERROR]

    @property
    def warning_list(self) -> list[ValidationMessage]:
        """Retourne les avertissements.

        :return: Liste des messages de sévérité ``WARNING``.
        :rtype: list[ValidationMessage]
        """
        return [m for m in self.messages if m.severity == Severity.WARNING]

    def add_error(self, code: str, text: str) -> None:
        """Ajoute un message d'erreur.

        :param code: Code du contrôle.
        :type code: str
        :param text: Texte descriptif.
        :type text: str
        """
        self.messages.append(ValidationMessage(Severity.ERROR, code, text))

    def add_warning(self, code: str, text: str) -> None:
        """Ajoute un avertissement.

        :param code: Code du contrôle.
        :type code: str
        :param text: Texte descriptif.
        :type text: str
        """
        self.messages.append(ValidationMessage(Severity.WARNING, code, text))

    def add_info(self, code: str, text: str) -> None:
        """Ajoute un message d'information.

        :param code: Code du contrôle.
        :type code: str
        :param text: Texte descriptif.
        :type text: str
        """
        self.messages.append(ValidationMessage(Severity.INFO, code, text))

    def __repr__(self) -> str:
        """Retourne une représentation technique du résultat.

        :return: Représentation technique.
        :rtype: str
        """
        return (
            f"ValidationResult("
            f"is_valid={self.is_valid!r}, "
            f"message_count={len(self.messages)})"
        )

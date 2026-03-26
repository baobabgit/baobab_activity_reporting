"""Module contenant le modèle Kpi."""

from baobab_activity_reporting.exceptions.validation_error import (
    ValidationError,
)


class Kpi:
    """Représente un indicateur clé de performance calculé.

    Encapsule le code, le libellé, la valeur et l'unité
    d'un indicateur d'activité.

    :param code: Code unique de l'indicateur (ex: ``"nb_appels_entrants"``).
    :type code: str
    :param label: Libellé lisible de l'indicateur.
    :type label: str
    :param value: Valeur numérique de l'indicateur.
    :type value: float
    :param unit: Unité de mesure (ex: ``"appels"``, ``"%"``).
    :type unit: str | None

    :raises ValidationError: Si ``code`` ou ``label`` est vide.

    :Example:
        >>> kpi = Kpi("nb_appels", "Nombre d'appels", 142.0, "appels")
        >>> print(kpi.formatted_value)
        142.0 appels
    """

    def __init__(
        self,
        code: str,
        label: str,
        value: float,
        unit: str | None = None,
    ) -> None:
        """Initialise un KPI.

        :param code: Code unique de l'indicateur.
        :type code: str
        :param label: Libellé lisible.
        :type label: str
        :param value: Valeur numérique.
        :type value: float
        :param unit: Unité de mesure.
        :type unit: str | None
        :raises ValidationError: Si un champ obligatoire est vide.
        """
        if not code.strip():
            raise ValidationError(
                "Le code du KPI ne peut pas être vide",
                field_name="code",
            )
        if not label.strip():
            raise ValidationError(
                "Le libellé du KPI ne peut pas être vide",
                field_name="label",
            )
        self.code: str = code.strip()
        self.label: str = label.strip()
        self.value: float = value
        self.unit: str | None = unit.strip() if unit is not None else None

    @property
    def formatted_value(self) -> str:
        """Retourne la valeur formatée avec son unité.

        :return: Valeur suivie de l'unité, ou la valeur seule.
        :rtype: str
        """
        if self.unit is not None:
            return f"{self.value} {self.unit}"
        return str(self.value)

    def __eq__(self, other: object) -> bool:
        """Vérifie l'égalité entre deux KPI par code.

        :param other: Objet à comparer.
        :type other: object
        :return: ``True`` si les codes sont identiques.
        :rtype: bool
        """
        if not isinstance(other, Kpi):
            return NotImplemented
        return self.code == other.code

    def __hash__(self) -> int:
        """Retourne le hash basé sur le code du KPI.

        :return: Valeur de hash.
        :rtype: int
        """
        return hash(self.code)

    def __repr__(self) -> str:
        """Retourne une représentation technique du KPI.

        :return: Représentation technique.
        :rtype: str
        """
        return (
            f"Kpi(code={self.code!r}, "
            f"label={self.label!r}, "
            f"value={self.value!r}, "
            f"unit={self.unit!r})"
        )

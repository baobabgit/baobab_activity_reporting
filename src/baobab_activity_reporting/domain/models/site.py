"""Module contenant le modèle Site."""

from baobab_activity_reporting.exceptions.validation_error import (
    ValidationError,
)


class Site:
    """Représente un site physique du centre de contact.

    Encapsule l'identité et la localisation d'un site
    sur lequel opèrent des agents.

    :param site_id: Identifiant unique du site.
    :type site_id: str
    :param name: Nom du site.
    :type name: str
    :param label: Libellé d'affichage du site.
    :type label: str | None

    :raises ValidationError: Si ``site_id`` ou ``name`` est vide.

    :Example:
        >>> site = Site("S01", "Paris Nord")
        >>> print(site.display_label)
        Paris Nord
    """

    def __init__(
        self,
        site_id: str,
        name: str,
        label: str | None = None,
    ) -> None:
        """Initialise un site.

        :param site_id: Identifiant unique du site.
        :type site_id: str
        :param name: Nom du site.
        :type name: str
        :param label: Libellé d'affichage.
        :type label: str | None
        :raises ValidationError: Si un champ obligatoire est vide.
        """
        if not site_id.strip():
            raise ValidationError(
                "L'identifiant du site ne peut pas être vide",
                field_name="site_id",
            )
        if not name.strip():
            raise ValidationError(
                "Le nom du site ne peut pas être vide",
                field_name="name",
            )
        self.site_id: str = site_id.strip()
        self.name: str = name.strip()
        self.label: str | None = label.strip() if label is not None else None

    @property
    def display_label(self) -> str:
        """Retourne le libellé d'affichage du site.

        Utilise le ``label`` s'il est défini, sinon le ``name``.

        :return: Libellé d'affichage.
        :rtype: str
        """
        return self.label if self.label is not None else self.name

    def __eq__(self, other: object) -> bool:
        """Vérifie l'égalité entre deux sites par identifiant.

        :param other: Objet à comparer.
        :type other: object
        :return: ``True`` si les identifiants sont identiques.
        :rtype: bool
        """
        if not isinstance(other, Site):
            return NotImplemented
        return self.site_id == other.site_id

    def __hash__(self) -> int:
        """Retourne le hash basé sur l'identifiant du site.

        :return: Valeur de hash.
        :rtype: int
        """
        return hash(self.site_id)

    def __repr__(self) -> str:
        """Retourne une représentation technique du site.

        :return: Représentation technique.
        :rtype: str
        """
        return f"Site(site_id={self.site_id!r}, " f"name={self.name!r}, " f"label={self.label!r})"

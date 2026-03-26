"""Module contenant le modèle Agent."""

from baobab_activity_reporting.exceptions.validation_error import (
    ValidationError,
)


class Agent:
    """Représente un agent du centre de contact.

    Encapsule l'identité d'un agent impliqué dans le
    traitement des appels et des tickets.

    :param agent_id: Identifiant unique de l'agent.
    :type agent_id: str
    :param last_name: Nom de famille de l'agent.
    :type last_name: str
    :param first_name: Prénom de l'agent.
    :type first_name: str
    :param site_name: Nom du site de rattachement.
    :type site_name: str | None

    :raises ValidationError: Si ``agent_id``, ``last_name`` ou
        ``first_name`` est vide.

    :Example:
        >>> agent = Agent("A001", "Dupont", "Marie")
        >>> print(agent.full_name)
        Marie Dupont
    """

    def __init__(
        self,
        agent_id: str,
        last_name: str,
        first_name: str,
        site_name: str | None = None,
    ) -> None:
        """Initialise un agent.

        :param agent_id: Identifiant unique de l'agent.
        :type agent_id: str
        :param last_name: Nom de famille.
        :type last_name: str
        :param first_name: Prénom.
        :type first_name: str
        :param site_name: Nom du site de rattachement.
        :type site_name: str | None
        :raises ValidationError: Si un champ obligatoire est vide.
        """
        if not agent_id.strip():
            raise ValidationError(
                "L'identifiant de l'agent ne peut pas être vide",
                field_name="agent_id",
            )
        if not last_name.strip():
            raise ValidationError(
                "Le nom de l'agent ne peut pas être vide",
                field_name="last_name",
            )
        if not first_name.strip():
            raise ValidationError(
                "Le prénom de l'agent ne peut pas être vide",
                field_name="first_name",
            )
        self.agent_id: str = agent_id.strip()
        self.last_name: str = last_name.strip()
        self.first_name: str = first_name.strip()
        self.site_name: str | None = site_name.strip() if site_name is not None else None

    @property
    def full_name(self) -> str:
        """Retourne le nom complet de l'agent.

        :return: Prénom suivi du nom de famille.
        :rtype: str
        """
        return f"{self.first_name} {self.last_name}"

    def __eq__(self, other: object) -> bool:
        """Vérifie l'égalité entre deux agents par identifiant.

        :param other: Objet à comparer.
        :type other: object
        :return: ``True`` si les identifiants sont identiques.
        :rtype: bool
        """
        if not isinstance(other, Agent):
            return NotImplemented
        return self.agent_id == other.agent_id

    def __hash__(self) -> int:
        """Retourne le hash basé sur l'identifiant de l'agent.

        :return: Valeur de hash.
        :rtype: int
        """
        return hash(self.agent_id)

    def __repr__(self) -> str:
        """Retourne une représentation technique de l'agent.

        :return: Représentation technique.
        :rtype: str
        """
        return (
            f"Agent(agent_id={self.agent_id!r}, "
            f"last_name={self.last_name!r}, "
            f"first_name={self.first_name!r}, "
            f"site_name={self.site_name!r})"
        )

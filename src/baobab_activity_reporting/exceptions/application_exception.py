"""Module contenant l'exception de base du projet."""


class ApplicationException(Exception):
    """Exception de base pour toutes les erreurs applicatives du projet.

    Toutes les exceptions spécifiques au projet doivent hériter
    de cette classe afin de permettre une capture uniforme des
    erreurs applicatives.

    :param message: Message décrivant l'erreur.
    :type message: str
    :param details: Détails complémentaires sur l'erreur.
    :type details: str | None

    :Example:
        >>> raise ApplicationException("Une erreur est survenue")
    """

    def __init__(self, message: str, details: str | None = None) -> None:
        """Initialise l'exception applicative.

        :param message: Message décrivant l'erreur.
        :type message: str
        :param details: Détails complémentaires sur l'erreur.
        :type details: str | None
        """
        self.message: str = message
        self.details: str | None = details
        full_message = message if details is None else f"{message} — {details}"
        super().__init__(full_message)

    def __str__(self) -> str:
        """Retourne une représentation lisible de l'exception.

        :return: Le message de l'exception avec ses détails éventuels.
        :rtype: str
        """
        if self.details is None:
            return self.message
        return f"{self.message} — {self.details}"

    def __repr__(self) -> str:
        """Retourne une représentation technique de l'exception.

        :return: Représentation technique incluant la classe et le message.
        :rtype: str
        """
        class_name = type(self).__name__
        return f"{class_name}(message={self.message!r}, details={self.details!r})"

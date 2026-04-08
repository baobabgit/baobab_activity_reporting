"""Identifiants stables pour classifier les décisions d'éligibilité de section."""


class SectionEligibilityCodes:
    """Codes machine pour tests, logs et diagnostics (pas de rendu documentaire).

    :cvar MIN_DATA_SATISFIED: Jeu minimal de données utiles présent.
    :cvar TELEPHONY_PARTIAL_SINGLE_LEG: Une seule jambe téléphonique active.
    :cvar TELEPHONY_BALANCED: Entrants et sortants portent de l'activité.
    :cvar EXCLUDED_NO_TELEPHONY_METRICS: Aucun indicateur téléphonique global exploitable.
    :cvar EXCLUDED_TELEPHONY_VALUES_UNRELIABLE: Valeurs téléphonie incohérentes ou invalides.
    :cvar EXCLUDED_NO_TICKET_VOLUME: Aucun volume ticket canal exploitable.
    :cvar EXCLUDED_TICKET_VALUES_UNRELIABLE: Valeurs tickets invalides.
    :cvar EXCLUDED_INSUFFICIENT_BREAKDOWN_DIMENSIONS: Pas assez de dimensions pour une ventilation.
    :cvar EXCLUDED_NO_ATTENTION_SIGNALS: Aucun signal d'anomalie détecté.
    :cvar ATTENTION_IMBALANCE_TELEPHONY: Déséquilibre entrants / sortants.
    :cvar ATTENTION_TICKET_CHANNEL_DOMINANCE: Canal ticket dominant.
    :cvar EXCLUDED_NO_EXPLOITABLE_PEER_SECTIONS: Conclusion sans autre section à contenu.
    :cvar CONCLUSION_ALLOWED: Conclusion autorisée par les sections pairs.
    :cvar PREFIX_GATE_PASSED: Ancienne porte par préfixes satisfaite.
    :cvar PREFIX_GATE_FAILED: Aucun KPI pour les préfixes attendus.
    :cvar MANDATORY_DEGRADED: Section obligatoire sans données (mode dégradé).
    :cvar ALWAYS_VISIBLE: Section toujours affichée (synthèse).
    """

    MIN_DATA_SATISFIED = "min_data_satisfied"
    TELEPHONY_PARTIAL_SINGLE_LEG = "telephony_partial_single_leg"
    TELEPHONY_BALANCED = "telephony_balanced"
    EXCLUDED_NO_TELEPHONY_METRICS = "excluded_no_telephony_metrics"
    EXCLUDED_TELEPHONY_VALUES_UNRELIABLE = "excluded_telephony_values_unreliable"
    EXCLUDED_NO_TICKET_VOLUME = "excluded_no_ticket_volume"
    EXCLUDED_TICKET_VALUES_UNRELIABLE = "excluded_ticket_values_unreliable"
    EXCLUDED_INSUFFICIENT_BREAKDOWN_DIMENSIONS = "excluded_insufficient_breakdown_dimensions"
    EXCLUDED_NO_ATTENTION_SIGNALS = "excluded_no_attention_signals"
    ATTENTION_IMBALANCE_TELEPHONY = "attention_imbalance_telephony"
    ATTENTION_TICKET_CHANNEL_DOMINANCE = "attention_ticket_channel_dominance"
    EXCLUDED_NO_EXPLOITABLE_PEER_SECTIONS = "excluded_no_exploitable_peer_sections"
    CONCLUSION_ALLOWED = "conclusion_allowed"
    PREFIX_GATE_PASSED = "prefix_gate_passed"
    PREFIX_GATE_FAILED = "prefix_gate_failed"
    MANDATORY_DEGRADED = "mandatory_degraded"
    ALWAYS_VISIBLE = "always_visible"

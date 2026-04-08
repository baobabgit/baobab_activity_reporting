"""Rédaction narrative de l'activité téléphonique."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.narrative_kpi_accessor import (
    NarrativeKpiAccessor,
)
from baobab_activity_reporting.reporting.presentation.duration_formatter import (
    DurationFormatter,
)
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class TelephonyActivityNarrativeWriter:
    """Interprète volumes et durées téléphoniques sans recopier les tableaux."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit un ou deux paragraphes.

        :param ctx: Contexte ; ``kpi_rows`` contient la téléphonie filtrée.
        :return: Paragraphes texte brut.
        """
        if ctx.status == SectionStatus.DEGRADED:
            return [self._degraded(ctx)]

        rows = ctx.kpi_rows
        inc, outg = NarrativeKpiAccessor.incoming_outgoing_counts(rows)
        dur_in = NarrativeKpiAccessor.numeric_for_code(
            rows,
            "telephony.incoming.duration_seconds.sum",
        )
        dur_out = NarrativeKpiAccessor.numeric_for_code(
            rows,
            "telephony.outgoing.duration_seconds.sum",
        )

        if inc is None and outg is None:
            return [
                "Les agrégats téléphoniques attendus sont absents : "
                "aucune lecture de volume n'est possible sur cette section."
            ]

        p1_parts: list[str] = []
        if inc is not None and outg is not None and (inc + outg) > 0:
            total = inc + outg
            ratio_in = 100.0 * inc / total
            p1_parts.append(
                f"L'activité se partage entre environ {int(round(inc))} appels entrants "
                f"et {int(round(outg))} sortants ; les entrants représentent environ "
                f"{ratio_in:.0f} % du flux."
            )
        elif inc is not None:
            p1_parts.append(
                f"Le volet entrant domine la photographie avec environ {int(round(inc))} "
                f"appels ; les sortants ne sont pas renseignés de manière comparable."
            )
        elif outg is not None:
            p1_parts.append(
                f"L'activité sortante atteint environ {int(round(outg))} appels "
                f"tandis que le volet entrant manque ou reste nul sur la période."
            )

        p1 = " ".join(p1_parts)

        p2: str | None = None
        if dur_in is not None or dur_out is not None:
            di = DurationFormatter.format_seconds(dur_in or 0.0) if dur_in is not None else None
            do = DurationFormatter.format_seconds(dur_out or 0.0) if dur_out is not None else None
            if di and do and di != "—" and do != "—":
                p2 = (
                    f"Les durées cumulées suggèrent un temps de conversation total d'environ {di} "
                    f"côté entrant et {do} côté sortant, à rapprocher des volumes pour juger "
                    f"l'intensité."
                )
            elif di and di != "—":
                p2 = (
                    f"La charge conversationnelle entrante s'exprime surtout par une durée "
                    f"cumulée d'environ {di}."
                )
            elif do and do != "—":
                p2 = f"La charge sortante se lit aussi à travers une durée cumulée d'environ {do}."

        if p2:
            return [p1, p2]
        return [p1]

    @staticmethod
    def _degraded(ctx: SectionEditorialContext) -> str:
        """Texte pour section téléphonie en mode dégradé."""
        base = ctx.section_objective or "Décrire l'activité téléphonique."
        return (
            f"{base} Les indicateurs agrégés ne sont pas disponibles ou sont jugés non fiables "
            f"pour la période du {ctx.period_start} au {ctx.period_end}."
        )

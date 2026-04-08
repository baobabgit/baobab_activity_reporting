"""Point d'entrée CLI : import, calcul KPI, génération de rapport."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import date

from baobab_activity_reporting.application.report_definition_resolver import (
    resolve_report_definition,
)
from baobab_activity_reporting.application.reporting_service import ReportingService
from baobab_activity_reporting.domain.models.reporting_period import ReportingPeriod


def _parse_date(value: str) -> date:
    """Convertit une chaîne ``YYYY-MM-DD`` en :class:`date`.

    :param value: Date ISO (date seule).
    :type value: str
    :return: Objet date Python.
    :rtype: date
    :raises SystemExit: Si le format est invalide.
    """
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        print(f"Date invalide (attendu YYYY-MM-DD): {value!r}", file=sys.stderr)
        raise SystemExit(2) from None


def main(argv: list[str] | None = None) -> int:
    """Analyse les arguments et exécute la sous-commande demandée.

    :param argv: Arguments (``None`` = ``sys.argv[1:]``).
    :type argv: list[str] | None
    :return: Code de sortie (0 si succès).
    :rtype: int
    """
    parser = argparse.ArgumentParser(
        prog="baobab-reporting",
        description=(
            "Chaîne complète Baobab : import CSV, calcul des KPI, "
            "génération de rapports (Markdown / DOCX)."
        ),
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Niveau de journalisation racine (défaut: INFO).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_imp = sub.add_parser("import", help="Importer trois fichiers CSV vers SQLite.")
    p_imp.add_argument("--database", required=True, help="Chemin du fichier SQLite.")
    p_imp.add_argument("--incoming", required=True, help="CSV appels entrants.")
    p_imp.add_argument("--outgoing", required=True, help="CSV appels sortants.")
    p_imp.add_argument("--tickets", required=True, help="CSV tickets.")

    p_comp = sub.add_parser("compute", help="Calculer et persister les KPI pour une période.")
    p_comp.add_argument("--database", required=True, help="Chemin du fichier SQLite.")
    p_comp.add_argument("--period-start", required=True, help="Début YYYY-MM-DD.")
    p_comp.add_argument("--period-end", required=True, help="Fin YYYY-MM-DD.")
    p_comp.add_argument(
        "--clear-period",
        action="store_true",
        help="Supprimer les KPI existants pour cette période avant calcul.",
    )

    p_gen = sub.add_parser("generate", help="Construire un ReportModel et exporter.")
    p_gen.add_argument("--database", required=True, help="Chemin du fichier SQLite.")
    p_gen.add_argument("--period-start", required=True, help="Début YYYY-MM-DD.")
    p_gen.add_argument("--period-end", required=True, help="Fin YYYY-MM-DD.")
    p_gen.add_argument(
        "--report-type",
        required=True,
        choices=[
            "activity_telephony",
            "activity_by_site",
            "activity_by_agent",
            "weekly_activity_by_agent",
            "weekly_activity_by_site",
        ],
        help="Identifiant du gabarit de rapport.",
    )
    p_gen.add_argument("--markdown", default=None, help="Chemin de sortie Markdown.")
    p_gen.add_argument("--docx", default=None, help="Chemin de sortie DOCX.")

    if argv is None:
        parse_args = parser.parse_args()
    else:
        parse_args = parser.parse_args(argv)

    logging.basicConfig(
        level=getattr(logging, str(parse_args.log_level)),
        format="%(levelname)s %(name)s %(message)s",
    )

    service = ReportingService(parse_args.database)
    try:
        if parse_args.command == "import":
            summary = service.import_sources(
                parse_args.incoming,
                parse_args.outgoing,
                parse_args.tickets,
            )
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        elif parse_args.command == "compute":
            period = ReportingPeriod(
                _parse_date(parse_args.period_start),
                _parse_date(parse_args.period_end),
            )
            summary = service.compute_metrics(
                period,
                clear_existing_for_period=bool(parse_args.clear_period),
            )
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        else:
            period = ReportingPeriod(
                _parse_date(parse_args.period_start),
                _parse_date(parse_args.period_end),
            )
            definition = resolve_report_definition(parse_args.report_type)
            model = service.generate_report(
                period,
                definition,
                markdown_path=parse_args.markdown,
                docx_path=parse_args.docx,
            )
            out = {
                "report_type": model.report_type,
                "title": model.title,
                "sections": len(model.sections),
            }
            print(json.dumps(out, ensure_ascii=False, indent=2))
    finally:
        service.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

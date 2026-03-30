"""Tests du module cli.main."""

import json
from pathlib import Path

import pytest

from baobab_activity_reporting.cli.main import _parse_date, main


class TestCliMain:
    """Tests de la CLI."""

    def test_import_command(
        self, tmp_path: Path, fixtures_dir: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """La sous-commande import produit un JSON et crée la base."""
        db = tmp_path / "cli.sqlite"
        code = main(
            [
                "--log-level",
                "ERROR",
                "import",
                "--database",
                str(db),
                "--incoming",
                str(fixtures_dir / "incoming_calls.csv"),
                "--outgoing",
                str(fixtures_dir / "outgoing_calls.csv"),
                "--tickets",
                str(fixtures_dir / "tickets.csv"),
            ]
        )
        assert code == 0
        assert db.is_file()
        captured = capsys.readouterr()
        payload = json.loads(captured.out)
        assert "sources" in payload
        assert len(payload["sources"]) == 3

    def test_compute_and_generate(
        self, tmp_path: Path, fixtures_dir: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Enchaîne import, compute et generate via la CLI."""
        db = tmp_path / "chain.sqlite"
        md_path = tmp_path / "rep.md"
        main(
            [
                "--log-level",
                "ERROR",
                "import",
                "--database",
                str(db),
                "--incoming",
                str(fixtures_dir / "incoming_calls.csv"),
                "--outgoing",
                str(fixtures_dir / "outgoing_calls.csv"),
                "--tickets",
                str(fixtures_dir / "tickets.csv"),
            ]
        )
        capsys.readouterr()
        main(
            [
                "--log-level",
                "ERROR",
                "compute",
                "--database",
                str(db),
                "--period-start",
                "2026-03-01",
                "--period-end",
                "2026-03-31",
                "--clear-period",
            ]
        )
        capsys.readouterr()
        code = main(
            [
                "--log-level",
                "ERROR",
                "generate",
                "--database",
                str(db),
                "--period-start",
                "2026-03-01",
                "--period-end",
                "2026-03-31",
                "--report-type",
                "activity_telephony",
                "--markdown",
                str(md_path),
            ]
        )
        assert code == 0
        assert md_path.is_file()
        final = capsys.readouterr().out.strip()
        out = json.loads(final)
        assert out["report_type"] == "activity_telephony"

    def test_parse_date_invalid(self) -> None:
        """Date mal formée : sortie avec code 2."""
        with pytest.raises(SystemExit) as exc:
            _parse_date("not-a-date")
        assert exc.value.code == 2

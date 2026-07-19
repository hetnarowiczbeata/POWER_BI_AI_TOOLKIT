import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from services.agent import odpowiedz_na_pytanie_metadata, rozpoznaj_typ_zadania


def utworz_model_testowy(root):
    model_path = Path(root) / "Test.SemanticModel"
    tables_path = model_path / "definition" / "tables"
    tables_path.mkdir(parents=True)

    (tables_path / "Miary.tmdl").write_text(
        """table Miary

\tmeasure Orders = SUM(fct_data[Orders])
\tmeasure 'Visible KPI' = [Orders]
\tmeasure 'Helper KPI' = [Visible KPI]
\tmeasure 'Unused KPI' = 1

\tpartition Miary = m
""",
        encoding="utf-8",
    )

    report_path = Path(root) / "Test.Report" / "definition" / "pages" / "p1" / "visuals" / "v1"
    report_path.mkdir(parents=True)
    (report_path / "visual.json").write_text(
        """{
  "projections": [
    {
      "field": {
        "Measure": {
          "Expression": {"SourceRef": {"Entity": "Miary"}},
          "Property": "Visible KPI"
        }
      }
    }
  ]
}""",
        encoding="utf-8",
    )

    return model_path


class TestDaxAgent(unittest.TestCase):
    def test_nieuzywane_miary_pytanie_nie_wraca_do_kolumn(self):
        with TemporaryDirectory() as root:
            model_path = utworz_model_testowy(root)

            odpowiedz = odpowiedz_na_pytanie_metadata(
                str(model_path),
                "Które miary są nie używane?",
            )

        self.assertIn("Miary bez jawnego uzycia", odpowiedz)
        self.assertIn("Unused KPI", odpowiedz)
        self.assertNotIn("Kolumny tabeli Miary", odpowiedz)

    def test_agent_traktuje_optymalizacje_jako_tryb_dax(self):
        self.assertEqual(rozpoznaj_typ_zadania("zoptymalizuj model"), "dax")
        self.assertEqual(rozpoznaj_typ_zadania("jakie relacje poprawic"), "dax")


if __name__ == "__main__":
    unittest.main()

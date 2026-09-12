import importlib.util
from pathlib import Path
import unittest


MODULE = Path(__file__).parents[1] / "projects/05-airflow-etl/src/quality.py"
spec = importlib.util.spec_from_file_location("quality", MODULE)
quality = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quality)


class QualityTests(unittest.TestCase):
    def test_required_fields(self):
        result = quality.check_required_fields(
            [{"id": 1, "score": 90}, {"id": 2, "score": None}],
            {"id", "score"},
        )
        self.assertEqual(result["row_count"], 2)
        self.assertEqual(result["missing_by_field"], {"score": 1})

    def test_minimum_rows(self):
        quality.assert_minimum_rows(10, 10)


if __name__ == "__main__":
    unittest.main()

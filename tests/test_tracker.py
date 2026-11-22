import json
import os
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from exporters import CsvExporter, JsonExporter, TextExporter, get_exporter
from tracker import ExpenseTracker


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp_dir.name, "expenses.json")
        self.export_dir = os.path.join(self.tmp_dir.name, "exports")
        self.tracker = ExpenseTracker(self.db_path, export_dir=self.export_dir)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_add_and_total(self):
        self.tracker.add_expense("Coffee", 3.5, "Food")
        self.tracker.add_expense("Notebook", 6.5, "Study")
        self.assertEqual(self.tracker.get_total(), Decimal("10.00"))

    def test_filter_by_category(self):
        self.tracker.add_expense("Coffee", 3.5, "Food")
        self.tracker.add_expense("Bus", 1.5, "Transport")
        food = self.tracker.filter_by_category("food")
        self.assertEqual(len(food), 1)
        self.assertEqual(food[0]["description"], "Coffee")

    def test_text_report(self):
        self.tracker.add_expense("Coffee", 3.5, "Food")
        report = self.tracker.generate_report("text")
        self.assertIn("Coffee", report)
        self.assertIn("3.50", report)

    def test_csv_report(self):
        self.tracker.add_expense("Coffee", 3.5, "Food")
        report = self.tracker.generate_report("csv")
        self.assertIn("category,description,amount", report)
        self.assertIn("Food,Coffee,3.50", report)

    def test_bad_format(self):
        with self.assertRaises(ValueError):
            self.tracker.generate_report("xml")

    def test_exporters_lookup(self):
        self.assertIsInstance(get_exporter("text"), TextExporter)
        self.assertIsInstance(get_exporter("csv"), CsvExporter)
        self.assertIsInstance(get_exporter("json"), JsonExporter)

    def test_json_report(self):
        self.tracker.add_expense("Coffee", "3.50", "Food")
        data = json.loads(self.tracker.generate_report("json"))
        self.assertEqual(data["total"], "3.50")
        self.assertEqual(len(data["expenses"]), 1)

    def test_decimal_total_no_float_error(self):
        self.tracker.add_expense("Item1", 0.1, "Food")
        self.tracker.add_expense("Item2", 0.2, "Food")
        self.assertEqual(self.tracker.get_total(), Decimal("0.30"))

    def test_reject_negative_and_zero(self):
        with self.assertRaises(ValueError):
            self.tracker.add_expense("Bad", -5.0, "Food")
        with self.assertRaises(ValueError):
            self.tracker.add_expense("Zero", 0, "Food")

    def test_reject_bad_amount_types(self):
        for bad in [float("nan"), float("inf"), True, "abc"]:
            with self.assertRaises(ValueError):
                self.tracker.add_expense("Invalid", bad, "Food")

    def test_reject_empty_text(self):
        with self.assertRaises(ValueError):
            self.tracker.add_expense("   ", 5.0, "Food")
        with self.assertRaises(ValueError):
            self.tracker.add_expense("Lunch", 5.0, "  ")

    def test_csv_blocks_formula_injection(self):
        self.tracker.add_expense("=SUM(1,2)", 2.0, "+Food")
        self.tracker.add_expense("@CMD()", 3.0, "-Other")
        report = self.tracker.generate_report("csv")
        self.assertIn("'+Food,\"'=SUM(1,2)\",2.00", report)
        self.assertIn("'-Other,'@CMD(),3.00", report)

    def test_csv_handles_commas(self):
        self.tracker.add_expense("Tea, cake", 4.25, "Food")
        report = self.tracker.generate_report("csv")
        self.assertIn('Food,"Tea, cake",4.25', report)

    def test_export_inside_folder(self):
        self.tracker.add_expense("Coffee", 3.5, "Food")
        saved = self.tracker.export_report("summary.txt", "text")
        self.assertTrue(saved.exists())
        self.assertEqual(saved.parent, Path(self.export_dir).resolve())

    def test_export_blocks_outside_path(self):
        self.tracker.add_expense("Coffee", 3.5, "Food")
        with self.assertRaises(ValueError):
            self.tracker.export_report("../outside.txt", "text")

    def test_save_and_reload(self):
        self.tracker.add_expense("Coffee", "3.50", "Food")
        self.tracker.save()
        reloaded = ExpenseTracker(self.db_path, export_dir=self.export_dir)
        self.assertEqual(reloaded.get_total(), Decimal("3.50"))
        self.assertEqual(len(reloaded.expenses), 1)


if __name__ == "__main__":
    unittest.main()

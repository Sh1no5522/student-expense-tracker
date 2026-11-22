import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

from exporters import get_exporter


class ExpenseTracker:
    def __init__(self, storage_path="expenses.json", export_dir="exports"):
        self.storage_path = Path(storage_path)
        self.export_dir = Path(export_dir).resolve()
        self.expenses = []
        self._load()

    def _load(self):
        if self.storage_path.exists():
            with open(self.storage_path, "r", encoding="utf-8") as f:
                self.expenses = json.load(f)

    def save(self):
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, indent=2)

    def _check_amount(self, amount):
        if isinstance(amount, bool):
            raise ValueError("Amount must be a positive number.")
        try:
            value = Decimal(str(amount))
        except (InvalidOperation, ValueError):
            raise ValueError("Amount must be a valid number.")
        if not value.is_finite() or value <= Decimal("0"):
            raise ValueError("Amount must be a positive number.")
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def add_expense(self, description, amount, category="General"):
        clean_desc = str(description).strip()
        clean_cat = str(category).strip()
        if not clean_desc:
            raise ValueError("Description cannot be empty.")
        if not clean_cat:
            raise ValueError("Category cannot be empty.")

        valid_amount = self._check_amount(amount)
        item = {
            "description": clean_desc,
            "amount": f"{valid_amount:.2f}",
            "category": clean_cat,
        }
        self.expenses.append(item)
        return item

    def get_total(self):
        total = Decimal("0.00")
        for item in self.expenses:
            total += Decimal(str(item["amount"]))
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def filter_by_category(self, category):
        target = category.strip().lower()
        return [e for e in self.expenses if e["category"].lower() == target]

    def generate_report(self, fmt="text"):
        exporter = get_exporter(fmt)
        return exporter.format_report(self.expenses, self.get_total())

    def _safe_export_path(self, filename):
        if not filename or not filename.strip():
            raise ValueError("Filename cannot be empty.")
        target = (self.export_dir / filename).resolve()
        try:
            target.relative_to(self.export_dir)
        except ValueError:
            raise ValueError("Export path must stay inside export_dir.")
        return target

    def export_report(self, filename, fmt="text"):
        target = self._safe_export_path(filename)
        target.parent.mkdir(parents=True, exist_ok=True)
        content = self.generate_report(fmt)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return target

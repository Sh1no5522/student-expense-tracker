import json
from pathlib import Path


class ExpenseTracker:
    def __init__(self, storage_path="expenses.json"):
        self.storage_path = Path(storage_path)
        self.expenses = []
        self._load()

    def _load(self):
        if self.storage_path.exists():
            with open(self.storage_path, "r", encoding="utf-8") as f:
                self.expenses = json.load(f)

    def save(self):
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, indent=2)

    def add_expense(self, description, amount, category="General"):
        item = {
            "description": description,
            "amount": amount,
            "category": category,
        }
        self.expenses.append(item)
        return item

    def get_total(self):
        total = 0.0
        for item in self.expenses:
            total += item["amount"]
        return total

    def filter_by_category(self, category):
        return [e for e in self.expenses if e["category"].lower() == category.lower()]

    def generate_report(self, fmt="text"):
        if fmt == "text":
            lines = ["Expense Report"]
            for e in self.expenses:
                lines.append(f"- {e['category']}: {e['description']} (${e['amount']})")
            lines.append(f"Total: ${self.get_total()}")
            return "\n".join(lines)
        elif fmt == "csv":
            lines = ["category,description,amount"]
            for e in self.expenses:
                lines.append(f"{e['category']},{e['description']},{e['amount']}")
            lines.append(f"TOTAL,,{self.get_total()}")
            return "\n".join(lines)
        elif fmt == "json":
            return json.dumps({"expenses": self.expenses, "total": self.get_total()}, indent=2)
        else:
            raise ValueError(f"Unsupported format: {fmt}")

    def export_report(self, output_path, fmt="text"):
        content = self.generate_report(fmt)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

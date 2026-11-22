import csv
import io
import json
from decimal import Decimal


BAD_PREFIXES = ("=", "+", "-", "@")


def clean_csv_cell(value):
    text = str(value)
    if text.startswith(BAD_PREFIXES):
        return "'" + text
    return text


class ReportExporter:
    def format_report(self, expenses, total):
        raise NotImplementedError


class TextExporter(ReportExporter):
    def format_report(self, expenses, total):
        lines = ["Expense Report"]
        for item in expenses:
            lines.append(f"- {item['category']}: {item['description']} (${item['amount']})")
        lines.append(f"Total: ${total:.2f}")
        return "\n".join(lines)


class CsvExporter(ReportExporter):
    def format_report(self, expenses, total):
        output = io.StringIO()
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(["category", "description", "amount"])
        for item in expenses:
            writer.writerow([
                clean_csv_cell(item["category"]),
                clean_csv_cell(item["description"]),
                f"{Decimal(str(item['amount'])):.2f}",
            ])
        writer.writerow(["TOTAL", "", f"{total:.2f}"])
        return output.getvalue().rstrip("\n")


class JsonExporter(ReportExporter):
    def format_report(self, expenses, total):
        data = {
            "expenses": expenses,
            "total": f"{total:.2f}",
        }
        return json.dumps(data, indent=2)


EXPORTERS = {
    "text": TextExporter(),
    "csv": CsvExporter(),
    "json": JsonExporter(),
}


def get_exporter(fmt):
    if fmt not in EXPORTERS:
        raise ValueError(f"Unsupported format: {fmt}")
    return EXPORTERS[fmt]

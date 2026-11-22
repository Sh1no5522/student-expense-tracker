# AGENTS.md

## Project
Student Expense Tracker is a small local Python CLI app for tracking daily student expenses, getting totals, filtering by category, and exporting text, CSV, or JSON reports. No database, login, or real personal data is used.

## Files
- main.py: runs the demo with sample expenses.
- tracker.py: ExpenseTracker class (load/save JSON, input checks, Decimal totals, safe export path).
- exporters.py: Strategy classes for report formats (TextExporter, CsvExporter, JsonExporter).
- tests/test_tracker.py: unittest tests for all features and bug fixes.

## Setup
- Python 3.10 or higher.
- No third-party packages are needed to run the app.
- Optional pinned dev tools are listed in requirements-dev.txt.

## Safe Commands
- Run demo: python main.py
- Run tests: python -m unittest discover -s tests -v
- Check syntax: python -m compileall -q .

## Coding and Test Rules
- Use Decimal for money totals, never float.
- Reject empty text, negative numbers, zero, booleans, NaN, and infinity.
- Clean CSV cells starting with =, +, -, or @ so Excel does not run them as formulas.
- Only allow report files to be saved inside export_dir.
- Keep AC1-AC5 working and add tests for every fix.

## Forbidden Actions
- Do not add passwords, API keys, .env files, or real personal data.
- Do not deploy to production or make network calls.
- Do not run destructive commands like rm -rf, git reset --hard, or git push --force.
- Do not install or change packages without asking first.
- Do not delete or weaken existing tests to make them pass.
- Do not push straight to main; a human must review every change first.

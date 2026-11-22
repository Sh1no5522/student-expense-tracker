# Student Expense Tracker

A small local Python CLI app for tracking student expenses, filtering by category, and saving text, CSV, or JSON reports.

## Project Files
- main.py - runs a quick demo with sample expenses
- tracker.py - core ExpenseTracker class (Decimal totals, input checks, safe file export)
- exporters.py - text, CSV, and JSON report exporters
- tests/test_tracker.py - unit tests
- AGENTS.md - rules for AI coding tools
- requirements-dev.txt - pinned optional dev tools

## Setup
Requires Python 3.10+. No external packages are needed to run the app.

## Commands
Run the app:
python main.py

Run tests:
python -m unittest discover -s tests -v

Check syntax / build:
python -m compileall -q .

## Notes
- Stores data in a local JSON file only (no database or login).
- CSV exports escape values starting with =, +, -, or @.
- Exported report files can only be saved inside the exports folder.

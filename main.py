from tracker import ExpenseTracker


def main():
    tracker = ExpenseTracker("sample_expenses.json")
    if not tracker.expenses:
        tracker.add_expense("Cafeteria lunch", 4.50, "Food")
        tracker.add_expense("Bus ticket", 2.25, "Transport")
    print(tracker.generate_report("text"))


if __name__ == "__main__":
    main()

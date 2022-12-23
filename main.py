import json
from pprint import pprint
from collections import OrderedDict

# JSON_FILES = [pos_json for pos_json in os.listdir(os.getcwd()) if pos_json.endswith('.json')]
INPUT_FILES = [
    "1-input.json",
    "2-input.json",
]


def main():
    dates = []
    for file in INPUT_FILES:
        with open(file) as f:
            data = json.load(f)
            expenseData = data.get("expenseData", [])
            revenueData = data.get("revenueData", [])

            minYM = "9999-99"
            maxYM = "0000-00"

            for expense in expenseData:
                date = "-".join(expense["startDate"].split("-")[:2])
                minYM = min(minYM, date)
                maxYM = max(maxYM, date)

            for rev in revenueData:
                date = "-".join(rev["startDate"].split("-")[:2])
                minYM = min(minYM, date)
                maxYM = max(maxYM, date)
                
            # Get the revenue and expense data
            revenues = {}
            expenses = {}
            for rev in revenueData:
                revenues[rev["startDate"]] = revenues.get(
                    rev["startDate"], 0) + rev["amount"]
            for exp in expenseData:
                expenses[exp["startDate"]] = expenses.get(
                    exp["startDate"], 0) + exp["amount"]

            # Generate the dates for the result
            dates = []
            for year in range(int(minYM.split("-")[0]), int(maxYM.split("-")[0]) + 1):
                for month in range(1, 13):
                    if year == int(minYM.split("-")[0]) and month < int(minYM.split("-")[1]):
                        continue
                    if year == int(maxYM.split("-")[0]) and month > int(maxYM.split("-")[1]):
                        continue
                    dates.append(f"{year}-{month:02d}-01T00:00:00.000Z")

            balance = []
            for date in dates:
                balance.append({
                    "amount": revenues.get(date, 0) - expenses.get(date, 0),
                    "startDate": date,
                })

            pprint(balance, indent=2)
            # Store the result as a json file
            with open(f"{file.split('.')[0]}-output.json", "w") as f:
                json.dump({"balance": balance}, f, indent=2)

    return


if __name__ == "__main__":
    main()
    exit(0)

# portfolio_tracker.py
import csv
import sys

# Hardcoded prices (you can change/add)
PRICES = {
    "AAPL": 180.0,
    "TSLA": 250.0,
    "GOOG": 140.0,
    "MSFT": 320.0,
    "AMZN": 110.0
}

def safe_float(prompt):
    while True:
        s = input(prompt).strip()
        try:
            return float(s)
        except ValueError:
            print("Invalid number. Please enter a numeric value (e.g. 10 or 10.5).")

def get_stock_entry():
    while True:
        ticker = input("Enter stock ticker (e.g. AAPL): ").strip().upper()
        if not ticker:
            print("Ticker cannot be empty.")
            continue
        qty = safe_float("Quantity of shares (can be fractional, e.g. 1.5): ")
        if qty < 0:
            print("Quantity can't be negative.")
            continue
        return ticker, qty

def get_price_for_unknown(ticker):
    print(f"Ticker '{ticker}' not found in price dictionary.")
    choice = input("Enter 'a' to add a custom price for this ticker, or 's' to skip this stock: ").strip().lower()
    if choice == 'a':
        price = safe_float(f"Enter price for {ticker}: ")
        PRICES[ticker] = float(price)
        print(f"Added {ticker} with price {price}.")
        return price
    print(f"Skipping {ticker}.")
    return None

def print_summary(rows, total):
    print("\n--- Portfolio Summary ---")
    print(f"{'Ticker':<8}{'Qty':>10}{'Price':>12}{'Value':>14}")
    for r in rows:
        print(f"{r['ticker']:<8}{r['qty']:>10.4f}{r['price']:>12.2f}{r['value']:>14.2f}")
    print("-" * 46)
    print(f"{'Total investment:':<30}{total:>16.2f}\n")

def save_to_csv(rows, total, filename):
    fieldnames = ['ticker', 'qty', 'price', 'value']
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
        writer.writerow({'ticker': 'TOTAL', 'qty': '', 'price': '', 'value': total})
    print(f"Saved CSV to {filename}")

def save_to_txt(rows, total, filename):
    with open(filename, 'w') as f:
        f.write("--- Portfolio Summary ---\n")
        f.write(f"{'Ticker':<8}{'Qty':>10}{'Price':>12}{'Value':>14}\n")
        for r in rows:
            f.write(f"{r['ticker']:<8}{r['qty']:>10.4f}{r['price']:>12.2f}{r['value']:>14.2f}\n")
        f.write("-" * 46 + "\n")
        f.write(f"{'Total investment:':<30}{total:>16.2f}\n")
    print(f"Saved TXT to {filename}")

def main():
    print("Simple Stock Portfolio Tracker")
    print("Known price tickers:", ", ".join(sorted(PRICES.keys())))
    n = int(safe_float("How many different stocks will you enter? (0 to exit): "))
    if n <= 0:
        print("No stocks entered. Exiting.")
        sys.exit(0)

    rows = []
    total = 0.0
    for i in range(n):
        print(f"\nStock #{i+1}:")
        ticker, qty = get_stock_entry()
        price = PRICES.get(ticker)
        if price is None:
            price = get_price_for_unknown(ticker)
            if price is None:
                continue  # skip this entry
        value = float(price) * float(qty)
        rows.append({'ticker': ticker, 'qty': qty, 'price': float(price), 'value': value})
        total += value

    print_summary(rows, total)

    save_choice = input("Save results? (y/n): ").strip().lower()
    if save_choice == 'y':
        fmt = input("Choose format - csv or txt (default csv): ").strip().lower() or 'csv'
        fname = input("Filename (default 'portfolio'): ").strip() or 'portfolio'
        if fmt == 'csv':
            if not fname.endswith('.csv'):
                fname += '.csv'
            save_to_csv(rows, total, fname)
        else:
            if not fname.endswith('.txt'):
                fname += '.txt'
            save_to_txt(rows, total, fname)

if __name__ == "__main__":
    main()

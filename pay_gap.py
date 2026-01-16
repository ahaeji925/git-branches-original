"""
Gender Pay Gap Analysis
"""

import csv

FILENAME = "earnings.csv"


def get_top_pay_disparities(top_n):
    """
    Calculate gender pay gaps and return top N countries with highest disparities.

    Args:
        top_n: Number of top results to return

    Returns:
        List of tuples: [(country, pay_gap_percentage), ...]
        Sorted by pay_gap_percentage descending
    """
    with open(FILENAME, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # mutiple rows per record for currencies, filter to USD normalized
    usd_data = [
        row for row in data if row.get("classif1.label") == "Currency: U.S. dollars"
    ]

    country_earnings = {}
    for row in usd_data:
        country = row["area"]
        sex = row["sex.label"]
        value = float(row["obs_value"])
        if country not in country_earnings:
            country_earnings[country] = {"Male": [], "Female": []}
        if sex in ["Male", "Female"]:
            country_earnings[country][sex].append(value)

    # average pay gap per country across whichever years are provided
    results = []
    for country, earnings in country_earnings.items():
        # skip records with missing data
        if earnings["Male"] and earnings["Female"]:
            male_avg = sum(earnings["Male"]) / len(earnings["Male"])
            female_avg = sum(earnings["Female"]) / len(earnings["Female"])
            pay_gap = ((male_avg - female_avg) / male_avg) * 100
            results.append((country, pay_gap))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]


if __name__ == "__main__":
    top_disparities = get_top_pay_disparities(10)

    print(f"{'Country':<40} {'Pay Gap %':>10}")
    print("-" * 50)

    for country, gap in top_disparities:
        print(f"{country:<40} {gap:>10.2f}%")

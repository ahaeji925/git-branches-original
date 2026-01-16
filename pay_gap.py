"""
Gender Pay Gap Analysis
"""

import pandas as pd

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
    df = pd.read_csv(FILENAME, encoding="utf-8-sig")

    usd_data = df[df["classif1.label"] == "Currency: U.S. dollars"].copy()
    filtered = usd_data[usd_data["sex.label"].isin(["Male", "Female"])]

    # group by country and sex, calculate average earnings
    country_sex_avg = (
        filtered.groupby(["area", "sex.label"])["obs_value"].mean().reset_index()
    )

    # pivot to get M and F side-by-side
    pivoted = country_sex_avg.pivot(
        index="area", columns="sex.label", values="obs_value"
    ).reset_index()

    # drop rows with missing data
    pivoted = pivoted.dropna()

    # calculate pay gap
    pivoted["pay_gap_percentage"] = (
        (pivoted["Male"] - pivoted["Female"]) / pivoted["Male"]
    ) * 100

    # top N
    results = (
        pivoted[["area", "pay_gap_percentage"]]
        .sort_values("pay_gap_percentage", ascending=False)
        .head(top_n)
    )

    return list(results.itertuples(index=False, name=None))


if __name__ == "__main__":
    top_disparities = get_top_pay_disparities(10)

    print(f"{'Country':<40} {'Pay Gap %':>10}")
    print("-" * 50)

    for country, gap in top_disparities:
        print(f"{country:<40} {gap:>10.2f}%")

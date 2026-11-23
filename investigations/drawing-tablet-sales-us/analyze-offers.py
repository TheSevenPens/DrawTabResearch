#!/usr/bin/env python3
"""Recompute the U.S. drawing tablet discount sample from the published offers."""

import argparse
import json
from pathlib import Path
from statistics import median, quantiles

BRANDS = ("Wacom", "Huion", "XPPen")
SEASONS = (
    "All", "Black Friday / Cyber", "Outside Black Friday",
    "Midyear Prime", "Anniversary", "Back to school", "October / fall",
)


def analysis(offers):
    core, paired = [], []
    for row in offers:
        sale, ref = row["sale_price_usd"], row["reference_price_usd"]
        eligible = (
            row["market"] == "US"
            and row["brand"] in BRANDS
            and row["device_type"] in ("Pen tablet", "Pen display")
            and type(sale) in (float, int)
        )
        if eligible:
            core.append(row)
        valid = (
            eligible
            and type(ref) in (float, int)
            and ref > sale > 0
            and "affiliate slug is inconsistent" not in (row.get("notes") or "")
        )
        if row["summary_sample"] != ("Yes" if valid else "No"):
            raise ValueError(f"Sample rule disagrees with saved row: {row['model']} ({row['url']})")
        if valid:
            paired.append(row)

    stats = {}
    for brand in ("All", *BRANDS):
        for season in SEASONS:
            rates = sorted(
                (1 - row["sale_price_usd"] / row["reference_price_usd"]) * 100
                for row in paired
                if (brand == "All" or row["brand"] == brand)
                and (
                    season == "All"
                    or (season == "Outside Black Friday" and row["season"] != "Black Friday / Cyber")
                    or row["season"] == season
                )
            )
            if rates:
                q1, _, q3 = quantiles(rates, n=4, method="inclusive") if len(rates) > 1 else rates * 3
                stats[f"{brand}|{season}"] = [
                    len(rates),
                    *(round(x, 1) for x in (rates[0], q1, median(rates), q3, rates[-1])),
                ]
    return {
        "offer_rows": len(offers),
        "price_rows": len(core),
        "paired_rows": len(paired),
        "stat_columns": ["n", "min_pct", "q1_pct", "median_pct", "q3_pct", "max_pct"],
        "stats": stats,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("offers", nargs="?", type=Path, default=Path(__file__).with_name("model-offers.json"))
    args = parser.parse_args()
    print(json.dumps(analysis(json.loads(args.offers.read_text(encoding="utf-8"))), indent=2))


if __name__ == "__main__":
    main()

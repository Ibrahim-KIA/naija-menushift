"""Challenge 3: auditable market-opportunity scoring with evidence abstention.

The real 48-row workbook lacks product demand and retailer observations. This
module NEVER fills gaps with zeros, invented sales, or soybean production proxies.
All illustrative numeric rankings have explicit synthetic markings.
"""
from __future__ import annotations

import csv
import math
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Mapping

WEIGHTS: dict[str, int] = {
    "Demand_Score_1to5": 30,
    "Affordability_Score_1to5": 25,
    "Channel_Score_1to5": 20,
    "Supply_Distribution_Score_1to5": 15,
    "Market_Gap_Score_1to5": 10,
}
WEIGHT_SCENARIOS: dict[str, dict[str, int]] = {
    "Original 30/25/20/15/10": WEIGHTS,
    "Demand-led 40/20/20/10/10": dict(zip(WEIGHTS, (40, 20, 20, 10, 10))),
    "Affordability-led 20/40/15/15/10": dict(zip(WEIGHTS, (20, 40, 15, 15, 10))),
    "Channel-led 20/20/35/15/10": dict(zip(WEIGHTS, (20, 20, 35, 15, 10))),
}
REQUIRED_FIELDS = {
    "Core": ("Opportunity_ID", "Product", "City", "Customer_Segment"),
    "Demand": ("Consumer_Demand_Signal", "Demand_Sample_Size", "Demand_Signal_Date", "Demand_Score_1to5"),
    "Affordability": (
        "Competitor_Price_NGN", "Competitor_Pack_or_Serving_Size",
        "Proposed_Product_Price_NGN", "Price_Comparison_Notes",
        "Affordability_Proxy_or_Source", "Affordability_Score_1to5",
    ),
    "Channels": (
        "Relevant_Retail_or_Foodservice_Count", "Channel_Access_Evidence", "Channel_Score_1to5",
    ),
    "Supply": (
        "Soybean_or_Tofu_Supplier_Evidence",
        "Distribution_or_Storage_Constraints", "Supply_Distribution_Score_1to5",
    ),
    "Competition": (
        "Local_Product_Availability_Evidence", "Typical_Competing_Product",
        "Competitor_Intensity_1to5", "Market_Gap_Score_1to5",
    ),
    "Provenance": ("Evidence_Confidence", "Source_IDs"),
}
POSITIVE_FIELDS = {
    "Demand_Sample_Size", "Competitor_Price_NGN", "Proposed_Product_Price_NGN",
}
SCORE_FIELDS = set(WEIGHTS) | {"Competitor_Intensity_1to5"}
CONFIDENCE = {"High", "Medium", "Low"}


@dataclass(frozen=True)
class MarketResult:
    opportunity_id: str
    product: str
    city: str
    customer_segment: str
    score: float | None
    evidence_confidence: str
    gaps: tuple[str, ...]
    synthetic: bool = False

    @property
    def ready(self) -> bool:
        return self.score is not None

    def as_dict(self) -> dict:
        return {
            "Opportunity": self.opportunity_id,
            "Product": self.product,
            "City": self.city,
            "Segment": self.customer_segment,
            "Score / 100": self.score,
            "Evidence confidence": self.evidence_confidence or "Unrated",
            "Status": "SYNTHETIC DEMO" if self.synthetic else ("Eligible to rank" if self.ready else "Missing evidence"),
            "Missing fields": ", ".join(self.gaps),
        }


def read_opportunities(path: str | Path) -> list[dict[str, str]]:
    path = Path(path)
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames or []
        expected = {field for fields in REQUIRED_FIELDS.values() for field in fields}
        if not headers or len(set(headers)) != len(headers) or not expected.issubset(headers):
            raise ValueError("Opportunity CSV has duplicate or missing required columns")
        rows = list(reader)
    if not rows:
        raise ValueError("No opportunity rows supplied")
    ids = set()
    for row in rows:
        if None in row or any(value is None for value in row.values()):
            raise ValueError("Malformed opportunity CSV row")
        ident = row["Opportunity_ID"].strip()
        if not ident or ident in ids:
            raise ValueError("Opportunity IDs must be unique and nonempty")
        ids.add(ident)
    return rows


def _positive_number(value: str) -> bool:
    try:
        v = float(value)
        return math.isfinite(v) and v > 0
    except (ValueError, TypeError):
        return False


def _valid_nonnegative_count(value: str) -> bool:
    try:
        number = float(value)
        return math.isfinite(number) and number.is_integer() and number >= 0
    except (ValueError, TypeError):
        return False


def _valid_score(value: str) -> bool:
    try:
        value = float(value)
        return math.isfinite(value) and value.is_integer() and 1 <= value <= 5
    except (ValueError, TypeError):
        return False


def evidence_gaps(row: Mapping[str, str]) -> tuple[str, ...]:
    """Missing / invalid evidence is abstention, not a score of zero."""
    gaps = []
    for group, fields in REQUIRED_FIELDS.items():
        for field in fields:
            value = str(row.get(field, "") or "").strip()
            if not value:
                gaps.append(field)
            elif field == "Relevant_Retail_or_Foodservice_Count" and not _valid_nonnegative_count(value):
                gaps.append(field + " [must be nonnegative integer]")
            elif field in SCORE_FIELDS and not _valid_score(value):
                gaps.append(field + " [must be integer 1–5]")
            elif field in POSITIVE_FIELDS and not _positive_number(value):
                gaps.append(field + " [must be positive]")
            elif field == "Demand_Signal_Date":
                try:
                    date.fromisoformat(value)
                except ValueError:
                    gaps.append(field + " [use ISO YYYY-MM-DD]")
            elif field == "Evidence_Confidence" and value not in CONFIDENCE:
                gaps.append(field + " [High/Medium/Low]")
    return tuple(gaps)


def score_opportunity(
    row: Mapping[str, str],
    *,
    weights: Mapping[str, int] | None = None,
    synthetic: bool = False,
) -> MarketResult:
    weights = weights or WEIGHTS
    if set(weights) != set(WEIGHTS) or sum(weights.values()) != 100 or any(v < 0 for v in weights.values()):
        raise ValueError("Weights must cover all five criteria, be nonnegative and sum to 100")
    gaps = () if synthetic else evidence_gaps(row)
    if synthetic and not all(_valid_score(str(row.get(key, ""))) for key in WEIGHTS):
        raise ValueError("Synthetic demonstration scores must all be valid integers 1–5")
    score = None
    if not gaps:
        score = round(sum(float(row[key]) * w for key, w in weights.items()) / 5.0, 2)
    return MarketResult(
        opportunity_id=row.get("Opportunity_ID", ""),
        product=row.get("Product", ""),
        city=row.get("City", ""),
        customer_segment=row.get("Customer_Segment", ""),
        score=score,
        evidence_confidence=row.get("Evidence_Confidence", ""),
        gaps=gaps,
        synthetic=synthetic,
    )


def evaluate_markets(
    rows: list[dict[str, str]],
    *,
    weights: Mapping[str, int] | None = None,
    synthetic: bool = False,
) -> list[MarketResult]:
    result = [score_opportunity(row, weights=weights, synthetic=synthetic) for row in rows]
    return sorted(result, key=lambda r: (r.score is None, -(r.score or 0), r.product, r.city, r.opportunity_id))


def evidence_coverage(results: list[MarketResult]) -> dict:
    missing = Counter(field.split(" [")[0] for r in results for field in r.gaps)
    return {
        "opportunities": len(results),
        "rankable": sum(r.ready for r in results),
        "not_rankable": sum(not r.ready for r in results),
        "missing_field_counts": dict(missing),
    }


def synthetic_demonstration(source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Six-city × two-product SCENARIO, never real market observations."""
    by_city_product = {}
    for row in source_rows:
        key = (row["City"], row["Product"])
        if key not in by_city_product:
            by_city_product[key] = row
    city_scores = {
        "Kano": (3, 4, 4, 4, 3),
        "Kaduna": (4, 4, 3, 4, 3),
        "Jos": (2, 4, 3, 3, 3),
        "Abuja": (4, 2, 4, 3, 3),
        "Lagos": (4, 2, 5, 3, 2),
        "Ibadan": (3, 3, 3, 3, 4),
    }
    demo = []
    for city in city_scores:
        for product in ("Tofu suya", "Kafi soy yoghurt"):
            source = by_city_product[(city, product)]
            row = dict(source)
            vals = city_scores[city]
            if product == "Kafi soy yoghurt":
                vals = (vals[0], vals[1], min(5, vals[2] + 1), max(1, vals[3] - 1), vals[4])
            row.update({k: str(v) for k, v in zip(WEIGHTS, vals)})
            row["Evidence_Confidence"] = "Low"
            row["Source_IDs"] = "SYNTHETIC-DO-NOT-CITE-AS-DEMAND"
            demo.append(row)
    if len(demo) != 12:
        raise ValueError("Synthetic demo expected all six cities and both products")
    return demo

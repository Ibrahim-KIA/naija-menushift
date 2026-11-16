"""Unsupervised buyer-behaviour exploration for Challenge 3.

K-means finds patterns in consented survey responses. A cluster is neither a
market-size estimate nor a proof of willingness to pay or an AI sales forecast.
No real segmentation is possible on the supplied empty survey sheet.
"""
from __future__ import annotations

import csv
import math
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

QUESTION_FIELDS = {
    "Tofu suya": (
        "Willing_To_Try_Tofu_Suya", "Willing_To_Buy_Tofu_Suya",
        "Max_WTP_Tofu_Suya_NGN", "Eats_Suya_How_Often",
    ),
    "Kafi soy yoghurt": (
        "Willing_To_Try_Kafi", "Willing_To_Buy_Kafi",
        "Max_WTP_Kafi_NGN", "Consumes_Yoghurt_How_Often",
    ),
}
FREQUENCIES = {
    "never": 0, "rarely": 1, "less than monthly": 1, "monthly": 2,
    "once a month": 2, "weekly": 3, "once a week": 3,
    "several times weekly": 4, "daily": 5,
}
YES = {"yes", "true", "1"}
NO = {"no", "false", "0"}


@dataclass(frozen=True)
class Segment:
    cluster: int
    respondents: int
    observed_buy_intent_pct: float
    mean_stated_wtp_ngn: float
    dominant_cities: tuple[str, ...]

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Segmentation:
    product: str
    n_respondents: int
    excluded_unconsented: int
    silhouette: float | None
    segments: tuple[Segment, ...]
    synthetic: bool = False


def read_survey(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames or []
        required = {"Respondent_ID", "Date", "City", "Consent_Obtained"}
        required |= {name for fields in QUESTION_FIELDS.values() for name in fields}
        if not headers or len(headers) != len(set(headers)) or not required.issubset(headers):
            raise ValueError("Survey CSV missing questionnaire columns or has duplicate headers")
        records = list(reader)
    if any(None in r or any(value is None for value in r.values()) for r in records):
        raise ValueError("Malformed survey CSV")
    return records


def _binary(value: str) -> float:
    value = (value or "").strip().lower()
    if value in YES:
        return 1.0
    if value in NO:
        return 0.0
    raise ValueError("Response must be explicitly yes or no")


def segment_consumers(
    survey: list[dict[str, str]], product: str, *, min_responses: int = 24,
    synthetic: bool = False,
) -> Segmentation:
    if product not in QUESTION_FIELDS:
        raise ValueError("Unknown product")
    fields = QUESTION_FIELDS[product]
    included = []
    rejected_consent = 0
    respondent_ids = set()
    for row in survey:
        consent = (row.get("Consent_Obtained") or "").strip().lower()
        if consent not in YES:
            rejected_consent += 1
            continue
        identifier = (row.get("Respondent_ID") or "").strip()
        if not identifier or identifier in respondent_ids:
            raise ValueError("Consented respondent IDs must be nonempty and unique")
        respondent_ids.add(identifier)
        if not row.get("City", "").strip():
            raise ValueError("Consented survey row missing city")
        try:
            date.fromisoformat(row["Date"])
            tried = _binary(row[fields[0]])
            buys = _binary(row[fields[1]])
            price = float(row[fields[2]])
            frequency = FREQUENCIES[row[fields[3]].strip().lower()]
        except (ValueError, KeyError, TypeError) as exc:
            raise ValueError(f"Invalid consented survey fields for respondent {identifier}") from exc
        if not math.isfinite(price) or not 0 <= price <= 1_000_000:
            raise ValueError("Stated willingness to pay is invalid")
        included.append((row["City"], tried, buys, price, frequency))
    if len(included) < min_responses:
        raise ValueError(f"Only {len(included)} consented, complete responses; need at least {min_responses}")
    features = np.array([[x[1], x[2], math.log1p(x[3]), x[4]] for x in included], dtype=float)
    if len(np.unique(features, axis=0)) < 3:
        raise ValueError("Responses lack variation for three-cluster segmentation")
    transformed = StandardScaler().fit_transform(features)
    model = KMeans(n_clusters=3, n_init=10, random_state=42)
    labels = model.fit_predict(transformed)
    if len(set(labels)) < 3:
        raise ValueError("Model produced fewer than three distinct segments")
    quality = silhouette_score(transformed, labels)
    clusters = []
    for cluster in sorted(set(labels)):
        subset = [r for i, r in enumerate(included) if labels[i] == cluster]
        counts = Counter(r[0] for r in subset)
        clusters.append(Segment(
            cluster=int(cluster), respondents=len(subset),
            observed_buy_intent_pct=round(sum(r[2] for r in subset) * 100 / len(subset), 1),
            mean_stated_wtp_ngn=round(sum(r[3] for r in subset) / len(subset), 2),
            dominant_cities=tuple(x for x, _ in counts.most_common(3)),
        ))
    return Segmentation(
        product=product,
        n_respondents=len(included),
        excluded_unconsented=rejected_consent,
        silhouette=round(float(quality), 3),
        segments=tuple(clusters),
        synthetic=synthetic,
    )


def synthetic_survey(product: str, count: int = 36) -> list[dict[str, str]]:
    """Make transparent, fictitious records for exercising clustering only."""
    if product not in QUESTION_FIELDS or count < 24:
        raise ValueError("Invalid synthetic test setup")
    fields = QUESTION_FIELDS[product]
    cities = ["Kano", "Kaduna", "Jos", "Abuja", "Lagos", "Ibadan"]
    records = []
    for i in range(count):
        category = i % 3
        # These numbers are invented for reproducibility, NOT survey data.
        wtp = (450, 1100, 2600)[category] + (i % 4) * 55
        willing = "yes" if category >= 1 else "no"
        row = {
            "Respondent_ID": f"SYNTHETIC-{i+1:03d}",
            "Date": "2026-11-16",
            "City": cities[(i // 3) % len(cities)],
            "Consent_Obtained": "yes",
            fields[0]: "yes" if category >= 1 else "no",
            fields[1]: willing,
            fields[2]: str(wtp),
            fields[3]: ("rarely", "weekly", "daily")[category],
        }
        records.append(row)
    return records

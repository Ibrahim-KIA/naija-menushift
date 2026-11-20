"""Run explicitly in the authorised AWS workshop terminal, never in CI.

Requires boto3 and MENUSHIFT_BEDROCK_MODEL_ID set for the workshop account.
Prints candidate IDs, deterministic baselines and fixed review questions. No credentials are printed.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from menushift.bedrock_advisor import advice_from_workshop
from menushift.kitchen_optimizer import explore

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    s = explore(
        ROOT / "data" / "sources",
        dish_id="suya",
        budget_ngn=1500, protein_target_g=10,
        max_prep_minutes=120,
        equipment=frozenset({"grill", "press", "freezer", "frying_pan"}),
        portions_g=(100,), preference="chewy and practical",
        avoid_allergens=(),
        seasoning_g=0,
    )
    balanced = s.best("balanced")
    cheapest = s.best("budget")
    result = advice_from_workshop(s, preference="chewy and practical")
    print(json.dumps({
        "status": result.status,
        "model_used": result.model_used,
        "food_service_ready": False,
        "suggestions": [asdict(item) for item in result.choices],
        "note": result.message,
        "eligible_option_count": len(s.eligible),
        "eligible_candidate_ids": [item.identifier for item in s.eligible],
        "deterministic_balanced_id": balanced.identifier if balanced else None,
        "cheapest_feasible_id": cheapest.identifier if cheapest else None,
    }, indent=2))


if __name__ == "__main__":
    main()

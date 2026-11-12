"""Traceable, constraint-aware menu comparison with a small text-retrieval component.

THIS IS A RESEARCH PROTOTYPE, NOT A FOOD SAFETY OR CLINICAL NUTRITION TOOL.
Demo prices/nutrients are fictional, explicitly marked in the fixtures, and must never
be described as market measurements. No recipe is automatically approved for food service.
"""
from __future__ import annotations

import csv
import math
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Sequence

from .quality import numeric_health


@dataclass(frozen=True)
class Evaluation:
    option_id: str
    dish_id: str
    name: str
    group: str
    cost_ngn: float
    protein_g: float
    iron_mg: float
    zinc_mg: float
    finished_g: float
    prep_minutes: float
    under_budget: bool
    meets_protein: bool
    plant_only: bool
    feasible: bool
    score: float | None
    reasons: tuple[str, ...]
    sources: tuple[str, ...]
    demo: bool
    allergens: tuple[str, ...] = ()
    score_breakdown: tuple[tuple[str, float], ...] = ()
    ingredient_cost_ngn: float = 0.0
    processing_cost_ngn: float = 0.0
    # purpose-specific traceability; the cost here includes all listed ingredients and explicit overheads

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Dataset:
    ingredients: list[dict[str, str]]
    dishes: list[dict[str, str]]
    options: list[dict[str, str]]
    items: list[dict[str, str]]
    demo: bool


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_dataset(folder: str | Path, *, demo: bool) -> Dataset:
    folder = Path(folder)
    required = ("ingredients.csv", "dishes.csv", "options.csv", "option_items.csv")
    missing = [name for name in required if not (folder / name).exists()]
    if missing:
        raise ValueError(f"Missing data files: {', '.join(missing)}")
    data = Dataset(*(read_csv(folder / name) for name in required), demo=demo)
    validate_dataset(data)
    return data


def _number(row: dict[str, str], field: str, record: str, *, allow_zero: bool = True) -> float:
    raw = (row.get(field) or "").strip()
    if not raw:
        raise ValueError(f"{record}: {field} is missing; obtain a sourced measurement or quotation")
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{record}: {field} is not numeric: {raw!r}") from exc
    if not math.isfinite(value):
        raise ValueError(f"{record}: {field} must be finite")
    if value < 0 or (not allow_zero and value == 0):
        raise ValueError(f"{record}: {field} must be {'positive' if not allow_zero else 'nonnegative'}")
    return value


def validate_dataset(data: Dataset) -> None:
    if not data.ingredients or not data.dishes or not data.options or not data.items:
        raise ValueError("Data files are incomplete. Fill all four CSV files before selecting verified mode.")
    ingredients = {}
    dishes = {}
    options = {}
    for row in data.ingredients:
        key = row.get("ingredient_id", "").strip()
        if not key or key in ingredients:
            raise ValueError("Ingredient IDs must be nonempty and unique")
        ingredients[key] = row
        if row.get("is_animal") not in ("true", "false"):
            raise ValueError(f"{key}: is_animal must be 'true' or 'false'")
        for field in ("price_ngn_per_kg", "protein_g_per_100g", "iron_mg_per_100g", "zinc_mg_per_100g"):
            _number(row, field, key)
        if _number(row, "protein_g_per_100g", key) > 100:
            raise ValueError(f"{key}: protein cannot exceed 100 g per 100 g ingredient")
        for field in ("price_source", "price_date", "nutrition_source", "nutrition_state", "price_region"):
            if not row.get(field, "").strip():
                raise ValueError(f"{key}: missing provenance field {field}")
        try:
            date.fromisoformat(row["price_date"])
        except ValueError as exc:
            raise ValueError(f"{key}: price_date must be YYYY-MM-DD") from exc
        if not data.demo and any("SYNTHETIC" in row.get(x, "").upper() for x in ("price_source", "nutrition_source")):
            raise ValueError(f"{key}: synthetic fixture is forbidden in verified mode")
    for row in data.dishes:
        key = row.get("dish_id", "").strip()
        if not key or key in dishes:
            raise ValueError("Dish IDs must be nonempty and unique")
        dishes[key] = row
    for row in data.options:
        key = row.get("option_id", "").strip()
        if not key or key in options:
            raise ValueError("Option IDs must be nonempty and unique")
        options[key] = row
        if row.get("dish_id") not in dishes:
            raise ValueError(f"{key}: unknown dish_id")
        if row.get("group") not in ("plant", "reference"):
            raise ValueError(f"{key}: group must be plant or reference")
        for field in ("energy_cost_ngn", "labour_cost_ngn", "other_cost_ngn", "prep_minutes", "finished_weight_g"):
            _number(row, field, key, allow_zero=field != "finished_weight_g")
    counts = {key: 0 for key in options}
    seen_pairs: set[tuple[str, str]] = set()
    for row in data.items:
        op = row.get("option_id")
        ing = row.get("ingredient_id")
        if op not in options or ing not in ingredients:
            raise ValueError(f"Unknown option/ingredient in option_items: {op}/{ing}")
        if (op, ing) in seen_pairs:
            raise ValueError(f"Duplicate option ingredient line: {op}/{ing}; combine purchase quantities")
        seen_pairs.add((op, ing))
        _number(row, "purchase_g", f"{op}/{ing}", allow_zero=False)
        keep = _number(row, "nutrient_retention_fraction", f"{op}/{ing}")
        if keep > 1:
            raise ValueError(f"{op}/{ing}: nutrient retention cannot exceed 1")
        if options[op]["group"] == "plant" and ingredients[ing]["is_animal"] == "true":
            raise ValueError(f"{op}: plant option contains animal-derived ingredient {ing}")
        counts[op] += 1
    if any(count == 0 for count in counts.values()):
        raise ValueError("Every option must have at least one ingredient line")
    if not any(o["group"] == "plant" for o in data.options):
        raise ValueError("At least one plant option is required")


def dish_options(data: Dataset, dish_id: str) -> list[dict[str, str]]:
    if dish_id not in {row["dish_id"] for row in data.dishes}:
        raise ValueError(f"Unknown dish: {dish_id}")
    return [op for op in data.options if op["dish_id"] == dish_id]


def _costs(data: Dataset, dish_id: str, price_shock: float) -> list[dict]:
    if not -1 < price_shock <= 2:
        raise ValueError("Price shock must be greater than -100% and at most +200%")
    ingredient = {r["ingredient_id"]: r for r in data.ingredients}
    results = []
    for op in dish_options(data, dish_id):
        lines = [i for i in data.items if i["option_id"] == op["option_id"]]
        values = {"cost": 0.0, "protein": 0.0, "iron": 0.0, "zinc": 0.0}
        references = set()
        allergens: set[str] = set()
        for line in lines:
            ing = ingredient[line["ingredient_id"]]
            allergens.update(a.strip().lower() for a in ing.get("allergens", "").split(";") if a.strip())
            mass = _number(line, "purchase_g", op["option_id"], allow_zero=False)
            retain = _number(line, "nutrient_retention_fraction", op["option_id"])
            values["cost"] += mass * _number(ing, "price_ngn_per_kg", ing["ingredient_id"]) / 1000 * (1 + price_shock)
            for key, col in (("protein", "protein_g_per_100g"), ("iron", "iron_mg_per_100g"), ("zinc", "zinc_mg_per_100g")):
                values[key] += mass * _number(ing, col, ing["ingredient_id"]) / 100 * retain
            references.add(f"{ing['ingredient_id']}: price={ing['price_source']} ({ing['price_date']}, {ing['price_region']}); nutrients={ing['nutrition_source']} [{ing['nutrition_state']}]")
        ingredient_cost = values["cost"]
        processing_cost = sum(_number(op, f, op["option_id"]) for f in ("energy_cost_ngn", "labour_cost_ngn", "other_cost_ngn"))
        values["cost"] += processing_cost
        numeric_health(values)
        values.update(option=op, sources=tuple(sorted(references)), allergens=tuple(sorted(allergens)), ingredient_cost=ingredient_cost, processing_cost=processing_cost)
        results.append(values)
    return results


def _semantic_scores(options: Sequence[dict[str, str]], preference: str) -> dict[str, float]:
    """Small corpus TF-IDF retrieval as an experimental preference matching component.

    This is NOT a validated predictor of flavour, taste, or restaurant acceptance.
    """
    if not preference.strip() or not options:
        return {o["option_id"]: 0.0 for o in options}
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
    except ImportError:
        return {o["option_id"]: 0.0 for o in options}
    corpus = [" ".join((o.get("name", ""), o.get("texture_tags", ""), o.get("method_notes", ""))) for o in options]
    corpus.append(preference)
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
    vectors = vectorizer.fit_transform(corpus)
    similarity = cosine_similarity(vectors[:-1], vectors[-1]).ravel()
    return {o["option_id"]: float(similarity[i]) for i, o in enumerate(options)}


def evaluate(data: Dataset, dish_id: str, *, budget_ngn: float, protein_target_g: float,
             price_shock: float = 0.0, preference: str = "chewy grilled", 
             max_prep_minutes: float = 180.0, avoid_allergens: Sequence[str] = ()) -> list[Evaluation]:
    if not all(math.isfinite(v) for v in (budget_ngn, protein_target_g, max_prep_minutes, price_shock)):
        raise ValueError("Input values must be finite")
    if len(preference) > 200:
        raise ValueError("Preparation preference is limited to 200 characters")
    if budget_ngn <= 0 or protein_target_g < 0 or max_prep_minutes <= 0:
        raise ValueError("Budget and max preparation time must be positive; protein target nonnegative")
    raw = _costs(data, dish_id, price_shock)
    options = [r["option"] for r in raw if r["option"]["group"] == "plant"]
    semantic = _semantic_scores(options, preference)
    output = []
    for r in raw:
        op = r["option"]
        cost, protein = r["cost"], r["protein"]
        prep = _number(op, "prep_minutes", op["option_id"])
        plant = op["group"] == "plant"
        affordable = cost <= budget_ngn + 1e-7
        enough = protein + 1e-7 >= protein_target_g
        timely = prep <= max_prep_minutes
        allergen_conflict = sorted(set(a.strip().lower() for a in avoid_allergens) & set(r["allergens"]))
        feasible = plant and affordable and enough and timely and not allergen_conflict
        reasons = []
        if not plant:
            reasons.append("Beef/reference only; excluded from plant recommendations")
        if not affordable:
            reasons.append("Exceeds ingredient-and-processing budget")
        if not enough:
            reasons.append("Does not reach estimated protein target")
        if not timely:
            reasons.append("Exceeds preparation time limit")
        if allergen_conflict:
            reasons.append("Excluded labeled allergen(s): " + ", ".join(allergen_conflict))
        breakdown: tuple[tuple[str, float], ...] = ()
        if feasible:
            # score = user-visible, explainable multi-criteria recommendation with text retrieval
            cost_score = max(0.0, 1 - cost / budget_ngn)
            protein_score = min(1.0, protein / max(protein_target_g, 1.0))
            time_score = max(0.0, 1 - prep / max_prep_minutes)
            similarity = semantic.get(op["option_id"], 0.0)
            breakdown = (("cost", round(0.45 * cost_score, 5)), ("protein", round(0.25 * protein_score, 5)), ("time", round(0.15 * time_score, 5)), ("text_match", round(0.15 * similarity, 5)))
            score = sum(value for _, value in breakdown)
            reasons.append("Passes budget, estimated protein and preparation constraints")
            reasons.append(f"Preference text match: {similarity:.2f} (experimental, not taste evidence)")
        else:
            score = None
        output.append(Evaluation(
            option_id=op["option_id"], dish_id=dish_id, name=op["name"], group=op["group"],
            cost_ngn=round(cost, 2), protein_g=round(protein, 2), iron_mg=round(r["iron"], 2),
            zinc_mg=round(r["zinc"], 2), finished_g=_number(op, "finished_weight_g", op["option_id"]),
            prep_minutes=prep, under_budget=affordable, meets_protein=enough, plant_only=plant,
            feasible=feasible, score=round(score, 5) if score is not None else None,
            reasons=tuple(reasons), sources=r["sources"], demo=data.demo, allergens=r["allergens"],
            score_breakdown=breakdown, ingredient_cost_ngn=round(r["ingredient_cost"],2), processing_cost_ngn=round(r["processing_cost"],2),
        ))
    return sorted(output, key=lambda x: (not x.feasible, -(x.score or 0), x.cost_ngn, x.option_id))


def baselines(results: Sequence[Evaluation]) -> dict:
    plants = [r for r in results if r.plant_only]
    feasible = [r for r in results if r.feasible]
    beef = [r for r in results if not r.plant_only]
    return {
        "cheapest_plant_unconstrained": min(plants, key=lambda r: r.cost_ngn).option_id if plants else None,
        "cheapest_feasible_plant": min(feasible, key=lambda r: r.cost_ngn).option_id if feasible else None,
        "recommended": feasible[0].option_id if feasible else None,
        "beef_reference": [r.to_dict() for r in beef],
        "no_feasible_option": not bool(feasible),
    }


def sensitivity(data: Dataset, dish_id: str, *, budget_ngn: float, protein_target_g: float,
                preference: str = "chewy grilled", max_prep_minutes: float = 180.0,
                avoid_allergens: Sequence[str] = ()) -> dict[str, list[Evaluation]]:
    return {
        label: evaluate(data, dish_id, budget_ngn=budget_ngn, protein_target_g=protein_target_g,
                        price_shock=shift, preference=preference, max_prep_minutes=max_prep_minutes,
                        avoid_allergens=avoid_allergens)
        for label, shift in (("−20% prices", -0.2), ("Base prices", 0.0), ("+20% prices", 0.2))
    }

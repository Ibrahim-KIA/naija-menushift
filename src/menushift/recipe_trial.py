"""Auditable preparation *trial* cards; not validated cooking instructions.

Steps describe what a food reviewer should test, not a certified kitchen process.
No temperatures, safe holding periods, cooking yields or sensory scores are invented.
"""
from __future__ import annotations

from dataclasses import dataclass

from .kitchen_optimizer import RecipeCandidate


@dataclass(frozen=True)
class TrialStep:
    heading: str
    instruction: str


@dataclass(frozen=True)
class RecipeTrial:
    candidate_id: str
    method: str
    steps: tuple[TrialStep, ...]
    evidence_gaps: tuple[str, ...]
    notes: tuple[str, ...]

    def to_markdown(self, candidate: RecipeCandidate) -> str:
        """Print a plain-text, source-led trial worksheet for an independent reviewer."""
        lines = [
            "# Naija MenuShift — Kitchen Trial Worksheet",
            f"Candidate: {self.method} | {candidate.portion_g:.0f} g FINISHED-WEIGHT ASSUMPTION",
            "STATUS: RESEARCH EXPERIMENT — NOT CERTIFIED OR READY FOR FOOD SERVICE",
            "",
            "## Provisional model output",
            f"Listed cost (incomplete): ₦{candidate.evaluation.cost_ngn:.2f}",
            f"Ingredient portion cost: ₦{candidate.evaluation.ingredient_cost_ngn:.2f}",
            f"Listed preparation cost: ₦{candidate.evaluation.processing_cost_ngn:.2f}",
            f"Estimated protein: {candidate.evaluation.protein_g:.2f} g",
            f"Assumed preparation duration: {candidate.evaluation.prep_minutes:.0f} minutes",
            "Unmeasured processing costs, coagulant, energy, labour and losses may change the result.",
            "",
            "## Ingredient purchase assumptions",
        ]
        for ingredient in candidate.ingredient_lines:
            lines.append(
                f"- {ingredient.name}: {ingredient.purchase_g:.2f} g purchased, "
                f"₦{ingredient.estimated_cost_ngn:.2f} modelled, "
                f"~{ingredient.estimated_protein_g:.2f} g source-referenced protein"
            )
            lines.append(
                f"  Price: {ingredient.source}. Nutrition: {ingredient.nutrition_source} "
                f"({ingredient.nutrition_state}). Label: {ingredient.allergen_labels or 'unreviewed'}."
            )
        if candidate.oil_cl:
            lines.append(
                f"- Oil allowance: {candidate.oil_cl:g} cl assigned to other/processing "
                "cost (NOT measured oil uptake)"
            )
        lines.extend(["", "## Experimental preparation protocol"])
        for number, step in enumerate(self.steps, 1):
            lines.append(f"{number}. {step.heading}: {step.instruction}")
        lines.extend(["", "## Measurements and validation still required"])
        lines.extend(f"- {gap}" for gap in self.evidence_gaps)
        lines.extend(["", "## Safety and interpretation"])
        lines.extend(f"- {note}" for note in self.notes)
        return "\n".join(lines) + "\n"


METHOD_PROCEDURES = {
    "awara_firm": TrialStep(
        "Unpressed trial",
        "Cut a measured portion of firm awara; test whether pieces hold during "
        "handling and grilling. Record breakage and actual finished mass.",
    ),
    "awara_pressed": TrialStep(
        "Pressed trial",
        "Weigh curd before and after pressing, record drained liquid, and assess "
        "handling and chewiness. Pressing removes water; it does not create protein.",
    ),
    "awara_frozen": TrialStep(
        "Freeze–thaw trial",
        "Use the kitchen's documented safe cold-storage and thawing procedure; "
        "measure freeze/thaw time, lost liquid and skewer stability. The displayed "
        "time is NOT a measured full freeze–thaw cycle.",
    ),
    "awara_fried": TrialStep(
        "Fried trial",
        "Weigh the curd before and after frying and record oil used, oil retained, "
        "fuel and texture. Do not treat the generic fried-tofu nutrient profile as "
        "a measurement of this recipe.",
    ),
}


def build_trial(candidate: RecipeCandidate) -> RecipeTrial:
    """Generate a transparent test protocol only for a hard-constraint eligible option."""
    if not candidate.eligible:
        raise ValueError("Cannot create a suggested trial card for an ineligible recipe")
    method = candidate.evaluation.option_id
    if method not in METHOD_PROCEDURES:
        raise ValueError("Unknown or unsupported trial preparation method")
    steps = (
        TrialStep(
            "Verify stock and labels",
            "Check the physical ingredient packages, declared soy and seasoning "
            "allergens and actual availability. Check shared-surface cross-contact "
            "with the food-safety lead before preparing for anyone.",
        ),
        TrialStep(
            "Record starting material",
            "Weigh purchased awara and every selected spice/seasoning separately. "
            "Record actual local prices, date, market and package size.",
        ),
        METHOD_PROCEDURES[method],
        TrialStep(
            "Seasoning study",
            "Use only ingredients whose labels and quantities were reviewed by the "
            "team. A full suya yaji formulation is NOT yet validated by this dataset.",
        ),
        TrialStep(
            "Grill and record",
            "Have the food-science reviewer set a safe cooking and handling protocol. "
            "Record fuel use, time, skewering/basket stability, and finished portion mass.",
        ),
        TrialStep(
            "Blind sensory check",
            "Use an agreed scoring sheet for texture, aroma, appearance, flavour and "
            "acceptability. Record actual reviewer responses; do not infer taste from text.",
        ),
    )
    gaps = (
        "Local finished-awara supplier quote or measured soy-to-tofu batch manufacturing cost",
        "Measured purchased-to-finished yield (including pressing/freezing/frying losses)",
        "Method-specific electricity, gas/charcoal, labour, coagulant and packaging costs",
        "Measured oil uptake where fried; genuine prep duration including freeze/thaw",
        "Matched local food-form nutritional analysis and nutrient retention",
        "Yaji/seasoning recipe, source, animal-derived ingredients and allergen review",
        "Food-safety review and recorded blind sensory panel before any service claim",
    )
    notes = (
        "All numerical estimates may be incomplete; do not call this a retail price or full cost.",
        "Soy is present. Unreviewed ingredient labels and cross-contact cannot be certified safe.",
        "A modelled protein target is not a clinical or dietary adequacy claim.",
        "The option must be approved and tested by an appropriate food/kitchen professional.",
    )
    return RecipeTrial(candidate.identifier, candidate.method, steps, gaps, notes)

"use client";

import { useRef, useState } from "react";
import type { Brief, Candidate, ExploreResult } from "@/lib/engine";
import { DATASET_NOTE } from "@/lib/data";
import CandidateDetail, { money } from "./CandidateDetail";
import RecipeBook from "./RecipeBook";

const objectives = [
  { key: "budget", label: "Lowest listed cost" },
  { key: "protein", label: "Most estimated protein" },
  { key: "kitchen", label: "Shortest assumed prep" },
] as const;

export function RecommendationResults({ result, brief, rice, servings, dietaryReview }: {
  result: ExploreResult;
  brief: Brief;
  rice: boolean;
  servings: number;
  dietaryReview: string;
}) {
  const eligible = new Set(result.eligibleIds);
  const options = result.candidates.filter((c) => c.feasible && eligible.has(c.identifier));
  const rejected = result.candidates.filter((c) => !c.feasible);
  const [chosen, setChosen] = useState(result.best.budget ?? options[0]?.identifier ?? "");
  const [comparisonOpen, setComparisonOpen] = useState(false);
  const comparison = useRef<HTMLHeadingElement>(null);
  const selected = options.find((option) => option.identifier === chosen);
  const reference = result.reference.find((item) => item.portionG === selected?.portionG);
  const picks = objectives.reduce<{ option: Candidate; labels: string[] }[]>((cards, objective) => {
    const option = options.find((item) => item.identifier === result.best[objective.key]);
    if (!option) return cards;
    const previous = cards.find((card) => card.option.identifier === option.identifier);
    if (previous) previous.labels.push(objective.label);
    else cards.push({ option, labels: [objective.label] });
    return cards;
  }, []);

  return (
    <div className="studio-results">
      <p className="studio-result-status" role="status"><strong>{options.length} {options.length === 1 ? "option fits" : "options fit"}</strong> · {result.inspected} portions checked</p>
      <p className="ns-note studio-caveat">Suya values are research estimates. Check actual costs, yields and supplier labels before service.</p>
      {options.length === 0 && (
        <div className="studio-empty">
          <h4>No options meet this brief</h4>
          <p>Review the checks below to see what ruled out the options. You can edit your budget, target, equipment or stock. Keep any required allergen exclusions in place.</p>
        </div>
      )}
      {options.length > 0 && (
        <label className="ns-field studio-all-options">
          <span className="ns-label">Choose the recipe to view</span>
          <select value={chosen} onChange={(event) => setChosen(event.target.value)}>
            {options.map((item) => <option key={item.identifier} value={item.identifier}>{item.method} · {item.portionG} g</option>)}
          </select>
        </label>
      )}
      {selected && <RecipeBook candidate={selected} rice={rice} dietaryReview={dietaryReview} />}
      {picks.length > 0 && (
        <details className="studio-disclosure studio-optional-results">
          <summary>Compare other ranking priorities ({picks.length})</summary>
        <div className="studio-option-grid">
          {picks.map(({ option, labels }) => (
            <article className="studio-recommendation" key={option.identifier} data-selected={chosen === option.identifier}>
              <p className="studio-tag">{labels.join(" · ")}</p>
              <h4>{option.method}</h4>
              <p className="ns-note">{option.portionG} g modelled portion</p>
              <dl className="studio-card-stats">
                <div><dt>Listed cost</dt><dd>{money(option.costNgn)}</dd></div>
                <div><dt>Est. protein</dt><dd>{option.proteinG.toFixed(1)} g</dd></div>
                <div><dt>Assumed prep</dt><dd>{option.prepMinutes} min</dd></div>
              </dl>
              <button type="button" className="studio-secondary" aria-pressed={chosen === option.identifier}
                onClick={() => { setChosen(option.identifier); setComparisonOpen(true); requestAnimationFrame(() => comparison.current?.focus()); }}>
                Compare this option
              </button>
            </article>
          ))}
        </div>
        </details>
      )}
      {selected && (
        <details className="studio-disclosure studio-comparison-details" open={comparisonOpen} onToggle={(event) => setComparisonOpen(event.currentTarget.open)}>
          <summary>Compare with beef, inspect sources and plan a kitchen trial</summary>
          <CandidateDetail key={selected.identifier} heading={comparison} candidate={selected} reference={reference} brief={brief} rice={rice} initialServings={servings} />
        </details>
      )}
      <details className="studio-disclosure" open={options.length === 0 || undefined}>
        <summary>Why options were ruled out</summary>
        <ul>
          {result.skippedEquipment > 0 && <li>{result.skippedEquipment} skipped because required equipment was unavailable.</li>}
          {result.skippedIngredients > 0 && <li>{result.skippedIngredients} skipped because required ingredients were unavailable.</li>}
          {result.skippedUnverifiedYaji > 0 && <li>{result.skippedUnverifiedYaji} skipped because the dataset has no verified peanut-free yaji for those options.</li>}
          {rejected.length === 0 && result.skippedEquipment + result.skippedIngredients + result.skippedUnverifiedYaji === 0 && <li>Every evaluated option met the entered constraints.</li>}
        </ul>
        {rejected.length > 0 && (
          <ul className="studio-rejections">
            {rejected.map((item) => (
              <li key={item.identifier}><strong>{item.method} · {item.portionG} g</strong><span>{item.reasons.join(" · ")}</span></li>
            ))}
          </ul>
        )}
      </details>
      <details className="studio-disclosure">
        <summary>About the research data and limitations</summary>
        <p className="ns-note">{DATASET_NOTE}</p>
      </details>
    </div>
  );
}

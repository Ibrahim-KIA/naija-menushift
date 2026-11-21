"use client";

import { useState, type Ref } from "react";
import { EQUIPMENT_LABELS, INVENTORY_ITEMS, MEASUREMENTS_NEEDED, TRIAL_STEPS } from "@/lib/data";
import type { Brief, Candidate, ReferenceEvaluation } from "@/lib/engine";
import { buildWorksheet } from "@/lib/worksheet";

export const money = (value: number) =>
  new Intl.NumberFormat("en-NG", { style: "currency", currency: "NGN" }).format(value);

const riceProtein = 150 * 2.3 / 100;

export default function CandidateDetail({ heading, candidate, reference, brief, rice, initialServings }: {
  heading: Ref<HTMLHeadingElement>;
  candidate: Candidate;
  reference: ReferenceEvaluation | undefined;
  brief: Brief;
  rice: boolean;
  initialServings: number;
}) {
  const [servings, setServings] = useState(String(initialServings));
  const count = Number(servings);
  const validCount = Number.isInteger(count) && count > 0 && count <= 10000;
  const side = rice ? riceProtein : 0;
  const weights = (grams: number) => `${(grams * count / 1000).toLocaleString("en-NG", { maximumFractionDigits: 3 })} kg`;
  const sourceId = candidate.ingredientLines.some((line) => line.ingredientId === "fried_awara") ? "172451" : "172475";

  function download() {
    const batchNotes = validCount
      ? `\n## Trial volume\n- Modelled portions: ${count}\n- Finished awara portion mass: ${weights(candidate.portionG)}\n- Scaled listed suya component cost: ${money(candidate.costNgn * count)}\n- Linear scaling uses unverified yields and excludes labour, waste and rice. Batch cooking time is unestimated.\n`
      : "";
    const file = new Blob([buildWorksheet(candidate, brief), batchNotes], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(file);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `menushift-trial-${candidate.identifier.replace("@", "-")}.md`;
    anchor.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  return (
    <article className="studio-comparison" aria-labelledby="comparison-title">
      <h4 ref={heading} id="comparison-title" tabIndex={-1}>Original vs. alternative</h4>
      <p className="ns-note">{candidate.portionG} g suya portion on each side{rice ? " with 150 g plain boiled rice" : ""}. Costs cover listed suya ingredients and processing. Prep is an assumption.</p>
      <div className="studio-option-grid studio-option-grid--two">
        <section className="studio-plate">
          <p className="studio-tag">Original</p>
          <h5>Beef suya</h5>
          {reference ? (
            <dl><div><dt>Listed suya cost</dt><dd>{money(reference.costNgn)}</dd></div>
              <div><dt>Estimated protein</dt><dd>{(reference.proteinG + side).toFixed(1)} g</dd></div>
              <div><dt>Assumed suya prep</dt><dd>{reference.prepMinutes} min</dd></div></dl>
          ) : <p>A matching beef portion is unavailable.</p>}
        </section>
        <section className="studio-plate studio-plate--adapted">
          <p className="studio-tag">Plant-based alternative</p>
          <h5>{candidate.method}</h5>
          <dl><div><dt>Listed suya cost</dt><dd>{money(candidate.costNgn)}</dd></div>
            <div><dt>Estimated protein</dt><dd>{(candidate.proteinG + side).toFixed(1)} g</dd></div>
            <div><dt>Assumed suya prep</dt><dd>{candidate.prepMinutes} min</dd></div></dl>
        </section>
      </div>
      {rice && <p className="ns-note">Rice adds 3.45 g estimated protein to each side. Cost and prep exclude rice. <a href="https://www.fao.org/infoods/infoods/tables-and-databases/faoinfoods-databases/en">FAO/INFOODS WAFCT, 01_069</a>.</p>}
      <details className="studio-disclosure">
        <summary>Why {candidate.method.toLowerCase()} qualifies</summary>
        <ul>
          <li>{money(candidate.costNgn)} listed cost within your {money(brief.budgetNgn)} limit.</li>
          <li>{candidate.proteinG.toFixed(1)} g estimated suya protein against your {brief.proteinTargetG} g target.</li>
          <li>{candidate.prepMinutes} minutes assumed prep against your {brief.maxPrepMinutes}-minute limit.</li>
          <li>Equipment in the brief includes {candidate.requiredEquipment.map((id) => EQUIPMENT_LABELS[id] ?? id).join(", ")}. Required stock includes {candidate.requiredInventory.map((id) => INVENTORY_ITEMS[id] ?? id).join(", ")}.</li>
          <li>Allergens on record: {candidate.allergens.join(", ") || "none recorded"}. Exclusions requested: {brief.avoidAllergens.join(", ") || "none"}. Confirm labels and cross-contact, including the yaji blend, before serving.</li>
        </ul>
        {candidate.reasons.length > 0 && <ul>{candidate.reasons.map((reason) => <li key={reason}>{reason}</li>)}</ul>}
        {candidate.scoreBreakdown.length > 0 && <p className="ns-note">Ranking factors: {candidate.scoreBreakdown.map((part) => `${part.label} ${part.value.toFixed(3)}`).join(" · ")}.</p>}
      </details>
      <details className="studio-disclosure">
        <summary>Sources and evidence quality</summary>
        <p>Estimated minerals for the awara component are {candidate.ironMg.toFixed(2)} mg iron and {candidate.zincMg.toFixed(2)} mg zinc. Pressing and freezing change moisture and serving weight. The model uses tofu nutrient references and assumed yields. It cannot establish local batch nutrition.</p>
        <p><a href={`https://fdc.nal.usda.gov/food-details/${sourceId}/nutrients`}>USDA tofu composition reference</a></p>
        <ul>{candidate.sources.map((source) => <li key={source}>{source}</li>)}</ul>
        <ul className="studio-evidence-list">
          {candidate.ingredientLines.map((line) => <li key={line.ingredientId}>
            <strong>{line.name} · {line.purchaseG} g purchase weight · {money(line.estimatedCostNgn)}</strong>
            <span>{line.nutritionState}. {line.nutritionSource}. {line.priceSource}. Allergen label: {line.allergenLabels}.</span>
          </li>)}
        </ul>
      </details>
      <details className="studio-disclosure">
        <summary>Meal visualisation prompt</summary>
        <p>Copy this prompt into an image tool for a concept illustration. Live image generation is unavailable in the studio.</p>
        <p className="ns-prompt">Concept illustration of Nigerian suya-style skewers using {candidate.ingredientLines.map((line) => line.name.toLowerCase()).join(", ")}{rice ? ", served with plain boiled rice" : ""}. Show the {candidate.method.toLowerCase()} preparation. Depict the listed ingredients only. Label the image “Concept illustration”.</p>
      </details>
      <section className="studio-trial" aria-labelledby="trial-title">
        <div><h5 id="trial-title">Plan a kitchen trial</h5><p className="ns-note">Scale the selected suya portion and take the evidence into a supervised trial.</p></div>
        <label className="ns-field">
          <span className="ns-label">Trial portions</span>
          <input type="number" min={1} max={10000} step={1} value={servings} onChange={(event) => setServings(event.target.value)} />
        </label>
        <p className="studio-batch" aria-live="polite">{validCount ? <><strong>{weights(candidate.portionG)}</strong> modelled awara portions · <strong>{money(candidate.costNgn * count)}</strong> scaled listed costs.</> : "Enter 1–10,000 whole portions."}</p>
        <p className="ns-note">Linear estimate. Allow for labour, loss, seasoning, rice and actual batch yield before purchasing. Batch prep time is unestimated.</p>
        <details className="studio-disclosure">
          <summary>Trial steps and measurements to collect</summary>
          <ol>{(TRIAL_STEPS[candidate.methodId] ?? []).map((step) => <li key={step}>{step}</li>)}</ol>
          <ul>{MEASUREMENTS_NEEDED.map((item) => <li key={item}>{item}</li>)}</ul>
        </details>
        <button type="button" className="studio-secondary" onClick={download}>Download trial worksheet</button>
      </section>
    </article>
  );
}

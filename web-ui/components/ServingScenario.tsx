"use client";

import { useState } from "react";

const fields = [
  { id: "meals", label: "Meals per day", initial: "500", max: 1000000 },
  { id: "days", label: "Operating days per year", initial: "180", max: 366 },
  { id: "share", label: "Share that shifts (%)", initial: "10", max: 100 },
  { id: "beef", label: "Beef per original portion (g)", initial: "60", max: 10000 },
] as const;

const number = new Intl.NumberFormat("en-NG", { maximumFractionDigits: 2 });

export default function ServingScenario() {
  const [inputs, setInputs] = useState<Record<string, string>>(
    Object.fromEntries(fields.map(({ id, initial }) => [id, initial])),
  );
  const valid = fields.every(({ id, max }) => {
    const value = Number(inputs[id]);
    return inputs[id].trim() !== "" && Number.isInteger(value) && value >= 0 && value <= max;
  });
  const adapted = Math.floor(Number(inputs.meals) * Number(inputs.days) * Number(inputs.share) / 100);

  return (
    <details className="ns-plate-plan">
      <summary>Estimate annual serving volumes</summary>
      <p>Illustrative scenario for a kitchen that adds a plant-based choice. Enter whole numbers to estimate take-up and the corresponding difference in beef portions.</p>
      <div className="ns-use-cases">
        {fields.map(({ id, label, max }) => (
          <label className="ns-field" key={id} htmlFor={`scenario-${id}`}>
            <span className="ns-label">{label}</span>
            <input id={`scenario-${id}`} type="number" min={0} max={max} step={1}
              value={inputs[id]} onChange={(event) => setInputs((previous) => ({ ...previous, [id]: event.target.value }))} />
          </label>
        ))}
      </div>
      <p aria-live="polite">{valid ? <>
        <strong>{number.format(adapted)}</strong> adapted portions a year · <strong>{number.format(adapted * Number(inputs.beef) / 1000)} kg</strong> of beef corresponding to those portions. This scenario assumes purchasing changes in proportion to portions served.
      </> : "Enter values within the ranges shown by the inputs."}</p>
    </details>
  );
}

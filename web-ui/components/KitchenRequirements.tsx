"use client";

import { useState } from "react";
import { ALL_EQUIPMENT, ALL_INVENTORY, EQUIPMENT_LABELS, INVENTORY_ITEMS } from "@/lib/data";
import type { Brief } from "@/lib/engine";

const PORTION_CHOICES = [80, 100, 120, 140, 160, 180, 200];

function toggle(list: string[], value: string) {
  return list.includes(value) ? list.filter((v) => v !== value) : [...list, value];
}

function NumberConstraint({ id, label, value, options, minimum, onChange }: {
  id: string; label: string; value: number; options: number[]; minimum: number; onChange: (value: number) => void;
}) {
  const [custom, setCustom] = useState(!options.includes(value));
  return (
    <div className="ns-field">
      <label className="ns-label" htmlFor={id}>{label}</label>
      <select id={id} value={custom || !options.includes(value) ? "custom" : value} onChange={(event) => {
        setCustom(event.target.value === "custom");
        if (event.target.value !== "custom") onChange(Number(event.target.value));
      }}>
        {options.map((option) => <option key={option} value={option}>{option.toLocaleString("en-NG")}</option>)}
        <option value="custom">Custom amount</option>
      </select>
      {(custom || !options.includes(value)) && <label className="ns-field">
        <span className="ns-label">Custom {label.toLowerCase()}</span>
        <input type="number" required min={minimum} value={value} onChange={(event) => onChange(Number(event.target.value))} />
      </label>}
    </div>
  );
}

export default function KitchenRequirements({ brief, patch }: {
  brief: Brief;
  patch: (update: Partial<Brief>) => void;
}) {
  return (
    <>
      <div className="studio-inputs">
        <NumberConstraint id="budget" label="Ingredient budget (₦)" value={brief.budgetNgn} options={[50, 100, 500, 1500, 3000]}
          minimum={1} onChange={(budgetNgn) => patch({ budgetNgn })} />
        <NumberConstraint id="protein" label="Protein target (g)" value={brief.proteinTargetG} options={[0, 10, 15, 20, 30]}
          minimum={0} onChange={(proteinTargetG) => patch({ proteinTargetG })} />
        <NumberConstraint id="prep" label="Prep time limit (minutes)" value={brief.maxPrepMinutes} options={[35, 45, 60, 90, 120]}
          minimum={1} onChange={(maxPrepMinutes) => patch({ maxPrepMinutes })} />
      </div>
      <p className="ns-note">Protein uses reference data. The budget covers listed suya ingredients and processing per portion.</p>
          <label className="ns-field">
            <span className="ns-label">Preferred texture or preparation</span>
            <input
              type="text"
              maxLength={200}
              value={brief.preference}
              onChange={(e) => patch({ preference: e.target.value })}
              placeholder="e.g. chewy grilled"
            />
            <span className="ns-note">
              Used to rank matching words after the kitchen checks.
            </span>
          </label>

      <div className="studio-constraints">
        <label className="ns-field">
          <span className="ns-label">Allergen exclusions</span>
          <select value={[...brief.avoidAllergens].sort().join(",")} onChange={(event) => patch({
            avoidAllergens: event.target.value ? event.target.value.split(",") : [],
          })}>
            <option value="">No exclusions entered</option>
            <option value="soy">Exclude soy</option>
            <option value="peanut">Exclude peanut / groundnut</option>
            <option value="peanut,soy">Exclude soy and peanut / groundnut</option>
          </select>
          <span className="ns-note">Awara contains soy. Peanut exclusion requires a verified peanut-free yaji, which is unavailable in this dataset.</span>
        </label>
<details className="ns-advanced"><summary>Equipment and stock</summary>          <fieldset className="ns-fieldset">
            <legend className="ns-label">Available equipment</legend>
            {ALL_EQUIPMENT.map((id) => (
              <label key={id} className="ns-check">
                <input
                  type="checkbox"
                  checked={brief.equipment.includes(id)}
                  onChange={() => patch({ equipment: toggle(brief.equipment, id) })}
                />
                <span>{EQUIPMENT_LABELS[id]}</span>
              </label>
            ))}
          </fieldset>

          <fieldset className="ns-fieldset">
            <legend className="ns-label">Ingredients in stock</legend>
            {ALL_INVENTORY.map((id) => (
              <label key={id} className="ns-check">
                <input
                  type="checkbox"
                  checked={(brief.availableIngredients ?? []).includes(id)}
                  onChange={() =>
                    patch({
                      availableIngredients: toggle(brief.availableIngredients ?? [], id),
                    })
                  }
                />
                <span>{INVENTORY_ITEMS[id]}</span>
              </label>
            ))}
          </fieldset>

</details></div>          <details className="ns-advanced">
            <summary>Advanced assumptions</summary>
            <fieldset className="ns-fieldset">
              <legend className="ns-label">Modelled portion sizes (g)</legend>
              <div className="ns-checkrow">
                {PORTION_CHOICES.map((p) => (
                  <label key={p} className="ns-check ns-check--chip">
                    <input
                      type="checkbox"
                      checked={brief.portionsG.includes(p)}
                      onChange={() => {
                        const next = brief.portionsG.includes(p)
                          ? brief.portionsG.filter((x) => x !== p)
                          : [...brief.portionsG, p].sort((a, b) => a - b);
                        if (next.length > 0) patch({ portionsG: next });
                      }}
                    />
                    <span>{p}</span>
                  </label>
                ))}
              </div>
            </fieldset>

            <div className="ns-grid2">
              <label className="ns-field">
                <span className="ns-label">Wet-curd yield (kg per kg dry soy)</span>
                <input
                  type="number"
                  step={0.05}
                  min={0.1}
                  max={10}
                  value={brief.wetYieldKgPerKgDry}
                  onChange={(e) => patch({ wetYieldKgPerKgDry: Number(e.target.value) })}
                />
              </label>
              <label className="ns-field">
                <span className="ns-label">Oil for frying (cl)</span>
                <input
                  type="number"
                  step={0.5}
                  min={0}
                  value={brief.oilCl}
                  onChange={(e) => patch({ oilCl: Number(e.target.value) })}
                />
              </label>
              <label className="ns-field">
                <span className="ns-label">Onion (g)</span>
                <input
                  type="number"
                  min={0}
                  value={brief.onionG}
                  onChange={(e) => patch({ onionG: Number(e.target.value) })}
                />
              </label>
              <label className="ns-field">
                <span className="ns-label">Pepper (g)</span>
                <input
                  type="number"
                  min={0}
                  value={brief.pepperG}
                  onChange={(e) => patch({ pepperG: Number(e.target.value) })}
                />
              </label>
              <label className="ns-field">
                <span className="ns-label">Salt (g)</span>
                <input
                  type="number"
                  min={0}
                  value={brief.saltG}
                  onChange={(e) => patch({ saltG: Number(e.target.value) })}
                />
              </label>
              <label className="ns-field">
                <span className="ns-label">Seasoning (g) — label unreviewed</span>
                <input
                  type="number"
                  min={0}
                  value={brief.seasoningG}
                  onChange={(e) => patch({ seasoningG: Number(e.target.value) })}
                />
              </label>
            </div>

            <label className="ns-field">
              <span className="ns-label">Price scenario (not a forecast)</span>
              <select
                value={String(brief.priceShock)}
                onChange={(e) => patch({ priceShock: Number(e.target.value) })}
              >
                <option value="-0.2">−20% prices</option>
                <option value="0">Base prices</option>
                <option value="0.2">+20% prices</option>
              </select>
            </label>
          </details>
    </>
  );
}

"use client";

import { ALLERGEN_OPTIONS, ALL_EQUIPMENT, ALL_INVENTORY, EQUIPMENT_LABELS, INVENTORY_ITEMS } from "@/lib/data";
import type { Brief } from "@/lib/engine";

const PORTION_CHOICES = [80, 100, 120, 140, 160, 180, 200];

function toggle(list: string[], value: string) {
  return list.includes(value) ? list.filter((v) => v !== value) : [...list, value];
}

export default function KitchenRequirements({ brief, patch }: {
  brief: Brief;
  patch: (update: Partial<Brief>) => void;
}) {
  return (
    <>
<div className="studio-inputs">          <div className="ns-field">
            <label className="ns-label" htmlFor="budget">
              Ingredient budget (₦)
            </label>
            <div className="ns-dual">
              <input
                id="budget"
                type="number"
                min={1}
                value={brief.budgetNgn}
                onChange={(e) => patch({ budgetNgn: Number(e.target.value) })}
              />
              <input
                type="range"
                min={100}
                max={3000}
                step={50}
                value={Math.min(3000, Math.max(100, brief.budgetNgn))}
                onChange={(e) => patch({ budgetNgn: Number(e.target.value) })}
                aria-label="Budget slider"
              />
            </div>
            <p className="ns-note">Listed ingredients and processing per portion.</p>
          </div>

          <div className="ns-field">
            <label className="ns-label" htmlFor="protein">
              Protein target (g)
            </label>
            <div className="ns-dual">
              <input
                id="protein"
                type="number"
                min={0}
                max={60}
                value={brief.proteinTargetG}
                onChange={(e) => patch({ proteinTargetG: Number(e.target.value) })}
              />
              <input
                type="range"
                min={0}
                max={40}
                step={1}
                value={Math.min(40, brief.proteinTargetG)}
                onChange={(e) => patch({ proteinTargetG: Number(e.target.value) })}
                aria-label="Protein target slider"
              />
            </div>
          </div>

          <div className="ns-field">
            <label className="ns-label" htmlFor="prep">
              Prep time limit (min)
            </label>
            <div className="ns-dual">
              <input
                id="prep"
                type="number"
                min={1}
                value={brief.maxPrepMinutes}
                onChange={(e) => patch({ maxPrepMinutes: Number(e.target.value) })}
              />
              <input
                type="range"
                min={15}
                max={240}
                step={5}
                value={Math.min(240, Math.max(15, brief.maxPrepMinutes))}
                onChange={(e) => patch({ maxPrepMinutes: Number(e.target.value) })}
                aria-label="Preparation time slider"
              />
            </div>
          </div>

          </div>
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

<div className="studio-constraints">          <fieldset className="ns-fieldset">
            <legend className="ns-label">Exclude allergens</legend>
            {ALLERGEN_OPTIONS.map((a) => (
              <div key={a.id}>
                <label className="ns-check">
                  <input
                    type="checkbox"
                    checked={brief.avoidAllergens.includes(a.id)}
                    onChange={() =>
                      patch({ avoidAllergens: toggle(brief.avoidAllergens, a.id) })
                    }
                  />
                  <span>Avoid {a.label}</span>
                </label>
                <p className="ns-note ns-note--indent">{a.hint}</p>
              </div>
            ))}
          </fieldset>

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

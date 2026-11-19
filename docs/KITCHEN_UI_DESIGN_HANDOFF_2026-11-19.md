# Kitchen Intelligence Studio — Desktop / Mobile Figma and UI implementation handoff
**19 November 2026 • UX system to implement and visually test**

The Streamlit UI exists on feature/kitchen-intelligence-studio-2026-11-19 (PR #14), with follow-on constraints and recipe worksheets in PR #15. **This document is an editable-design brief, NOT evidence that Figma frames have been created or visually audited.** Figma file ownership awaits selection of the destination team/plan.

## Personas and main decision
Primary: independent Nigerian restaurant owner/caterer who needs a practical plant-protein menu alternative at a target *listed cost* and within available ingredients/equipment. Secondary: hackathon judge or food-science reviewer who needs evidence and uncertainty.

Goal: Find a viable *research formulation for kitchen testing* in under four steps. Do not label results "safe", "delicious", "measured" or "retail-priced".

## Visual identity (matches existing Streamlit CSS and theme)
- Forest `#173B2D`, dark green `#102C22`, rich green `#1B5940`, warm cream `#FBFAF5`, gold accent `#BC8948`, light border `#D8E2D9`.
- Header wordmark: Naija MenuShift (text; no unapproved logos). Brand voice: confident and approachable, not a sterile AI dashboard.
- Typography: accessible sans-serif, large hero, concise body, tabular numbers for naira values, reduced saturation for secondary metadata.
- Grid: max width 1180px, responsive native columns, generous spacing; focus outlines visible at all interactive controls.
- Status: warning text with explicit labels, not just color. Unreviewed data is always visible at the point of decision.

## Desktop layout target (1440×1024 viewport, scroll)
1. Small product header, premium hero panel, purpose line and visible research warning.
2. Four-step progress pill bar.
3. Dish selector and constraint panel. Primary controls: budget for **listed partial costs**, protein target, max assumed time, desired characteristics, available equipment, available ingredients.
4. Advanced assumptions collapsed: source-food yield, modelled portions, spice quantities, unverified seasoning, oil, allergen exclusion, price sensitivity.
5. Result summary: candidate count, eligible count, Pareto frontier count, exclusions for missing equipment/stock/yaji.
6. Three decision cards across desktop width: cheapest feasible, highest estimated protein, shortest assumed prep.
7. Source-traceable details: why suggested, estimated ingredient quantities and prices, nutrition source state, preparation trial steps and download link.
8. Chart and methods/explanation in secondary expandable sections.

## Mobile layout target (390×844 and 320px width)
1. Hero is compact and readable; no full-viewport ornamental element hiding the decision inputs.
2. Step pills wrap and stay readable; all sections follow single-column DOM order.
3. Inputs use native labels and full-width hit targets. No 3-column tiny inputs in mobile; verify responsive stacking.
4. Cards appear in one column with cost/protein/time visible, no clipping, larger touch controls.
5. Long source text and tables can scroll horizontally only inside the table viewport; entire page must not horizontally overflow.
6. Main warning and reasons remain near the result, not hidden in a sidebar.
7. At 200% zoom and keyboard-only use, controls, focus and no-feasible state must remain usable.

## UI component states to design in Figma
- Normal eligibility; low-budget abstention; unavailable equipment; missing awara; unreviewed seasoning; soy exclusion; peanut/yaji exclusion; missing evidence; downloadable trial worksheet.
- Cards: budget-first / protein-first / kitchen-first, including when multiple objectives select the **same** candidate (no artificial diversity).
- Evidence badges: "source reference", "modelled", "measured" (last only after independently approved data exists), "unreviewed".
- Trial card: not a retail recipe or commercial price; warnings and citations above action links.

## Interactions and acceptance
- Every constraint update triggers deterministic recalculation; no paid AI invocation on page load.
- The hard restriction gate cannot be bypassed by scores or LLM text.
- Score explanations are secondary; the restaurant owner must always see cost, protein and practicality first.
- Downloaded worksheet includes recipe ID, ingredient grams, price/nutrient sources, calculation caveats and required field measurements.
- Output content must not embed user input into unsafe HTML.
- Test no-soy and no-peanut cases; the latter abstains because verified peanut-free yaji does not exist yet.
- Accessibility acceptance requires screenshot/viewport tests and keyboard/screen-reader review; the Python CI checks do not provide these.

## Suggested Figma frames (after choosing target plan)
- Desktop / Main decision (1440×1024)
- Desktop / Recommended candidate and evidence (1440×1024)
- Desktop / No eligible formulation (1440×1024)
- Mobile / Main decision (390×844)
- Mobile / Recommended candidate (390×844)
- Mobile / No eligible formulation (390×844)
- Small component sheet for three outcome cards, constraints, warnings and disclosure status.

**Design review status:** Code and specification prepared; Figma Design file and device screenshots remain outstanding until plan selection and visual testing.

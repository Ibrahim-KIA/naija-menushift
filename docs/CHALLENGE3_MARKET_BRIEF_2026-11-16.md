# Challenge 3 — Nigeria Alt-Protein Market Opportunity
**Decision brief · 16 November 2026 · Hack the Fork Nigeria 2026**

## Executive result

**Build complete enough to demonstrate the scoring/segmentation workflow; NO evidence-backed winner is established.** The team has 48 candidate opportunities (two products × six cities × four buyer segments), 2024 *state-level* soybean output, and general market and scientific background. The new dataset has **zero product-specific survey responses, zero observed demand signals, and no 1–5 scores**, so the real opportunity model **abstains**.

**Recommendation for immediate fieldwork, not a market winner:**
1. **Tofu suya:** investigate Kano and Kaduna suya/campus vendors, specifically comparative portion price, purchase frequency, vendor willingness, skewer stability, seasoning, and cold holding. Test Lagos competitor positioning against a documented existing tofu-suya offer.
2. **Kafi soy yoghurt:** investigate Kano/Kaduna kiosks and neighbourhood grocers, then Abuja outlets, for pack sizes, affordable target price, preference for fermented soy vs dairy yoghurt, vendor stocking interest, repeat purchases, packaging and cold chain.
3. **Lagos/Abuja:** include for competitive and channel comparisons; **Jos/Ibadan:** additional cross-region controls.
4. **No national demand, market size, revenue or optimal city claims** until observed inputs exist.

## Meeting — Sunday 15 Nov 2026: source-reported decisions
The team joined an introductory alternative-protein session; meeting summary was supplied by Ibrahim on 16 Nov. External read.ai and tl;dv links could not be independently fetched, so the user-provided notes govern this synopsis.

- Alternative proteins: plant, fermentation and cultivated; hackathon explicitly focuses on plant/fermentation; insect protein is out of scope.
- Ingredient functionality matters as much as grams of protein: solubility, water holding, emulsification and gelation.
- Challenge 1 ranks functional ingredients; **Challenge 2 recommends plant-based dish adaptations under constraints**; **Challenge 3 segments and scores markets to decide where to launch**.
- Judges expect AI to be substantive, assumptions and failures disclosed, and mentor engagement.
- Abdulhakeem to share introductory slides with group. The uploaded seven-page "Alternative Proteins 101 for AI Builders" deck is available.
- Team agreed to complete **Challenge 3 today (Monday 16 November)**. Ibrahim and Muhammad explicitly tagged.
- Amina explained some of her research was organised using AI, and submitted a market document and two-product dataset. **AI-assisted formatting/source retrieval is not itself source verification.**

## Product/market scope
**Tofu suya** is ready-to-eat plant-based suya; **Kafi** is a proposed soy yoghurt. These are not necessarily existing brands or proven enterprises. Distinguish the *Challenge 3 consumer food market* from **Naija MenuShift's Challenge 2 restaurant decision-support software**; SaaS/customer segmentation is a separate business model and must not be substituted for the food-product market.

### 48-row opportunity unit
- Products: Tofu suya; Kafi soy yoghurt.
- Cities: Kano, Kaduna, Jos, Abuja, Lagos, Ibadan.
- Segments: households/general consumers; students/young adults; health-conscious consumers; vegetarian/flexitarian/meat reducers.
- Formula: (Demand×30 + Affordability×25 + Channel×20 + Supply/distribution×15 + Market gap×10) / 5, on 1–5 inputs, result **20–100**.
- Weights are **team hypotheses**, not official judging weights. Compare ranking stability under alternative weights.
- If **any supporting evidence is missing**, no numeric score or winner is produced. Do not interpret missing data as a score of zero.

## Source-backed findings (not product-specific sales data)

1. **Soy production:** NAERLS/FMAFS estimated 2024 Nigeria soybean output **947,952.08 tonnes**. In the workbook: Kaduna **93,741.86 t**, Kano **66,915.95 t**, Plateau **25,172.74 t**, FCT **29,065.91 t**, Oyo **24,114 t**. These are state-level output, not city availability to a tofu or yoghurt manufacturer. Source: https://naerls.gov.ng/wp-content/uploads/2025/04/Agricultural-Performance-Survey-of-2024-Wet-Season-in-Nigeria.pdf .
2. **Food acceptance:** a Nigerian tofu study in Enugu youth and TSP sensory work provide local food-formulation context, but **not sales demand for tofu suya**. Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC6250531/ and https://doi.org/10.1080/23311932.2019.1671749 .
3. **Kafi product feasibility:** Bukar et al. (2019) reported **64% and 70%** overall acceptability for two soy-yoghurt formulations. This is a study result, **not Kafi sales, nationwide preference or safety certification**. Source: https://www.nsmjournal.org.ng/uploads/articles/nutritional_and_sensory_evaluation_of_soy-yoghurt_produced_with__lactobacillus_plantarum_isolated_from_locally_fermented_milk__nono__7.pdf .
4. **Yoghurt competitive structure:** Euromonitor (Oct 2025) reported Nigerian yoghurt and dairy-alternatives demand sensitive to affordability, package sizes and distribution, with small local grocers dominant. Plant-based dairy is niche. This is **category-wide**, not evidence of Kafi demand or specific pack price. Source: https://www.euromonitor.com/dairy-products-and-alternatives-in-nigeria/report .
5. **Correction to supplied research:** contrary to an implication that no Nigerian tofu-suya direct competitor is known, VeggieVictory's Lagos menu **lists Tofu Suya ₦2,500** and Vchunks Suya ₦2,000. Price is a published restaurant *selling* price, **serving weight and actual sales unknown**. Source: https://veggievictory.com/menu/ (checked 16 Nov 2026).
6. **Unknowns:** Kafi's actual formula, starter culture/animal-derived constituents, shelf life, nutritional labelling, and stable cold-chain conditions are not validated. Do not imply vegan status or safety from the term "soy yoghurt."

## Channel and segment research hypotheses
| Product | First customers to interview | Initial outlet types | Key hypothesis to disprove |
|---|---|---|---|
| Tofu suya | Existing suya buyers, campus young adults, vendor owners | Street-food suya vendors, campus/quick-service outlets | Familiar seasoning + acceptable texture can generate paid trial at comparable **per-stick** price |
| Kafi soy yoghurt | Yoghurt buyers, students, households, shopkeepers | Local grocers, kiosks, cafés and campus shops | A feasible soy-yoghurt flavour/pack can be sold within consumers' price ceilings through reliable chilled distribution |

These are **research hypotheses**, not ranked customers or confirmed launch markets.

## AI contribution and baseline
- **Transparent baseline:** 5-factor weighted score, evidence-gated. Report ranked candidates only when dates, sample sizes, prices/pack sizes, channel counts and supplier constraints are known. Check weight sensitivity.
- **AI experiment:** unsupervised **K-means** clusters consented product-specific survey responses on trial/purchase intention, stated willingness to pay and purchase frequency. Minimum 24 **complete, consented** responses per product; three clusters; deterministic random state; show within-sample silhouette. This is **exploratory pattern discovery**, not a claim of predictive demand.
- **No data fabrication:** the uploaded Survey_Responses tab is empty. The app includes a clearly labelled 36-person synthetic test to demonstrate code only; never use these fictitious results in business recommendations.
- **Fair comparisons:** tofu suya against beef suya or snack portions of similar weight; Kafi against same-pack-size dairy yoghurt and direct soy yoghurts where available. Soy milk is **adjacent**, not a confirmed soy-yoghurt competitor. Keep direct/indirect/adjacent categories distinct.
- **Judging claim:** "We built a working segmentation and opportunity-scoring pipeline that abstains with incomplete evidence; it is *not yet* a validated Nigeria market predictor."

## Required fieldwork to make a defensible decision
1. Obtain **dated, consented** product-specific interviews in at least two cities; record actual sample sizes, frequencies, try/buy responses and acceptable price ceilings. Keep anonymous Respondent_ID, no phone or identifiable details in GitHub.
2. Collect **3 price/pack observations** per product/market (beef suya per portion, current yoghurt brands per volume, tofu/soy alternatives). Record store, unit size, date and city.
3. Count accessible food outlets and obtain at least **2 retailer/vendor interviews per pilot market**, including margin, cold holding, ordering terms and current shelf space.
4. Seek **supplier quotes** and measure transport/cold storage constraints and price fluctuations; state soybean/awara difference.
5. Agree a 1–5 scoring rubric for each criterion with at least **two independent reviewers**; store source IDs and reasons, note disagreements.
6. Run both the fixed-weight baseline and AI clustering on **real** consented data and compare whether the clusters add useful targeting insight; report failures honestly.
7. Choose a pilot market only after budget, feasibility and demand evidence is evaluated. Ask food-science and business mentors at the earliest checkpoint.

## Hand-off
- **Ibrahim:** competitor audit, location/channel validation, scoring governance, business decision narrative; coordinate actual merchant quotes and interviews.
- **Muhammad Inuwa:** implement/tests for market pipeline and UI; review the scoring rubric, clustering model and tests.
- **Amina:** validate research citations, prices, questionnaire, soy-yoghurt formulation and packaging/cold-chain questions.
- **Team food specialist/mentor:** texture/fermentation hygiene, labelling, food safety, storage and sensory testing.

## Implementation
- `pages/3_Market_Opportunity.py` — isolated Streamlit Challenge 3 market radar.
- `src/menushift/market3.py` — evidence readiness, 5-factor scoring, weight sensitivity.
- `src/menushift/market_segments.py` — consent-aware clustering experiment.
- `data/challenge3/opportunities.csv` — 48 empty-scoring source rows.
- `data/challenge3/survey_responses.csv` — headers only, no recorded individual responses.
- `tests/test_market3.py` / `tests/test_market_segments.py` / `tests/test_market3_ui.py` — safeguards.
- Updated workbook exported separately for team fieldwork: 48-cell audit, competitor correction and fieldwork planner.

**Release decision:** the code can be reviewed and demonstrated synthetically. No evidence-backed market ranking, public business claim or production sales recommendation is approved. 

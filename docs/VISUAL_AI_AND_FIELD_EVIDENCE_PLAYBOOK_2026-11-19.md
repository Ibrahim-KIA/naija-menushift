# Team Sprout — Evidence Collection & AI Interpretation Handoff
**Hack the Fork Nigeria 2026 · Challenge 2 · 19 November 2026**

## Current status — do not overclaim
- **Implemented in review branch:** bounded Bedrock visual-request interpreter, source-grounded prompt builder, reviewer-only evidence CSV intake, package/chef/sensory/batch validation, and separate reporting of approved measured servings.
- **Not yet performed:** actual AWS Bedrock text model call, real AI image generation (image model not on organiser allowlist), physical package/lot inspection, cooking batches, consented tasting, professional chef interviews, completed human-reviewed serving data.
- Original Amina workbook remains a reference table (https://docs.google.com/spreadsheets/d/1hs6y8OQfaEFRoJvjXuwQ6K42mV8q2csZleoK4KkT5Fo/edit). It supplies market estimates and USDA food references, **not measured finished servings**. Do not automatically promote its pressed/frozen water-loss formulas to verified food composition.

## Advanced natural-language visual requests
The owner writes a free-form request such as:
> “Make this feel like an evening roadside suya stand, viewed from above on a wooden board; keep the food exactly as described.”

The optional Bedrock text interpreter maps language to an allowlisted *style, plating, camera angle, light and setting* JSON object. A local strict parser refuses additional fields, unknown enumerations, illegal ingredients or changes to food. The actual recipe stays the source of truth; e.g. “add beef” raises the recipe-change warning instead of silently adding meat to the image prompt.

The UI always supports offline fallback visual choices. Bedrock interpretation is triggered **only on an explicit click** if configured with `ENABLE_BEDROCK_VISUAL_INTERPRETER=true` and a verified `BEDROCK_TEXT_MODEL_ID` permitted by the organiser. Credentials come from the standard AWS SDK chain; do not insert workshop secrets in code, prompt, GitHub or Figma.

Image-generation action is visible in the recipe panel, but will **refuse to make an AWS image request** unless an image model is specifically allowed by the organiser and all approval gates are set. User approval to add this feature does not modify the AWS account's model allowlist. The 19 Nov official Participant Guide lists Titan Embeddings and Nova text models but not Titan Image Generator, and explicitly excludes Stability AI. Continue asking for a permitted model ID, region, cost/quota and usage terms before enabling live inference. `amazon.nova-canvas` is retired.

## Food labels — exactly what Amina must capture
For each purchased package used in the batch (awara, yaji, seasoning, oil, etc.):
1. Photograph both **ingredient statement** and **allergen / may contain** panel in usable resolution. Review the actual batch/lot number and mass; do not assume a retail website photo matches the purchased package.
2. Record supplier/brand, product, lot code, net mass, ingredient statement and declared allergens. Enter *none* only if the actual package was reviewed and no allergen is declared; blank/unknown is not clearance.
3. Include **soy** on awara/tofu evidence. A suya-style recipe requires reviewed yaji, including **groundnut/peanut where applicable**. Record "may contain" and cross-contact review separately; a food package lacking the warning does not guarantee absence of cross-contact.
4. Review whether packaged seasoning/yaji contains animal-derived constituents. If unclear, do not mark it plant-only.
5. Hash each photo locally with SHA-256 and record the hash/reference in the CSV. The app hashes uploads in memory; it neither runs OCR nor pretends to approve the photo.
6. A named team reviewer checks the exact package evidence, records review date and signs the review. No review status is inferred from AI output.

Reference: NAFDAC prepackaged food labelling guidance (ingredients and allergens, including soy and peanuts): https://www.nafdac.gov.ng/wp-content/uploads/Files/Resources/Guidelines/FOOD/Guidelines-For-Food-Labelling_Labelling.pdf . WHO/FAO precautionary allergen labelling and cross-contact guidance: https://www.who.int/publications/i/item/B09033 .

## Measured batch protocol — minimum practical pilot
For each four preparation methods, under a food specialist's safe process:
- Capture start batch ID, purchased awara grams, weighed seasoning grams, actual market price and purchase date.
- Record pressed/frozen/fried weight changes, finished portion grams, cooking time, consumed fuel/electricity, oil retained (if applicable), paid or estimated actual labour and packaging/waste/other costs **with their measurement basis**.
- Use at least two independent repeats where feasible. More repeats improve the uncertainty estimate; two repeats are not a statistical validation study.
- Record measurement sheets and photo/scale evidence separately using pseudonymous codes; the application does not infer missing values as zero.
- Avoid serving unapproved unlabelled allergen mixtures to people. Follow qualified kitchen/food-safety guidance.

Template: `data/evidence_intake/batches.csv`. A reviewed batch is a *record*, not proof that the recipe is safe or nutritionally matched.

## Sensory trials — actual feedback, never generated by AI
- Recruit willing participants and obtain explicit consent to record anonymous ratings. Do not include names, phone numbers, clinical allergy history, or other personal details in the CSV.
- Food expert confirms safe handling and allergen briefing before tastings.
- Use coded, blinded samples with standard conditions and portion size. Randomise serving order where possible.
- Record 1–9 whole-number hedonic ratings for aroma, flavour, texture, appearance and overall liking. Separately record observed skewer stability: held / partial / crumbled / not tested.
- Capture multiple independent participants; **one score must never be described as consumer acceptance**.
- Reviewer signs only actual obtained, consented records. Test records used in unit tests are synthetic and cannot be imported as real evidence.
- Show mean scores with respondent count and context; no population-wide conclusion without adequate sample design.

Template: `data/evidence_intake/sensory.csv`. Design draws on established hedonic evaluation practices; apply consistent taste panel methods and blind coding appropriate to local food-safety review.

## Chef and restaurant practicality feedback
- Obtain **actual** feedback from a practising chef, food technologist or restaurant owner. Record their role as self-reported; do not claim credential verification unless checked separately.
- Capture rated preparation practicality, skewer workability and customer fit on a 1–5 scale; note constraints and corrections.
- Use pseudonymous reviewer codes and consent. A reviewer signs only the feedback actually received.
- A restaurant owner mentioning a pricing concern is qualitative evidence; it does not validate the numerical price model.

Template: `data/evidence_intake/chef_feedback.csv`.

## Approved serving-level integration
Each approved serving record must reference:
- reviewed purchased awara **and reviewed yaji** label/formulation evidence,
- a reviewed batch with measured purchased and finished mass, full cost components and preparation duration,
- a reviewed consented tasting record linked to the same method and batch,
- a reviewed chef/restaurant-owner feedback record linked to the same method and batch,
- independently sourced protein value with explicit `protein_evidence_type=lab_measured|matched_reference`, food state and source,
- a named human approver, review date and exact ID links.

Only linked `approved` records are surfaced in the app's "Independent serving evidence" section; even there, figures remain visibly separated from the source-based experimental recommendations. `matched_reference` protein stays **estimated**, never disguised as a local lab assay.

Current templates are intentionally header-only. The existing `data/verified/{ingredients,dishes,options,option_items}.csv` remain unchanged and empty; do not falsely claim a completed independently verified dataset.

## Reviewer workspace
`pages/2_Kitchen_Evidence.py` is disabled unless:
- `ENABLE_EVIDENCE_REVIEW_WORKSPACE=true`
- `EVIDENCE_REVIEW_ACCESS_CODE` is a strong secret (min 16 characters) configured *outside Git*.
A reviewer then uploads five local CSVs in memory, audits links and checks panel summaries. No raw label images or sensitive research data are persisted automatically; reviewed CSVs must go through the team's separate approval workflow before being committed.

## Prioritised real-world actions for tomorrow
1. Amina: obtain real ingredient packages and photograph labels, confirm source / lot / soy and peanut content.
2. Food reviewer/chef: approve safe preparation plan, measure 1–2 real batches, capture cooking yield/fuel/oil and revised yaji recipe.
3. Volunteer panel: consent, blind tasting where safe, rate independently; no fabricated review scores.
4. Muhammad: run evidence validation and update the complete linked CSVs in a review PR; do not bypass blank or pending fields.
5. Team: compare measured cost and prep times against experimental engine, rehearse limitations; only then approve promotion of a serving-level dataset.

## Technical and policy documentation
- Amazon Bedrock Converse: https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html
- Amazon Nova Converse examples: https://docs.aws.amazon.com/nova/latest/userguide/using-converse-api.html
- NAFDAC Food labelling: https://www.nafdac.gov.ng/wp-content/uploads/Files/Resources/Guidelines/FOOD/Guidelines-For-Food-Labelling_Labelling.pdf
- WHO cross-contact risk and precautionary labelling: https://www.who.int/publications/i/item/B09033

# Naija MenuShift — Independent price, nutrition, yield and food-safety evidence audit
**19 November 2026 • Research-status report (NOT a validated restaurant dataset)**

## Scope and source
Directly re-opened Amina's original Google Sheet:
https://docs.google.com/spreadsheets/d/1hs6y8OQfaEFRoJvjXuwQ6K42mV8q2csZleoK4KkT5Fo/edit

Two tabs: ten market/processing references and five food-state nutrient rows. The repository stores the original imported content in `data/research/amina_2026-11-13_*.csv`, but the original spreadsheet remains the primary source for the submitted figures.

## Priority corrections and status
| Figure | Research conclusion | System treatment |
|---|---|---|
| Soybeans ₦644/kg | Exchange/commodity benchmark, NOT local purchased tofu. A source quote cannot be converted into a complete wet-awara cost without independently measured yield, coagulant, water, processing and labour | Keep as historical source input in research model, never present as a verified awara retailer quote |
| Boneless beef ₦7,171/kg | May 2026 NBS national raw boneless average (repo's secondary transcription: ₦7,171.41). Not a current Abuja/Zaria price, not cooked suya cost | Beef remains a reference only; raw price and cooked nutrient food states cannot be treated as one measured serving |
| Oil ₦3,264 per 75 cl | NBS-derived 75 cl retail price reference, not ₦/kg | Price by volume; measured *consumed/retained* oil still missing |
| Onions ₦1,164/kg | Workbook April/May note is ambiguous; repo's May secondary transcription is ₦1,180.01 | Preserve original, specify source month, do not invent a current local quote |
| Pepper ₦1,178/kg | Exact pepper type and quote date not established | Source quality insufficient for verified mode |
| Seasoning ₦1,900 per 100 × 4 g cubes | Quoted package math can be evaluated, but ingredient composition/animal derivative/allergen labels not checked | Mark labels unknown and refuse dietary clearance |
| Salt ₦175 per 500 g | Price/unit arithmetic valid, current listing/date and brand need review | Unverified local retail listing |
| Kerosene ₦2,977/L; LPG ₦1,620/kg | Mixing historical reference periods and fuel units; without measured batch consumption neither is a cost per serving | Do not include guessed fuel spend or hide it as zero |
| Local milling ₦150/batch | Informal source with missing date, vendor and actual batch size | Requires independently confirmed local quote |
| Calcium-set firm tofu 17.3 g protein/100 g | USDA FoodData Central SR Legacy 172475 reference, but NOT a direct Nigerian awara assay | Display as source-referenced estimate with explicit food-form uncertainty |
| Pressed tofu 21.6 g/100 g; frozen 23.1 g/100 g | Calculated 17.3/0.8 and 17.3/0.75 using assumed 20%/25% mass loss **with no loss of protein solids**; not measurements | Label as *modelled moisture concentration*, no claim that pressing creates protein |
| Fried tofu 18.8 g/100 g | USDA FDC 172451 generic fried tofu reference, not the team's pressed/fried/grilled output | Do not imply measured oil absorption or pre/post fry yield |
| Cooked lean beef 29.5 g/100 g | USDA cooked food reference, not raw boneless mass used for price | A meaningful raw-to-cooked comparison needs weighed meat yield |

**Consequence:** the current `data/verified/` tables stay incomplete. No web listing or publication eliminates the need for portion and kitchen measurements.

## Additional independent local price leads (not validated supplier quotes)
The structured source log is `data/research/independent_price_leads_2026-11-19.csv`.

- **Abuja fresh beef:** Kubwa aggregator listing ₦8,500/kg, last noted 8 September 2026; Abuja Wholesale Prices online listing ₦8,550/kg (date unspecified). Both require cut verification, store confirmation, and November quote. Sources: https://www.foodstuffmarkets.com/prices and https://abujawholesaleprices.com/wholesale-meat-fish-abuja/
- **Zaria prepared peppered awara:** A & B Square post (1 November 2026) says ₦2,000/pack; **no pack mass**. This is prepared food, not raw tofu per kilogram. Source: https://www.restaurants10.com/NG/Zaria/368295613030485/A-%26-B-Square
- **Lagos fresh tofu:** Supermart listing ₦2,700, **sold out** with no weight stated. Asian Grocery Nigeria tofu ₦4,500, **out of stock**, no weight stated. Neither supports any ₦/kg conversion. Sources: https://www.supermart.ng/products/fresh-tofu and https://www.asiangroceryng.com/shop/tofu
- **Beef national benchmark:** May 2026 NBS Selected Food Price Watch catalogue (official dataset catalogue and secondary price transcription). https://microdata.nigerianstat.gov.ng/index.php/catalog/162/related-materials

**No confirmed, orderable Abuja/Zaria fresh-awara price per kg was obtained from public research on 19 November.** Ask two direct local suppliers for firm-awara price per weighed kilogram and actual availability.

## Food yields, cost and portion methodology
Independent food-science sources show why production parameters cannot simply be assumed:
- 2025/26 open-access soybean-variety/tofu study documents an explicit yield calculation using dry soybean mass, final pressed tofu mass, and processed soymilk batch fraction. This establishes a **measurement protocol**, not this team's yield. https://pmc.ncbi.nlm.nih.gov/articles/PMC13089988/
- Nigerian study of awara coagulants/texture and sensory outcomes shows coagulant composition affects properties, limiting transfer of USDA calcium-set nutrient profiles to local awara. https://pmc.ncbi.nlm.nih.gov/articles/PMC12753399/
- Nigerian comparison of steaming, baking, frying and microwaving tofu finds cooking method influences nutrient concentrations and sensory measures; **does not validate our four suya candidates**. https://www.ajol.info/index.php/njns/article/view/235846
- Field cooking procedures and market recipes are *preparation leads*, not controlled yield or sensory findings. A finished 100g piece should always be tied to purchased grams, measured post-press mass, true retained oil and fuel.

**Measured serving cost formula (to be calculated only after field data exists):**
`(mass purchased × matching price per unit) + coagulant + oil consumed + fuel/energy consumed + labour + packaging + waste/other costs`, divided by **actual saleable servings**.

Three repeated batches per method are suggested for preliminary variability (not a scientifically powered sensory study). Use `data/research/kitchen_batch_measurements_template.csv`, leaving missing measurements blank; never enter fake zeros.

## Suya identity, allergen and safety gap (critical)
Traditional suya's yaji seasoning commonly contains **groundnut / peanut cake (kuli-kuli)** plus spice mixtures, with recipe variation; the current dataset does **not** include a reviewed groundnut/yaji mixture. References:
- Nigerian suya research: https://safer.uct.cl/index.php/SAFER/article/download/369/328/1383
- Food science/technical description with kuli-kuli: https://library.faraafrica.org/storage/2020/10/Book_Animal-Products-Science-Enterprise-Prof-EB-Sonaiya-2020.pdf
- A commercial yaji ingredient disclosure: https://poshyfoods.com/faq/

**Implementation:** Kitchen optimiser now rejects a 'peanut-free suya' outcome because yaji composition is unverified; the UI explains why. Soy is a declared allergen in tofu. Missing seasoning labels are 'unreviewed', not 'safe'.

For any future packaged product, obtain the current NAFDAC labelling requirements and food-safety review. Nigerian regulatory and research references:
- https://www.nafdac.gov.ng/wp-content/uploads/Files/Resources/Guidelines/FOOD/Guidelines-For-Food-Labelling_Labelling.pdf
- https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2025.1644344/full
- Cross-contact technical guidance (US FDA, **not** an assertion of Nigerian law): https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/food-allergies

A labelled allergen-free statement is not sufficient evidence of cross-contact control. Require actual package/photo review and a kitchen process check, including shared equipment. Do not call any generated trial card safe to sell.

## Sensory and kitchen practicality
Published Nigerian studies show that preparation/functional properties influence acceptability, but **we found no independent sensory panel validating these exact tofu-suya formulations**. Record texture, aroma, visual appearance, chew, skewer retention, and consumer acceptance as direct blinded trial results rather than AI-generated claims.
- Nigerian tofu cooking-method study: https://www.ajol.info/index.php/njns/article/view/235846
- Nigerian soy-wara fermentation sensory study: https://www.tandfonline.com/doi/abs/10.1080/15428052.2017.1418692
- `data/research/sensory_review_template.csv` contains headers only; user consent and pseudonymized non-sensitive responses required.

## Release gates for incorporating approved data
1. Confirm fresh awara and local beef purchase prices, exact package weight, market, date and supply type.
2. Complete at least one **independently verified** weighed batch per candidate before promoting serving estimates; follow with repeat batches for range/variability.
3. Verify grain/coagulant conversion, purchased-to-finished yield, oil and processing costs, and nutrient state.
4. Validate recipe ingredients, soy, groundnut/yaji, spice/seasoning labels, and food-handling review.
5. Have food specialist approve source status; do not infer certification from an online paper.
6. Only then populate **all four** `data/verified/*.csv` tables, run numerical-data checks and compare against current synthetic/default and simplest-feasible baselines.
7. Preserve an evidence trail for each imported value, including reviewer, quote date, context and any unresolved uncertainty.

**Conclusion:** Sources are reviewed and local market leads gathered; evidence is not yet sufficient to claim a measured, ready-for-restaurant suya recipe or to replace the existing verified-data gate.

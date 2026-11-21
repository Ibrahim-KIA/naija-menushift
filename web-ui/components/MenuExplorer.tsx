import NutritionPanel from "./NutritionPanel";

export const menuAdaptations = [
  {
    name: "Jollof rice with peppered cowpeas",
    image: "jollof",
    nutrition: ["330 g serving", 410, 9, 1.4, 66, 10, 5, 16, 370],
    protein: "Cowpeas",
    original: "Chicken jollof",
    keep: "Keep the jollof tomato and pepper base.",
    swap: "Serve peppered cowpeas where chicken would sit. Use plant-only stock for the rice.",
    check: "Compare smoked-pepper flavour and how the cowpeas hold through service. Expect a softer bite than chicken.",
    estimate: "12.8 g",
    entry: "03_007",
    ingredients: ["One serving of jollof rice made with plant-only stock", "150 g cooked, drained cowpeas", "15 g sliced onion", "3 g fresh chilli", "1 tsp vegetable oil"],
    method: "Soften the onion and chilli in the oil. Stir in the cooked cowpeas and warm them through under your kitchen’s approved procedure. Spoon alongside the jollof rice.",
    note: "Check jollof stock and seasonings for animal ingredients and verify supplier allergen labels.",
  },
  {
    name: "Bambara groundnut and pepper bowl",
    image: "bambara",
    nutrition: ["215 g serving", 295, 8, 1, 39, 5, 3, 15, 180],
    protein: "Bambara groundnut",
    original: "Beef pepper stew",
    keep: "Keep the tomato, onion and chilli base.",
    swap: "Fold cooked Bambara groundnuts into the pepper base in place of beef pieces.",
    check: "Taste for pepper and tomato balance. Check the bite of the legumes after holding.",
    estimate: "14.7 g",
    entry: "03_012",
    ingredients: ["150 g cooked, drained Bambara groundnuts", "25 g chopped tomato", "15 g sliced onion", "3 g fresh chilli", "1 tsp vegetable oil"],
    method: "Soften the onion, tomato and chilli in the oil. Fold in the cooked Bambara groundnuts and warm them through under your kitchen’s approved procedure.",
    note: "Verify legume allergy and cross-contact requirements with your kitchen before service.",
  },
  {
    name: "Egusi soup with cowpeas",
    image: "egusi",
    nutrition: ["300 g serving", 430, 24, 5, 37, 9, 4, 18, 450],
    protein: "Cowpeas",
    original: "Egusi soup with meat or fish",
    keep: "Keep the ground melon seeds, leafy greens and pepper base.",
    swap: "Use cooked cowpeas for the bite-size pieces. Use plant-only stock and leave out ground crayfish.",
    check: "Compare broth depth, thickness and how the cowpeas hold together in the soup.",
    estimate: "12.8 g",
    entry: "03_007",
    ingredients: ["One tested portion of plant-only egusi soup base", "150 g cooked, drained cowpeas"],
    method: "Prepare the egusi base separately. Fold the cooked cowpeas in near the end and heat using your kitchen’s approved procedure. Serve with your usual accompaniment.",
    note: "Confirm all ingredients in the soup base. The cowpea value excludes the egusi soup and any swallow.",
  },
  {
    name: "Pepper and onion moi moi",
    image: "moimoi",
    nutrition: ["160 g serving", 220, 8, 1.3, 25, 5, 3, 11, 250],
    protein: "Cowpeas",
    original: "Moi moi with fish or egg",
    keep: "Keep the smooth steamed cowpea batter and the pepper and onion base.",
    swap: "Use diced red pepper in place of the fish or egg filling. Use water or plant-only stock in the batter.",
    check: "Compare the steamed set, moisture and savoury flavour. Check the portion after holding.",
    estimate: "",
    entry: "",
    ingredients: ["One portion of your kitchen’s peeled cowpea batter", "20 g diced red pepper", "Plain salt or reviewed plant-only seasoning"],
    method: "Mix the diced red pepper into the batter. Portion and steam using your kitchen’s approved moi moi procedure. Record the cooked weight and check the set before service.",
    note: "Protein needs the weighed batter recipe and finished yield. Confirm every batter ingredient and supplier label before service.",
  },
  {
    name: "Mild onion cowpea bowl",
    image: "jollof",
    nutrition: ["180 g serving", 220, 5, 0.8, 32, 4, 3, 13, 35],
    protein: "Special dietary trial · chilli omitted",
    original: "Peppered cowpeas",
    keep: "Keep cooked cowpeas and the softened onion base.",
    swap: "Leave out chilli and mixed seasonings for a mild version.",
    check: "Review the recipe against the diner’s documented dietary requirements.",
    estimate: "12.8 g",
    entry: "03_007",
    ingredients: ["150 g cooked, drained unsalted cowpeas", "20 g diced onion", "1 tsp plain vegetable oil", "Water as needed"],
    method: "Soften the onion in the oil. Add the cooked cowpeas and a splash of water. Warm through using your kitchen’s approved procedure.",
    note: "Example for dietary review. Clinical suitability and cross-contact require qualified review.",
  },
  {
    name: "Bambara tomato bowl · no salt added",
    image: "bambara",
    nutrition: ["205 g serving", 295, 8, 1.1, 39, 5, 3, 15, 25],
    protein: "Special dietary trial · sodium review",
    original: "Bambara groundnut and pepper bowl",
    keep: "Keep cooked Bambara groundnuts, tomato and onion.",
    swap: "Prepare without added salt, stock cubes or commercial sauces.",
    check: "Review measured sodium against the facility’s spec. Supplier ingredients can contribute sodium.",
    estimate: "14.7 g",
    entry: "03_012",
    ingredients: ["150 g cooked, drained unsalted Bambara groundnuts", "30 g chopped tomato", "15 g diced onion", "1 tsp vegetable oil"],
    method: "Soften tomato and onion in the oil. Add the cooked groundnuts and warm through using your kitchen’s approved procedure.",
    note: "Example for sodium review. The synthetic panel does not establish a low-sodium or therapeutic claim.",
  },
] as const;

export type MenuAdaptation = (typeof menuAdaptations)[number];

export function MenuAdaptationCard({ menu, expanded = false }: { menu: MenuAdaptation; expanded?: boolean }) {
  return (
    <article className="studio-plate">
      <p className="studio-tag">{menu.protein}</p>
      <h3 className="ns-menu-name">{menu.name}</h3>
      <p className="ns-note">Adapted from {menu.original}</p>
      <p><strong>Keep.</strong> {menu.keep}</p>
      <p><strong>Swap.</strong> {menu.swap}</p>
      {menu.estimate && <p><strong>{menu.estimate}</strong> estimated protein from 150 g cooked legumes</p>}
      <details className="studio-disclosure" open={expanded || undefined}>
        <summary>Open recipe</summary>
        {expanded && <figure className="menu-concept"><img src={`/menu-${menu.image}.webp`} alt="" /><figcaption>AI-generated concept for this dish family</figcaption></figure>}
        <h4>Ingredients for one trial portion</h4>
        <ul>{menu.ingredients.map((ingredient) => <li key={ingredient}>{ingredient}</li>)}</ul>
        <h4>Method</h4>
        <p>{menu.method}</p>
        <p><strong>Check in a tasting.</strong> {menu.check}</p>
        <p className="ns-note">{menu.note}</p>
        <NutritionPanel demo={menu.nutrition} />
        {menu.entry && <p className="ns-note">Composition source. <a href="https://www.fao.org/infoods/infoods/tables-and-databases/faoinfoods-databases/en">FAO/INFOODS WAFCT 2019, {menu.entry}</a></p>}
      </details>
    </article>
  );
}

export default function MenuExplorer() {
  return (
    <section className="ns-explorer ns-menu-library" id="menu-library" aria-labelledby="explorer-heading">
      <h2 id="explorer-heading" className="ns-panel-title">More plant-based menu options</h2>
      <p className="ns-note ns-explorer-note">
        Start with a dish you already cook. See what to keep, what to swap, and what to taste-test. Where shown, protein covers the cooked legume portion. Recipe costing and constraint checks are pending.
      </p>
      <div className="studio-option-grid studio-option-grid--two">
        {menuAdaptations.map((menu) => (
          <MenuAdaptationCard key={menu.name} menu={menu} />
        ))}
      </div>
    </section>
  );
}

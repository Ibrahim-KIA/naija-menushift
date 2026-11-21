export const menuAdaptations = [
  {
    name: "Jollof rice with peppered cowpeas",
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
        <h4>Ingredients for one trial portion</h4>
        <ul>{menu.ingredients.map((ingredient) => <li key={ingredient}>{ingredient}</li>)}</ul>
        <h4>Method</h4>
        <p>{menu.method}</p>
        <p><strong>Check in a tasting.</strong> {menu.check}</p>
        <p className="ns-note">{menu.note}</p>
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

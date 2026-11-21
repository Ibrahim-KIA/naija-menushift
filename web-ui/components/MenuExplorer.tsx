const menus = [
  {
    name: "Jollof rice with peppered cowpeas",
    protein: "Cowpeas",
    estimate: "12.8 g",
    entry: "03_007",
    ingredients: ["One serving of jollof rice made with plant-only stock", "150 g cooked, drained cowpeas", "15 g sliced onion", "3 g fresh chilli", "1 tsp vegetable oil"],
    method: "Soften the onion and chilli in the oil. Stir in the cooked cowpeas and warm them through under your kitchen’s approved procedure. Spoon alongside the jollof rice.",
    note: "Check jollof stock and seasonings for animal ingredients and verify supplier allergen labels.",
  },
  {
    name: "Bambara groundnut and pepper bowl",
    protein: "Bambara groundnut",
    estimate: "14.7 g",
    entry: "03_012",
    ingredients: ["150 g cooked, drained Bambara groundnuts", "25 g chopped tomato", "15 g sliced onion", "3 g fresh chilli", "1 tsp vegetable oil"],
    method: "Soften the onion, tomato and chilli in the oil. Fold in the cooked Bambara groundnuts and warm them through under your kitchen’s approved procedure.",
    note: "Verify legume allergy and cross-contact requirements with your kitchen before service.",
  },
] as const;

export default function MenuExplorer() {
  return (
    <section className="ns-explorer ns-menu-library" id="menu-library" aria-labelledby="explorer-heading">
      <h2 id="explorer-heading" className="ns-panel-title">More plant-based menu options</h2>
      <p className="ns-note ns-explorer-note">
        Open a recipe to plan a kitchen trial. Protein estimates cover the cooked legume portion only. These recipes have no scored constraints or full-meal costing yet.
      </p>
      <div className="studio-option-grid studio-option-grid--two">
        {menus.map((menu) => (
          <article key={menu.name} className="studio-plate">
            <p className="studio-tag">{menu.protein}</p>
            <h3 className="ns-menu-name">{menu.name}</h3>
            <p><strong>{menu.estimate}</strong> estimated protein from 150 g cooked legumes</p>
            <details className="studio-disclosure">
              <summary>Open recipe</summary>
              <h4>Ingredients for one trial portion</h4>
              <ul>{menu.ingredients.map((ingredient) => <li key={ingredient}>{ingredient}</li>)}</ul>
              <h4>Method</h4>
              <p>{menu.method}</p>
              <p className="ns-note">{menu.note}</p>
              <p className="ns-note">Composition source. <a href="https://www.fao.org/infoods/infoods/tables-and-databases/faoinfoods-databases/en">FAO/INFOODS WAFCT 2019, {menu.entry}</a></p>
            </details>
          </article>
        ))}
      </div>
    </section>
  );
}

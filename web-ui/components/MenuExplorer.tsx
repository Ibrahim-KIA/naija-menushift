import { MENU_EXPLORER_ITEMS } from "@/lib/data";

/**
 * Plant-based menu explorer — illustrative product-vision section inspired by
 * the real menu of Veggie Victory, Lagos (Nigeria's first vegan restaurant).
 * These items are NOT engine outputs and carry no costed formulation.
 */
export default function MenuExplorer() {
  return (
    <section className="ns-explorer ns-menu-library" aria-labelledby="explorer-heading">
      <h2 id="explorer-heading" className="ns-panel-title">
        Dishes awaiting research data
      </h2>
      <p className="ns-note ns-explorer-note">
        The interactive studio covers suya. These dishes need preparation and cost records before we can compare options.
      </p>
      <div className="ns-menu-grid">
        {MENU_EXPLORER_ITEMS.map((item) => (
          <article key={item.name} className="ns-menu-card">
            <p className="ns-card-kicker">{item.style}</p>
            <h3 className="ns-menu-name">{item.name}</h3>
            <p>{item.description}</p>
            <p className="ns-chip">Protein base: {item.proteinBase}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

import Studio from "@/components/Studio";
import MenuExplorer from "@/components/MenuExplorer";

export default function HomePage() {
  return (
    <div className="ns-shell">
      <header className="ns-header">
        <p className="ns-wordmark">Naija MenuShift</p>
        <p className="ns-header-sub">
          A Taste of Nigeria · Hack the Fork Nigeria 2026 · Challenge 2
        </p>
        <p><a href="https://naija-menushift.streamlit.app/" rel="noopener noreferrer">Open the complete Streamlit research application</a></p>
      </header>

      <section className="ns-hero">
        <h1>Add plant-based choices to the Nigerian menu you already serve.</h1>
        <p className="ns-hero-purpose">
          Compare preparations for a familiar dish using your budget, equipment and
          ingredient restrictions. Pick a promising option to test in your kitchen.
        </p>
        <p><strong><a href="#menu-studio">Try the suya example</a></strong> · <a href="#institutional-planning">Plan for an institutional kitchen</a></p>
        <div className="ns-warning" role="note">
          <strong>Research warning:</strong> this is a separate suya-focused synthetic demonstration, not the complete Python-backed multi-dish research application. Prices and
          nutrients are illustrative estimates from reference data, not verified market
          measurements, and no output is approved for food service. Unreviewed data is
          labelled at the point of decision.
        </div>
      </section>

      <main id="menu-studio">
        <Studio />
        <section className="ns-hero" id="institutional-planning" aria-labelledby="institutional-title">
          <h2 id="institutional-title">From a suya trial to a full menu</h2>
          <p><strong>Hospital catering.</strong> Start with a general catering menu and have the kitchen and a qualified dietitian review any proposed changes before service.</p>
          <p><strong>School feeding.</strong> Check supplier capacity, service scale, student acceptance and applicable meal standards with the programme operator and nutrition team.</p>
          <details>
            <summary>See a complete-meal planning example</summary>
            <h3>Eba, egusi soup and an accompaniment</h3>
            <p>Compare a beef plate with a plant-based version using awara and a verified plant-based soup base. Confirm the stock, seasonings and every supplier ingredient before classifying the plate.</p>
            <p>Whole-plate estimates are unavailable. We need recipe weights, cooked yields, portion sizes, matched nutrient records and current supplier quotes for both versions. Awara adds soy, and seasonings or shared equipment may introduce other allergens.</p>
            <p>For a kitchen trial, record cooked yield, moisture and texture after holding, labour time, and cost per served portion. Record binding and emulsion stability where they affect the dish.</p>
          </details>
        </section>
        <MenuExplorer />
      </main>

      <footer className="ns-footer">
        <p>
          Naija MenuShift — a bounded, explainable decision tool. A model may propose;
          only the deterministic constraint engine decides. Beef appears as a comparison
          reference only and is never recommended.
        </p>
      </footer>
    </div>
  );
}


import Studio from "@/components/Studio";
import MenuExplorer from "@/components/MenuExplorer";
import ServingScenario from "@/components/ServingScenario";

export default function HomePage() {
  return (
    <div className="ns-shell">
      <a className="ns-skip" href="#menu-studio">Skip to studio</a>
      <header className="ns-header">
        <a className="ns-wordmark" href="#home"><span aria-hidden="true">✳</span> Naija MenuShift</a>
        <nav aria-label="Main navigation">
          <a href="#menu-studio">Studio</a>
          <a href="#institutional-planning">For institutions</a>
        </nav>
      </header>
      <section className="ns-hero ns-landing" id="home" aria-labelledby="hero-title">
        <div className="ns-hero-copy">
          <p className="ns-eyebrow">A TASTE OF NIGERIA</p>
          <h1 id="hero-title">Plant-based ideas for Nigerian kitchens.</h1>
          <p className="ns-hero-purpose">Start with suya. Set your kitchen limits, compare awara preparations with the original and take the strongest option into a trial.</p>
          <a className="ns-cta" href="#menu-studio">Start the guided suya example <span aria-hidden="true">↗</span></a>
        </div>
        <figure className="ns-hero-photo">
          {/* The licensed photo depicts the conventional dish. */}
          <img src="/suya.jpg" alt="Traditional suya on skewers in Kaduna, Nigeria" width="1080" height="1080" fetchPriority="high" />
          <figcaption><strong>Traditional suya</strong><a href="https://commons.wikimedia.org/wiki/File:Suya_in_skewers.jpg">Halima Waziri</a> · <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a> · Cropped</figcaption>
        </figure>
      </section>
      <main>
        <section className="ns-studio-section" id="menu-studio" aria-labelledby="studio-title" tabIndex={-1}>
          <div className="ns-section-intro">
            <div><h2 id="studio-title">Menu studio</h2><p>Explore a catering, hospital or school feeding example.</p></div>
            <details className="ns-evidence"><summary>About the estimates</summary><p>Prices and yields are demonstration inputs. Nutrients use ingredient references. Confirm supplier labels, cross-contact and actual batch yields before service.</p></details>
          </div>
          <Studio />
        </section>
        <section className="ns-institutional" id="institutional-planning" aria-labelledby="institutional-title">
          <div className="ns-section-intro"><div><h2 id="institutional-title">Plan for an institutional kitchen</h2><p>Move from an ingredient shortlist to a trial your team can measure.</p></div></div>
          <div className="ns-use-cases">
            <article><h3>Hospital catering</h3><p>Start with a general catering menu. Record cost per served portion, batch yield and allergens. Have a qualified dietitian review any therapeutic use.</p></article>
            <article><h3>School feeding</h3><p>Check supplier capacity, portions, service scale and student acceptance against the programme’s standards with its nutrition team.</p></article>
          </div>
          <details className="ns-plate-plan">
            <summary>What an eba and egusi comparison would require</summary>
            <div className="ns-use-cases">
              <article><h3>Original plate</h3><p>Eba, egusi soup and beef. Record the beef cut, cooked serving weight and every stock and seasoning ingredient.</p></article>
              <article><h3>Proposed plate</h3><p>Eba, egusi soup with a verified plant-based stock, and awara. Confirm soy and other allergens, supplier specifications and texture after holding.</p></article>
            </div>
            <p>Complete-meal totals need weighed recipes, cooked yields, matched food composition and local quotes. Compare batch costs, moisture retention, cooking time and texture before serving.</p>
          </details>
          <ServingScenario />
        </section>
        <MenuExplorer />
      </main>
      <footer className="ns-footer"><strong>Naija MenuShift</strong><p>Kitchen planning and research</p></footer>
    </div>
  );
}

import type { Candidate } from "@/lib/engine";
import { TRIAL_STEPS } from "@/lib/data";
import { money } from "./CandidateDetail";

export default function RecipeBook({ candidate, rice, dietaryReview }: {
  candidate: Candidate;
  rice: boolean;
  dietaryReview: string;
}) {
  return (
    <article className="recipe-book" aria-labelledby="recipe-title">
      <figure className="recipe-cover">
        <img src="/awara-cover.webp" alt="Concept illustration of spice-coated awara skewers on a ceramic plate" width="1536" height="1024" />
        <figcaption>AI-generated serving concept · shared across awara preparations</figcaption>
      </figure>
      <div className="recipe-body">
        <header className="recipe-title">
          <p>A TASTE OF NIGERIA · KITCHEN TRIAL</p>
          <h4 id="recipe-title">{candidate.method} suya{rice ? " with plain rice" : ""}</h4>
          <p>One modelled portion · Contains soy</p>
        </header>
        <dl className="recipe-facts">
          <div><dt>Suya portion</dt><dd>{candidate.portionG} g</dd></div>
          <div><dt>Estimated protein</dt><dd>{(candidate.proteinG + (rice ? 3.45 : 0)).toFixed(1)} g</dd></div>
          <div><dt>Assumed suya prep</dt><dd>{candidate.prepMinutes} min</dd></div>
          <div><dt>Listed suya cost</dt><dd>{money(candidate.costNgn)}</dd></div>
        </dl>
        {dietaryReview && <p className="recipe-review" role="note"><strong>{dietaryReview}.</strong> This recipe has not been checked against that requirement. Have a qualified reviewer apply your facility’s standards before service.</p>}
        <div className="recipe-columns">
          <section aria-labelledby="ingredients-title">
            <h5 id="ingredients-title">Ingredients</h5>
            <p className="ns-note">Modelled purchase quantities for one serving.</p>
            <ul className="recipe-ingredients">
              {candidate.ingredientLines.map((line) => <li key={line.ingredientId}>
                <span>{line.name}</span><strong>{line.purchaseG} g</strong>
              </li>)}
              {candidate.oilCl > 0 && <li><span>Oil for frying</span><strong>{candidate.oilCl} cl</strong></li>}
              {rice && <li><span>Plain boiled rice</span><strong>150 g cooked</strong></li>}
            </ul>
            <p className="ns-note">Check the actual seasoning and yaji ingredient labels and cross-contact risks. Rice cost and prep are excluded.</p>
          </section>
          <section aria-labelledby="recipe-method-title">
            <h5 id="recipe-method-title">Trial method</h5>
            <ol className="recipe-method">
              {(TRIAL_STEPS[candidate.methodId] ?? []).map((step) => <li key={step}>{step}</li>)}
            </ol>
            <p className="ns-note">Follow your kitchen’s approved cooking and handling procedures. Record measured yield, prep time and finished-portion weight before using this formulation in service.</p>
          </section>
        </div>
      </div>
    </article>
  );
}

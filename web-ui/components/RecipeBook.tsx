import type { Candidate } from "@/lib/engine";
import { money } from "./CandidateDetail";

const preparations: Record<string, string> = {
  awara_firm: "Cut weighed firm awara into even pieces for skewering.",
  awara_pressed: "Press the weighed awara, record the liquid lost, then cut into even pieces.",
  awara_frozen: "Use your approved freeze and thaw procedure, then press and portion the thawed awara.",
  awara_fried: "Portion the awara for pan-frying. Measure the listed oil and record how much the batch uses.",
};

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
            <p className="ns-note">One trial serving. Quantities are editable in your brief.</p>
            <ul className="recipe-ingredients">
              {candidate.ingredientLines.map((line) => <li key={line.ingredientId}>
                <span>{line.name}</span><strong>{line.purchaseG} g</strong>
              </li>)}
              {candidate.oilCl > 0 && <li><span>Oil for frying</span><strong>{candidate.oilCl} cl</strong></li>}
              {rice && <li><span>Plain boiled rice</span><strong>150 g cooked</strong></li>}
            </ul>
            <p className="ns-note">The example uses fresh onion, chilli and plain salt. Use plain ingredients with verified supplier labels. Keep stock, cubes and unreviewed blends out of the trial. {rice && "Rice cost and prep are excluded."}</p>
          </section>
          <section aria-labelledby="recipe-method-title">
            <h5 id="recipe-method-title">Trial method</h5>
            <ol className="recipe-method">
              <li>{preparations[candidate.methodId] ?? "Weigh and portion the awara before the trial."}</li>
              <li>Use the amounts listed. Chop fresh onion and chilli if included. Keep a little onion for serving and season the awara with the remaining listed ingredients.</li>
              <li>{candidate.oilCl > 0 ? "Pan-fry the portion using the listed oil." : "Thread the pieces onto skewers and grill under your kitchen’s approved procedure."} Record the time and finished weight.</li>
              <li>Plate the awara{rice ? " beside the weighed cooked rice" : ""}. Add any reserved onion and record the final serving weight and holding texture.</li>
            </ol>
            <p className="ns-note">Protein is estimated from the awara reference and the rice where selected. The seasoning rows are priced only. Follow your kitchen’s approved cooking and handling procedures. Record measured yield, prep time and finished-portion weight before using this formulation in service.</p>
          </section>
        </div>
      </div>
    </article>
  );
}

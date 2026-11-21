"use client";

import { useRef, useState } from "react";
import KitchenRequirements from "./KitchenRequirements";
import { RecommendationResults } from "./RecommendationResults";
import { DEFAULT_BRIEF, explore, type Brief, type ExploreResult } from "@/lib/engine";

const examples = [
  { id: "caterer", name: "Catering kitchen", description: "Explore a plant-based version of a familiar menu item.", time: 120, servings: 40 },
  { id: "hospital", name: "Hospital catering", description: "Plan a trial for general food service with a 60-minute prep limit.", time: 60, servings: 80 },
  { id: "school", name: "School feeding", description: "Estimate a larger batch with a 90-minute prep limit.", time: 90, servings: 500 },
] as const;

type Example = (typeof examples)[number];
type Run = { result: ExploreResult; brief: Brief; rice: boolean; example: Example; dietaryReview: string };
const stepLabels = ["Choose a meal", "Set requirements", "Read your recipe"] as const;

export default function Studio() {
  const [example, setExample] = useState<Example>(examples[0]);
  const [dietaryReview, setDietaryReview] = useState("");
  const [rice, setRice] = useState(false);
  const [brief, setBrief] = useState<Brief>(DEFAULT_BRIEF);
  const [step, setStep] = useState(0);
  const [run, setRun] = useState<Run | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const heading = useRef<HTMLHeadingElement>(null);
  const inFlight = useRef(false);

  const goTo = (next: number) => {
    setStep(next);
    requestAnimationFrame(() => heading.current?.focus());
  };

  const chooseExample = (next: Example) => {
    setExample(next);
    setBrief((current) => ({ ...current, maxPrepMinutes: next.time }));
    setRun(null);
  };

  const patch = (update: Partial<Brief>) => {
    setBrief((current) => ({ ...current, ...update }));
    setRun(null);
  };

  const submit = async () => {
    if (inFlight.current) return;
    inFlight.current = true;
    setLoading(true);
    setRun(null);
    setError(null);
    goTo(2);
    try {
      const result = await explore(brief);
      setRun({ result, brief, rice, example, dietaryReview: example.id === "hospital" ? dietaryReview : "" });
    } catch (failure) {
      setError(failure instanceof Error ? failure.message : "The request failed. Try again.");
    } finally {
      setLoading(false);
      inFlight.current = false;
    }
  };

  return (
    <div className="studio-workspace">
      <ol className="studio-progress" aria-label="Recommendation steps">
        {stepLabels.map((label, index) => (
          <li key={label} aria-current={step === index ? "step" : undefined}>
            <button disabled={loading || index > step} onClick={() => goTo(index)}>
              <span aria-hidden="true">{index + 1}</span>{label}
            </button>
          </li>
        ))}
      </ol>
      <div className="studio-content">
        <div className="studio-step-header">
          <div>
            <h3 ref={heading} tabIndex={-1}>{stepLabels[step]}</h3>
            <p>{step === 0 ? "Start with suya, the dish supported by this recommendation dataset." : step === 1 ? "Adjust the example to match your kitchen before comparing." : "Review the trade-offs and decide what to test in the kitchen."}</p>
          </div>
          {step > 0 && !loading && <button type="button" className="studio-secondary" onClick={() => goTo(step - 1)}>{step === 2 ? "Edit requirements" : "Back"}</button>}
        </div>
        {step === 0 && (
          <>
            <fieldset className="studio-pick">
              <legend>Meal</legend>
              <div className="studio-option-grid studio-option-grid--two">
                <label className="studio-option">
                  <input type="radio" name="meal" checked={!rice} onChange={() => { setRice(false); setRun(null); }} />
                  <span><strong>Suya</strong><small>Same-portion beef and awara comparison</small></span>
                </label>
                <label className="studio-option">
                  <input type="radio" name="meal" checked={rice} onChange={() => { setRice(true); setRun(null); }} />
                  <span><strong>Suya with plain rice</strong><small>Shared rice side added to the protein comparison</small></span>
                </label>
              </div>
            </fieldset>
            <fieldset className="studio-pick">
              <legend>Kitchen example</legend>
              <div className="studio-option-grid">
                {examples.map((option) => (
                  <label key={option.id} className="studio-option">
                    <input type="radio" name="kitchen" checked={option.id === example.id} onChange={() => chooseExample(option)} />
                    <span><strong>{option.name}</strong><small>{option.description}</small></span>
                  </label>
                ))}
              </div>
            </fieldset>
            <p className="ns-note">Examples supply editable assumptions for the same suya analysis. Use a qualified reviewer for therapeutic diets or school meal standards.</p>
            <button className="studio-primary" onClick={() => goTo(1)}>Set kitchen requirements <span aria-hidden="true">→</span></button>
          </>
        )}
        {step === 1 && (
          <form onSubmit={(event) => { event.preventDefault(); void submit(); }}>
            <p className="studio-scope">{example.name} · {rice ? "Suya with rice" : "Suya"} · Limits apply to the suya portion</p>
            <KitchenRequirements key={example.id} brief={brief} patch={patch} />
            {example.id === "hospital" && (
              <fieldset className="recipe-dietary">
                <legend>Hospital catering · dietary review</legend>
                <label className="ns-field">
                  <span className="ns-label">Meal review requirement</span>
                  <select value={dietaryReview} onChange={(event) => setDietaryReview(event.target.value)}>
                    <option value="">General catering</option>
                    <option value="Sodium review requested">Sodium review requested</option>
                    <option value="Texture review requested">Texture review requested</option>
                    <option value="Dietitian review requested">Dietitian review requested</option>
                  </select>
                </label>
                <p className="ns-note">Use the protein and allergen fields above for kitchen requirements. The review selection stays on this page. Enter no names, patient records or diagnoses. A qualified reviewer must confirm therapeutic meals.</p>
              </fieldset>
            )}
            <div className="studio-actions">
              <button type="submit" className="studio-primary">Find my trial recipe <span aria-hidden="true">→</span></button>
              <button className="studio-secondary" type="button" onClick={() => { setBrief({ ...DEFAULT_BRIEF, maxPrepMinutes: example.time }); setRun(null); }}>Reset requirements</button>
            </div>
          </form>
        )}
        {step === 2 && loading && (
          <div role="status" className="studio-loading">
            <strong>Checking your kitchen requirements…</strong>
            <div className="studio-option-grid" aria-hidden="true"><span /><span /><span /></div>
          </div>
        )}
        {step === 2 && error && (
          <div className="ns-alert ns-alert--error" role="alert">
            <h4>We couldn’t compare options</h4><p>{error}</p>
            <button className="studio-secondary" onClick={() => void submit()}>Try again</button>
          </div>
        )}
        {step === 2 && run && <RecommendationResults result={run.result} brief={run.brief} rice={run.rice} servings={run.example.servings} dietaryReview={run.dietaryReview} />}
      </div>
    </div>
  );
}

export type Nutrition = readonly [string, ...number[]];

const rows = [
  ["Energy", "kcal"], ["Total fat", "g"], ["Saturated fat", "g"], ["Carbohydrate", "g"],
  ["Dietary fibre", "g"], ["Total sugars", "g"], ["Protein", "g"], ["Sodium", "mg"],
] as const;

export default function NutritionPanel({ demo, protein, portion }: { demo?: Nutrition; protein?: number; portion?: string }) {
  return (
    <section className="packet-nutrition" aria-label="Nutrition information">
      <h4>Nutrition information</h4>
      <p>{demo ? `Illustrative label · per ${demo[0]}` : `Estimated · per ${portion}`}</p>
      <dl>{rows.map(([label, unit], index) => {
        const value = demo ? demo[index + 1] : label === "Protein" ? protein?.toFixed(1) : undefined;
        return <div key={label}><dt>{label}</dt><dd>{value === undefined ? "Unavailable" : `${value} ${unit}`}</dd></div>;
      })}</dl>
      <p>{demo ? "Synthetic figures for UI demonstration. Use verified measurements for labelling, dietary decisions or service." : "Protein is estimated from reference composition. Other label values need matched recipe data."}</p>
    </section>
  );
}

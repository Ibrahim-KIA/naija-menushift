export type Nutrition = readonly [string, ...number[]];

const rows = [
  ["Energy", "kcal"], ["Total fat", "g"], ["Saturated fat", "g"], ["Carbohydrate", "g"],
  ["Dietary fibre", "g"], ["Total sugars", "g"], ["Protein", "g"], ["Sodium", "mg"],
] as const;

export default function NutritionPanel({ demo, protein, portion, iron, zinc }: { demo?: Nutrition; protein?: number; portion?: string; iron?: number; zinc?: number }) {
  return (
    <section className="packet-nutrition" aria-label="Nutrition information">
      <h4>Nutrition information</h4>
      <p>{demo ? `Illustrative label · per ${demo[0]}` : `Estimated · per ${portion}`}</p>
      <dl>{(demo ? rows : [["Protein", "g"], ["Iron", "mg"], ["Zinc", "mg"]] as const).map(([label, unit], index) => {
        const value = demo ? demo[index + 1] : (label === "Protein" ? protein : label === "Iron" ? iron : zinc)?.toFixed(label === "Protein" ? 1 : 2);
        if (value === undefined) return null; return <div key={label}><dt>{label}</dt><dd>{value === undefined ? "Unavailable" : `${value} ${unit}`}</dd></div>;
      })}</dl>
      <p>{demo ? "Synthetic figures for UI demonstration. Use verified measurements for labelling, dietary decisions or service." : "Reference-based estimates. Iron and zinc cover the suya component only. Other nutrients need matched recipe data."}</p>
    </section>
  );
}

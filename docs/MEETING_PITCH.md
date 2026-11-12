# Demo and pitch guide (readable talk track)

“Our project, Naija MenuShift, is an evidence-aware decision-support tool for Nigerian restaurants exploring plant-based alternatives to familiar menu items. Suya is our first demonstration, not the only dish the system will support.

We let a restaurant owner choose a dish, set a maximum serving cost and a minimum estimated protein requirement, and compare plausible plant alternatives. For suya, we are starting with four tofu preparation approaches. Beef suya is displayed only as a conventional reference.

The tool calculates purchase and preparation costs, estimates nutrients from supplied sources, excludes options that fail constraints, and explains the remaining recommendations. It also shows the cheapest-only baseline and how rankings respond when ingredient prices rise or fall by 20 percent.

An important distinction: the sample demonstration data are **fictional**. We need dated local prices, real ingredient composition entries and kitchen trials before making customer claims. We also still need to measure whether our NLP/ranking component performs better than simpler baselines. Our goal is an honest, testable recommendation method that can later cover additional Nigerian dishes.”

## Suggested live click-through

1. Open Streamlit in Synthetic demonstration mode; read the warning aloud.
2. Choose suya, show all four plant options and the beef reference.
3. Tighten budget/protein requirement until the app shows *no feasible option*.
4. Relax requirements and demonstrate ranking and explanations.
5. Change preference or apply +20% price shock; inspect differences.
6. Explain source-data limitations and the planned transition to verified numbers.

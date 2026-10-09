# Guide for content development — GIANT "Data Analysis in STEM"

This is the practical guide for whoever fleshes out and refines the module's lesson
content day to day (currently: the JIMES internship, supervised by Fabian Schemann).
It assumes you've read `README.md` first and can already preview the site locally.

## What already exists, and what's a first draft

| File | Status |
|---|---|
| `index.qmd` (overview page) | Based closely on the project's existing `Layer_1.docx` text. Treat as close to final; check with Fabian before restructuring it. Note: "Layer 1/Layer 2" was internal-only planning language and has been removed from all user-facing text — don't reintroduce it. |
| `01-understanding-data.qmd` | **Rewritten twice**: first onto the real DWD dataset, then restructured again to follow the intern team's original `COURSE_OUTLINE.docx` outline and analogies closely (data types → tidy data/type/range/duplicate checks → missing values with three named strategies A/B/C → data management), rather than an earlier, AI-added "five-checks/data-audit" framing that is no longer used. Adapted into the shared design system (box classes, non-executable code, chapter numbering) — see `data/README.md` for the dataset. Uses 34 years (1991–2024) of real DWD data for five German regions so Chapters 2–4 can teach period-over-period comparison; all counts/figures in this chapter reflect that. The dataset is **real, open DWD data (CC BY 4.0)** with a small number of disclosed, deliberately reintroduced formatting issues (unit-suffix strings, duplicate rows, blanked values) layered on top for the quality-check exercises — see the "full disclosure" section of `data/README.md` before changing anything here. |
| `02-exploring-visualizing.qmd` | **Rewritten** onto the DWD dataset, then simplified to follow **annual mean temperature as the one variable tracked all the way through** the chapter (per Fabian's request to reduce the number of variables/regions shown at once); precipitation now makes one short, explicitly-labelled supporting appearance for outlier detection. The main trend figure now shows the national average alone (`fig-temp-trend-national.png`); the full five-region breakdown (`fig-temp-trend-by-region.png`) moved into the chapter's `.deeper` differentiation box rather than being the primary figure. Exercise 2.5 explicitly compares the early decade (1991–2000) against the recent decade (2015–2024) — this sets up Chapter 3's hypothesis test. All figures regenerated from, and captions/exercise text double-checked against, the real 34-year data (an earlier version of this chapter had a factually wrong outlier claim — see `data/README.md`'s "Two real signals" section for the corrected, verified numbers before writing new claims here). Every `dplyr`/`ggplot2` pipeline now has inline `#` comments explaining each step, `%>%` is explicitly explained on first use (conveyor-belt analogy), and skewness/IQR/`coord_flip()`/`alpha` all get a plain-language explanation or analogy — per the intern team's newbie-accessibility feedback (see the same note on Chapters 3–4). |
| `03-statistical-inference.qmd` | **Rewritten** onto the DWD dataset: bootstrap CI on 2015–2024 temperature (n = 50, 5 regions × 10 years), hypothesis test comparing 1991–2000 vs. 2015–2024 temperature (real numbers: diff ≈ +1.18 °C, p < 0.001, Cohen's d ≈ 1.45 — a large effect that agrees with significance *and* with corroborating trends in precipitation/sunshine, used deliberately as a teaching contrast to the more common "significant but small" case). Already single-variable (temperature) throughout — no restructuring needed for that. The `infer` pipelines (`specify()`/`generate()`/`calculate()`/`hypothesize()`) now have a line-by-line inline comment each, plus a card-shuffling analogy for the permutation test and a Cohen's-d small/medium/large calibration note — same newbie-accessibility pass as Chapters 2 and 4. |
| `04-statistical-modelling.qmd` | **Rewritten** onto the DWD dataset: simple regression `Temperature_C ~ Sunshine_hours` (slope ≈ +0.0015, R² ≈ 0.08 — real but weak), then a multiple regression adding `Year` and `Region`. The real result is a clean "the extra complexity clearly *does* earn its place" finding (adjusted R² jumps from ≈0.07 to ≈0.57, `anova()` p < 0.001). Temperature stays the one response variable throughout; `Sunshine_hours`/`Year`/`Region` are explicitly framed as predictors of it, not co-equal variables. `lm()` is spelled out ("linear model") on first use, dummy variables get an on/off-switch analogy, homoscedasticity gets a "megaphone" visual analogy, and `plot(model, which = )` is explained — same newbie-accessibility pass as Chapters 2 and 3. |
| `05-reproducible-research.qmd` | **New**, no earlier source document. Deliberately links out to r4ds/Happy Git rather than re-explaining Git from scratch — expand the guided tasks if students need more scaffolding. |
| `06-ai-assisted-learning.qmd` | **New**, built from the GIANT project description's language on Socratic dialogue / computational offloading / prompt literacy. Review against however Acemate actually behaves once it exists — the "what Acemate will/won't do" framing should match the real tool. |
| `07-sustainability-problem-solving.qmd` | **New**, built around a worked example that now tracks the DWD dataset ("are the monitored weather stations showing signs of a shifting climate?") plus the renewable-energy/emissions example from the project's own rubric-proposal document. Swap in different worked examples if you prefer. Now opens with a theoretical-grounding section ("Why 'Global' Matters") drawing on Mezirow's transformative learning and Rieckmann's emancipatory Global Citizenship Education, kept deliberately free of GIANT-specific branding so the module stays usable outside GIANT, plus a `.reflection-box` self-check against Goodale et al.'s (2024) six GCE competencies near the end of the chapter. This is the module's main home for the GCED/transformative-learning dimension Fabian asked to be built out — see the sources-box at the end of the chapter for full citations. |
| `08-scientific-communication.qmd` | **New**. The dashboard section now requires `shinydashboard` specifically (per explicit sponsor feedback), with a defined list of required elements (linked panels, an input control, labels, an uncertainty indicator, a key-finding caption, a short qualitative reflection panel tying the finding to who it affects and what perspective might be missing, deployability). The `app.R` skeleton is untested demonstration code — run it before publishing and fix anything that doesn't render against your actual Shiny/R versions. |
| `resources.qmd` | Consolidates links from `Useful Links.docx`, `Ressources Bogner.docx` and `Resources Navigation.xlsx`. Add new links here as you find them, organised by competency area. |
| `data/` | Real DWD (Deutscher Wetterdienst) practice dataset, CC BY 4.0 — see `data/README.md` for the exact source URLs, licence, and full disclosure of what was synthetically added for teaching purposes. Safe to extend (e.g. swap in a real Eurostat challenge dataset for a student's own project) once you have one ready; keep the same column-naming style if you do. |

**Bottom line:** chapters 1–3 carry real institutional content and should mostly need
polish, not rewriting. Chapters 4–8 are genuinely first drafts — useful scaffolding and
a consistent voice to match, but expect to rewrite substantial portions once you've
worked through the source OERs yourself.

## The design system (use it consistently — this is what "one module" instead of "eight documents" depends on)

Defined once in `styles.css`, used the same way in every chapter:

- `::: {.guiding-question}` — the one question the lesson answers, right under the title.
- `::: {.exercise-box}` — a hands-on task with runnable code and 1–3 questions.
- `::: {.expected-output}` — nest inside an exercise box when there's a concrete result
  to check against (a number range, a specific finding). Skip it for open-ended tasks.
- `::: {.acemate-box}` — a specific, checkable nudge about AI use. The box's icon label
  ("🤖 Ask your learning buddy") is deliberately AI-tool-agnostic — write the content
  as "ask your learning buddy to …", not "ask Acemate to …", so the module still reads
  correctly for a student using a different AI tool if Acemate access ever lapses. Don't
  add one to every lesson "just because" — only where there's a genuine tension worth
  flagging (see the existing chapters for the bar to clear).
- `::: {.differentiation-box}` — every chapter has exactly one, containing a nested
  `::: {.struggling}` (a beginner-level resource, e.g. an intro-to-R book) and a nested
  `::: {.deeper}` (an advanced resource, e.g. a data-science-in-R book). Placed at a
  natural difficulty jump in the chapter, not necessarily at the end.
- `::: {.reflection-box}` — a prompt for personal or positional reflection (not a
  technical task): noticing your own frame of reference, whose perspective a dataset
  represents, who is affected by a finding. Currently used in Chapter 7, grounded in the
  transformative-learning and Global Citizenship Education literature (see Chapter 7's
  sources-box). Use sparingly — most chapters don't need one; it exists specifically for
  the GCED/stewardship dimension of the module, not as a general "food for thought" box.
- `::: {.sources-box}` — every chapter has exactly one, right before "Check your
  understanding", listing the 3–5 open resources the lesson actually drew on with a
  link to the matching section of `resources.qmd`. If you add or remove a source a
  lesson draws on, update both places.
- Quarto's own `::: {.callout-note}`, `.callout-tip`, `.callout-important`,
  `.callout-warning` — for anything that isn't an exercise or a learning-buddy note.

Copy `_template-lesson.qmd` as the starting point for any new lesson — it has the full
pattern with inline instructions. It is intentionally **not** listed in `_quarto.yml`'s
`chapters:`, so it never appears in the published site; only files you explicitly add
to that list show up in the sidebar.

## Content rules

1. **Use the shared practice dataset** (`data/clean/dwd_climate_clean.csv`, or the
   raw version only in Chapter 1) unless you have a specific reason to introduce a new
   one — consistency across chapters is what lets a student carry intuition forward.
2. **One analogy per concept**, plain language, no unexplained jargon on first use.
3. **Every exercise ends in a question that asks for interpretation**, not just a
   number — "what does this mean" rather than "what did you get".
4. **Cite the open resource you drew on** in the lesson's opening line and/or in
   `resources.qmd` — this module's whole premise (per the project description) is
   bringing existing OERs together, not reinventing them.
5. **Match the existing tone**: direct, concrete, environmental-science examples
   throughout, never abstract "variable X and Y" filler when a climate-data example is
   available.
6. **Figures live in `images/`**, generated from the real practice dataset (see
   `images/` for the current set — temperature distribution, temperature outliers by
   region, precipitation-by-region boxplot, temperature trend (national, primary) and by
   region (differentiation box), decade comparison, temperature-vs-sunshine scatter,
   bootstrap CI, missing-values heatmap). Regenerate scripts live in the scratchpad used
   for this module's development; regenerate figures if the dataset changes, and keep
   the same muted teal/orange colour scheme and the source/caption line under each
   figure so new ones look like they belong. Before writing a new caption or exercise
   question that makes a factual claim about the data (which year is an outlier, which
   direction a trend moves), **recompute it** rather than assuming — this module has
   already had one figure/caption mismatch slip through undetected.

## Workflow

- Work in a feature branch, one lesson (or one clearly-scoped change) per branch/PR —
  not one giant commit at the end (this is also literally the lesson taught in
  Chapter 5, so it's worth practicing what the module preaches).
- Preview locally before pushing: `quarto preview` (see `README.md`).
- Open a pull request even if you're the only one reviewing it yet — it gives Fabian a
  clean diff to check rather than a wall of changed files.

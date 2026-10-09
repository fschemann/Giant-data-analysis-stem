# Teaching dataset: German regional climate data (DWD, 1991–2024)

This is the running example used across Chapters 1 through 4 (and referenced again in
Chapters 6–8). Unlike the earlier versions of this dataset, it is **real, official
government data** — not simulated.

## Source and license

**Source:** Deutscher Wetterdienst (DWD), Climate Data Center (CDC), "regional
averages" annual series. Three variables, each its own file on DWD's open data server:

- Air temperature (mean): [`regional_averages_tm_year.txt`](https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/annual/air_temperature_mean/regional_averages_tm_year.txt)
- Precipitation (total): [`regional_averages_rr_year.txt`](https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/annual/precipitation/regional_averages_rr_year.txt)
- Sunshine duration: [`regional_averages_sd_year.txt`](https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/annual/sunshine_duration/regional_averages_sd_year.txt)

Each file covers 1881 (or later, depending on variable) through the most recently
completed year, as an area-weighted average per German Bundesland plus a national
("Deutschland") average. Full methodology: DWD's own dataset description,
[`DESCRIPTION_regional_averages_DE_annual_air_temperature_mean_en.pdf`](https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/annual/air_temperature_mean/DESCRIPTION_regional_averages_DE_annual_air_temperature_mean_en.pdf).

**License:** **CC BY 4.0**, stated explicitly by DWD in
[`Terms_of_use.pdf`](https://opendata.dwd.de/climate_environment/CDC/Terms_of_use.pdf)
("The Creative Commons BY 4.0 — Licence 'CC BY 4.0' apply."). Attribution used
throughout this module: *"Deutscher Wetterdienst (DWD), Climate Data Center, regional
climate averages, retrieved 24 September 2026, CC BY 4.0."*

**How the values were obtained:** every number in `data/clean/dwd_climate_clean.csv`
was read directly from the three DWD source files above, for five Bundesländer —
Bayern, Sachsen, Nordrhein-Westfalen, Schleswig-Holstein, Baden-Württemberg — plus the
national "Deutschland" series, for 1991–2024. Each value was cross-checked against a
second, independent read of the same source files (exact match), and a sample of
national temperature values was additionally cross-checked against the German Wikipedia
article ["Zeitreihe der Lufttemperatur in
Deutschland"](https://de.wikipedia.org/wiki/Zeitreihe_der_Lufttemperatur_in_Deutschland)
(exact match on every year checked). The exact retrieval script, with every value
inline and the source URLs in its docstring, is [`generate_climate_dataset.py`](generate_climate_dataset.py)
— run it yourself to regenerate the CSVs from the same hard-coded, source-verified
numbers.

## Why five Bundesländer (not all sixteen)

Bayern, Sachsen, Nordrhein-Westfalen, Schleswig-Holstein and Baden-Württemberg were
chosen because each has been a single, consistently-defined DWD reporting region for
the whole 1991–2024 period, and together they give a good south/east/west/north/southwest
spread across Germany. Some other DWD columns changed definition over the dataset's
full 1881–present history (e.g. Berlin was reported jointly with Brandenburg, and
Hamburg/Bremen jointly with Niedersachsen, in earlier decades) — a genuine real-world
metadata detail, not a data-quality problem, and one Chapter 1 asks you to notice by
reading the DWD documentation rather than guessing. "Deutschland" is kept as a separate
national reference series, not a sixth comparison region, since it is an aggregate of
all sixteen states rather than an independent observation.

## Files

| File | Used from | Description |
|---|---|---|
| `raw/dwd_climate_raw.csv` | Chapter 1 | The real values above, with a small set of **deliberately introduced, fully disclosed** formatting issues (see below) for the data-cleaning exercise. |
| `clean/dwd_climate_clean.csv` | Chapter 2 onward | The real values, unaltered, tidy. |

## Columns

| Column | Type | Description |
|---|---|---|
| `Region` | character | Bundesland name, or `Deutschland` for the national average |
| `Region_Code` | character | Short code: `R01`–`R05` for the five states, `DE` for the national series |
| `Year` | numeric | 1991–2024 |
| `Temperature_C` | numeric | Annual mean air temperature, °C |
| `Precipitation_mm` | numeric | Annual total precipitation, mm |
| `Sunshine_hours` | numeric | Annual total sunshine duration, hours |

## What is real, and what was deliberately added (full disclosure)

**Every number is real DWD data.** Nothing was invented, scaled, or adjusted. The only
changes between `raw/` and `clean/` are these, added on top of the real values, purely
so Chapter 1 has something concrete to practice finding and fixing — each one is listed
here exactly, with no attempt to disguise it as a genuine DWD error:

1. **5 rows** where `Precipitation_mm`'s real numeric value was rewritten as a text
   string with a stray unit suffix, e.g. `"885.0mm"` instead of `885.0`.
2. **4 rows duplicated** (8 rows total), simulating an overlapping/re-merged export —
   the row's values are still the same real measurement, just repeated.
3. **3 rows** where the real `Sunshine_hours` value was blanked out (`NA`), to practice
   a missing-data check.

Raw file: 208 rows (204 real rows + 4 duplicates). Clean file: 204 rows (5 regions ×
34 years + Deutschland × 34 years = 170 + 34 = 204), matching what Chapter 1's own
coverage check expects.

## Two real signals used across Chapters 2–4

- **Warming trend.** Comparing the first ten years of the period (1991–2000) against
  the most recent ten (2015–2024), pooling all five regions ($n=50$ each): mean
  temperature rises from 8.99°C to 10.16°C, a real **+1.18°C** difference. A
  permutation test on this comparison (Chapter 3, Exercise 3.3) gives $p < 0.001$ with
  a *large* effect size (Cohen's $d \approx 1.45$) — a genuinely large, not merely
  statistically-detectable, shift. Regressing temperature on year alone gives a slope of
  about **+0.048°C per year (≈0.48°C per decade)**, $R^2 \approx 0.27$.
- **Drier, sunnier.** Over the same two ten-year windows, pooling all five regions
  ($n=50$ each, matching the temperature comparison above): mean precipitation falls by
  about **40.6mm/year** (845mm → 805mm) and mean sunshine duration rises by about
  **189 hours/year** (1596h → 1785h) — consistent with, though not proof of, a shifting
  regional climate (Chapter 3's "beyond the p-value" discussion asks you to interrogate
  exactly this distinction). (The national-only series, `Region == "Deutschland"`, shows
  a very similar but not identical pattern — −43.8mm/year, +188.6 hours/year — a useful
  reminder to always say explicitly which population a summary number was computed over.)
- **A real cold outlier.** 1996 is Germany's coldest year in the 1991–2024 record
  (national mean 7.2°C, the lowest of all 34 years) — a genuine outlier under the
  1.5×IQR rule in three of the five individual regions (Nordrhein-Westfalen, Sachsen,
  Schleswig-Holstein), and each region's coldest or near-coldest year even where its own
  natural variability is wide enough that the IQR rule doesn't flag it. This is the
  primary outlier example used in Chapter 2.
- **Two real dry years.** 2003 and 2018 are the two driest years nationally in the
  1991–2024 record (real, well-documented German drought years) — and also, somewhat
  counter-intuitively, two of the least sunny years, not the sunniest. Checking the
  *temperature* record separately, only 2018 was also unusually warm nationally (rank 4
  of 34); 2003's famous summer heatwave does not stand out in the *annual* mean, a good
  reminder that an annual average can hide a dramatic single season. These are real
  environmental extremes, not sensor errors — a secondary outlier example in Chapter 2.

## Relationships used in Chapter 4

`Temperature_C ~ Sunshine_hours` alone is a real but *weak* relationship (slope ≈
0.0015°C/hour, $R^2 \approx 0.08$, $p < 0.001$) — statistically detectable with $n=170$,
but explaining only a small share of the variation, a useful honest contrast to Chapter
3's much larger year-over-year effect. Adding `Year` and `Region` as further predictors
raises adjusted $R^2$ from about 0.07 to about 0.57 — here, unlike some textbook
examples, the added complexity clearly *does* earn its place (`anova()` $p < 0.001$),
because temperature genuinely depends on both the warming trend over time and on
geography, not on sunshine duration alone.

## Superseded datasets (removed)

Two earlier versions of this module's practice dataset — a synthetic water-quality
dataset (`water_quality_raw.csv`, `water_quality_clean.csv`, `generate_dataset.py`) and
a synthetic station-climate dataset (`station_climate_*.csv`, an earlier revision of
`generate_climate_dataset.py` now overwritten by the real-data version described above)
— are no longer referenced anywhere and have been deleted from this folder. This note is
kept only so nobody goes looking for those filenames after seeing them mentioned
elsewhere (e.g. in older commit history).

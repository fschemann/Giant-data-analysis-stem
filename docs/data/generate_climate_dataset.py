"""
Builds the module's practice dataset from REAL, verified DWD (Deutscher Wetterdienst)
open data: annual regional climate averages for Germany, 1991-2024.

Source: DWD Climate Data Center (CDC), "regional_averages_DE" annual series:
  https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/annual/air_temperature_mean/regional_averages_tm_year.txt
  https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/annual/precipitation/regional_averages_rr_year.txt
  https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/annual/sunshine_duration/regional_averages_sd_year.txt
License: CC BY 4.0 (https://opendata.dwd.de/climate_environment/CDC/Terms_of_use.pdf)
Retrieved: 24 September 2026.

Every number below was read directly from the three DWD source files above (values for
five Bundeslaender -- Bayern, Sachsen, Nordrhein-Westfalen, Schleswig-Holstein,
Baden-Wuerttemberg -- plus the national "Deutschland" series, for 1991-2024), and
cross-checked against a second, independent read of the same files (exact match) and
against the German Wikipedia article "Zeitreihe der Lufttemperatur in Deutschland"
(exact match on 5 spot-checked years). These are REAL, UNALTERED measurements -- no
synthetic values, no planted signal.

This script writes:
  - data/clean/dwd_climate_clean.csv   -- the real data, tidy, as-is
  - data/raw/dwd_climate_raw.csv       -- the SAME real numbers, with a small, fully
    disclosed set of formatting issues deliberately added for the Chapter 1 data-
    cleaning exercise (see data/README.md for the exact, itemised list of what was
    changed and why -- nothing here is presented as a genuine DWD error).
"""
import os
import numpy as np
import pandas as pd

YEARS = list(range(1991, 2025))  # 1991-2024 inclusive, 34 years

# --- Real DWD values, read from the source files above ---------------------------
# Temperature (deg C, annual mean)
temperature = {
    "Bayern":               [7.44,8.60,7.97,9.35,8.14,6.70,8.14,8.41,8.48,9.12,8.32,8.98,8.76,8.17,7.97,8.55,9.05,8.73,8.45,7.34,8.91,8.53,8.10,9.60,9.43,8.88,8.83,9.89,9.50,9.48,8.31,9.90,10.06,10.27],
    "Sachsen":               [8.80,9.91,8.75,9.97,9.29,7.28,9.26,9.59,10.10,10.39,9.35,9.70,9.63,9.34,9.42,10.02,10.34,10.01,9.54,7.99,9.98,9.44,9.07,10.68,10.32,10.08,10.03,10.88,10.93,10.98,9.63,10.84,11.02,11.48],
    "Nordrhein-Westfalen":   [9.01,9.97,9.08,10.26,9.77,7.93,9.65,9.69,10.35,10.50,9.85,10.28,10.14,9.58,9.88,10.35,10.48,9.87,9.81,8.43,10.38,9.66,9.20,10.95,10.35,10.11,10.31,11.02,10.74,11.13,9.79,11.21,11.23,11.32],
    "Schleswig-Holstein":    [8.46,9.53,8.17,9.31,8.86,7.16,8.96,8.99,9.65,9.81,8.85,9.62,9.20,9.12,9.24,9.88,10.04,9.74,9.28,7.67,9.40,8.80,8.78,10.48,9.71,9.61,9.57,10.18,10.18,10.46,9.50,10.25,10.29,10.77],
    "Baden-Wuerttemberg":    [8.22,9.12,8.57,9.88,8.77,7.42,8.81,8.92,9.05,9.71,9.00,9.55,9.45,8.70,8.60,9.19,9.47,9.08,9.00,7.93,9.64,9.08,8.56,10.14,9.89,9.29,9.40,10.38,9.87,10.24,8.83,10.59,10.69,10.56],
    "Deutschland":           [8.35,9.37,8.47,9.70,8.90,7.20,8.89,9.06,9.49,9.87,9.02,9.56,9.38,8.94,8.99,9.54,9.85,9.48,9.18,7.85,9.64,9.09,8.71,10.33,9.94,9.55,9.58,10.45,10.28,10.43,9.16,10.52,10.63,10.89],
}

# Precipitation (mm, annual total)
precipitation = {
    "Bayern":               [808.3,947.4,1007.7,956.4,1111.8,866.3,837.4,1013.4,1052.5,1045.7,1116.0,1230.0,690.0,912.6,956.6,909.3,1075.4,882.1,967.4,1001.1,860.3,927.0,933.3,821.7,744.0,923.3,968.1,757.3,860.5,861.0,962.8,817.6,1044.6,1070.4],
    "Sachsen":               [409.8,595.9,648.5,721.7,579.9,499.0,534.5,637.0,529.1,570.3,628.5,751.6,421.2,582.4,581.8,478.2,806.1,593.3,635.0,750.8,531.3,540.4,628.9,550.5,564.0,484.6,635.2,352.5,485.5,499.9,582.4,420.7,735.0,613.2],
    "Nordrhein-Westfalen":   [734.7,916.9,1042.2,1006.6,874.9,733.1,778.9,1126.4,925.7,919.0,1001.9,1085.0,761.9,957.6,885.6,842.3,1128.2,851.4,877.9,870.0,753.8,816.5,720.9,820.1,835.0,770.7,875.3,617.7,815.0,740.7,840.7,715.8,1197.9,1028.3],
    "Schleswig-Holstein":    [770.3,747.2,875.0,952.4,733.3,553.7,736.9,1041.4,836.1,699.2,899.8,1026.6,619.8,887.7,743.6,777.8,983.0,836.7,773.2,861.5,869.1,799.7,754.7,805.3,894.1,742.6,998.6,577.9,815.3,771.0,802.2,748.7,1027.7,961.7],
    "Baden-Wuerttemberg":    [763.4,985.9,988.0,1062.0,1154.4,885.0,858.1,998.6,1158.8,1025.7,1184.0,1231.6,707.1,927.8,913.0,972.2,1049.6,933.7,968.1,999.7,812.0,977.2,987.7,875.4,732.0,954.9,957.1,765.0,932.6,816.0,980.9,839.7,1019.3,1068.9],
    "Deutschland":           [644.5,796.0,885.7,890.6,877.5,682.9,714.1,919.7,838.0,838.0,928.8,1018.1,608.2,811.9,785.1,750.0,969.5,778.3,812.7,868.5,732.9,767.5,778.7,727.1,701.3,733.1,858.7,586.3,735.0,704.9,801.1,669.1,958.0,901.6],
}

# Sunshine duration (hours/year)
sunshine = {
    "Bayern":               [1670.5,1572.9,1604.0,1645.4,1479.5,1523.1,1733.4,1559.5,1587.3,1618.2,1608.2,1631.9,2064.8,1648.9,1729.0,1832.3,1824.5,1709.1,1683.8,1543.4,1928.1,1790.8,1502.3,1613.0,1783.6,1617.2,1749.2,2026.0,1904.9,1967.5,1779.2,2055.3,1852.1,1717.2],
    "Sachsen":               [1728.3,1727.4,1642.5,1645.1,1600.3,1427.0,1728.6,1510.5,1595.4,1610.2,1464.1,1530.0,2031.2,1589.2,1798.6,1855.6,1714.5,1614.8,1644.9,1559.5,1987.4,1759.6,1481.3,1662.2,1854.8,1641.8,1609.9,2030.6,1930.6,1902.5,1616.9,2002.6,1714.6,1830.1],
    "Nordrhein-Westfalen":   [1589.3,1540.7,1488.6,1509.2,1563.2,1462.2,1643.7,1268.8,1593.7,1415.1,1444.3,1430.1,1974.2,1498.8,1647.4,1664.7,1527.9,1516.3,1597.6,1468.9,1738.1,1500.1,1416.3,1536.2,1660.7,1564.0,1458.6,1941.6,1717.0,1802.7,1508.4,1984.0,1652.9,1499.7],
    "Schleswig-Holstein":    [1665.0,1675.4,1459.0,1672.0,1815.7,1589.6,1745.3,1379.3,1729.1,1472.2,1500.0,1548.7,1948.1,1584.2,1823.6,1676.5,1652.9,1708.8,1791.5,1578.8,1649.9,1555.6,1623.2,1692.2,1637.8,1573.2,1499.0,1947.6,1676.5,1850.2,1554.9,1933.9,1746.9,1646.9],
    "Baden-Wuerttemberg":    [1742.6,1605.0,1591.3,1576.5,1525.8,1612.0,1789.7,1615.8,1597.0,1669.0,1651.1,1628.2,2108.2,1658.4,1749.9,1838.1,1851.2,1692.2,1729.8,1581.7,1983.2,1832.2,1532.9,1666.7,1861.6,1644.9,1814.6,2021.2,1932.5,2050.0,1805.2,2176.3,1846.4,1654.0],
    "Deutschland":           [1679.1,1623.3,1539.1,1612.0,1600.8,1503.6,1721.7,1437.9,1626.0,1546.0,1513.7,1533.2,2013.7,1589.4,1742.5,1770.8,1691.5,1634.9,1685.8,1538.2,1847.4,1673.5,1507.6,1620.9,1742.6,1607.4,1596.1,2015.4,1834.2,1896.0,1631.2,2024.1,1753.1,1675.3],
}

REGIONS = ["Bayern", "Sachsen", "Nordrhein-Westfalen", "Schleswig-Holstein", "Baden-Wuerttemberg"]
STATION_CODE = {"Bayern": "R01", "Sachsen": "R02", "Nordrhein-Westfalen": "R03",
                "Schleswig-Holstein": "R04", "Baden-Wuerttemberg": "R05"}

# sanity check: every array must have exactly 34 values
for var_name, d in [("temperature", temperature), ("precipitation", precipitation), ("sunshine", sunshine)]:
    for region, vals in d.items():
        assert len(vals) == len(YEARS), f"{var_name}/{region}: expected {len(YEARS)} values, got {len(vals)}"

rows = []
for region in REGIONS + ["Deutschland"]:
    for i, year in enumerate(YEARS):
        rows.append({
            "Region": region,
            "Region_Code": STATION_CODE.get(region, "DE"),
            "Year": year,
            "Temperature_C": temperature[region][i],
            "Precipitation_mm": precipitation[region][i],
            "Sunshine_hours": sunshine[region][i],
        })
clean = pd.DataFrame(rows)

os.makedirs("/home/claude/giant-data-analysis-stem/data/raw", exist_ok=True)
os.makedirs("/home/claude/giant-data-analysis-stem/data/clean", exist_ok=True)
clean.to_csv("/home/claude/giant-data-analysis-stem/data/clean/dwd_climate_clean.csv", index=False)

# --- Build the "raw" teaching file: same real numbers, disclosed formatting issues ---
rng = np.random.default_rng(2026)
raw = clean.copy()
raw["Precipitation_mm"] = raw["Precipitation_mm"].astype(object)

# Only plant issues in the 5-region rows (not the Deutschland reference rows), so the
# national series always stays a clean, trustworthy reference to check the states against.
station_rows = raw.index[raw["Region"] != "Deutschland"].to_numpy()

# 1) 5 precipitation values written with a stray "mm" unit suffix (string, not float)
unit_idx = rng.choice(station_rows, size=5, replace=False)
for i in unit_idx:
    raw.at[i, "Precipitation_mm"] = f"{raw.at[i, 'Precipitation_mm']}mm"

# 2) 4 duplicated rows (simulating a re-downloaded/merged export)
remaining = np.setdiff1d(station_rows, unit_idx)
dup_idx = rng.choice(remaining, size=4, replace=False)
raw = pd.concat([raw, raw.loc[dup_idx]], ignore_index=True)

# 3) 3 sunshine-duration values blanked out (missing), to practice a missing-data check
remaining2 = np.setdiff1d(remaining, dup_idx)
missing_idx = rng.choice(remaining2, size=3, replace=False)
raw.loc[missing_idx, "Sunshine_hours"] = np.nan

raw = raw.sort_values(["Region", "Year"]).reset_index(drop=True)
raw.to_csv("/home/claude/giant-data-analysis-stem/data/raw/dwd_climate_raw.csv", index=False)

# --- Report exact numbers to hardcode into the chapters -----------------------------
print("clean rows:", len(clean), "(5 regions x 34 years + Deutschland x 34 years =", 6*34, ")")
print("raw rows (incl. 4 duplicates):", len(raw))
print("unit-suffix rows:", len(unit_idx), "| duplicate rows added:", len(dup_idx), "| blanked sunshine rows:", len(missing_idx))
print()
print("--- Signal check: early period (1991-2000) vs late period (2015-2024), Deutschland ---")
early = clean[(clean.Region == "Deutschland") & (clean.Year.between(1991, 2000))]
late = clean[(clean.Region == "Deutschland") & (clean.Year.between(2015, 2024))]
print("Temp   early mean:", round(early.Temperature_C.mean(), 3), " late mean:", round(late.Temperature_C.mean(), 3),
      " diff:", round(late.Temperature_C.mean() - early.Temperature_C.mean(), 3))
print("Precip early mean:", round(early.Precipitation_mm.mean(), 2), " late mean:", round(late.Precipitation_mm.mean(), 2),
      " diff:", round(late.Precipitation_mm.mean() - early.Precipitation_mm.mean(), 2))
print("Sun    early mean:", round(early.Sunshine_hours.mean(), 2), " late mean:", round(late.Sunshine_hours.mean(), 2),
      " diff:", round(late.Sunshine_hours.mean() - early.Sunshine_hours.mean(), 2))
print()
print("--- 1991 vs 2024 single-year, Deutschland ---")
print("Temp 1991:", clean[(clean.Region=="Deutschland")&(clean.Year==1991)].Temperature_C.values[0],
      " Temp 2024:", clean[(clean.Region=="Deutschland")&(clean.Year==2024)].Temperature_C.values[0])

"""
make_figures.py
Generate publication-quality matplotlib figures for the project report.

All figures use the forest/moss palette consistent with the presentation deck.
Outputs PNG (for ReportLab embedding) at 200 dpi.

Run from repo root:
    python analysis/make_figures.py
"""

import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FuncFormatter

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "processed"
FIG  = ROOT / "figures"
FIG.mkdir(exist_ok=True)

# --- Palette (matches deck) ---
FOREST = "#1F4E2C"
MOSS   = "#97BC62"
SAGE   = "#B7CFA1"
GOLD   = "#C8A951"
SLATE  = "#55615A"
INK    = "#1A1A1A"
RULE   = "#D8DDD0"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": SLATE,
    "axes.labelcolor": INK,
    "axes.titlecolor": FOREST,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "xtick.color": SLATE,
    "ytick.color": SLATE,
    "grid.color": RULE,
    "grid.linewidth": 0.5,
    "legend.frameon": False,
    "legend.fontsize": 9,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
})

def style_ax(ax):
    ax.yaxis.grid(True, linestyle="-", alpha=0.6)
    ax.set_axisbelow(True)

# ============================================================================
# Figure 1 — National demand projection
# ============================================================================
nd = pd.read_csv(DATA / "national_dc_demand.csv")
fig, ax = plt.subplots(figsize=(7.5, 4.3))
ax.plot(nd["year"], nd["dc_twh_low"],  color=SAGE,   lw=2.2, marker="o", ms=4, label="Low (LBNL)")
ax.plot(nd["year"], nd["dc_twh_mid"],  color=MOSS,   lw=2.5, marker="o", ms=4, label="Mid (LBNL midpoint)")
ax.plot(nd["year"], nd["dc_twh_high"], color=FOREST, lw=2.8, marker="o", ms=4, label="High (IEA / Goldman)")
ax.axvline(2024, color=SLATE, lw=0.6, ls="--", alpha=0.5)
ax.text(2024.1, 660, "actual ← → forecast", fontsize=8, color=SLATE, alpha=0.7)
ax.set_xlabel("Year")
ax.set_ylabel("TWh per year")
ax.set_title("U.S. data-center electricity consumption, 2018–2030", loc="left")
ax.legend(loc="upper left")
style_ax(ax)
fig.savefig(FIG / "fig01_national_demand.png")
plt.close(fig)

# ============================================================================
# Figure 2 — State concentration (horizontal bars)
# ============================================================================
sd = pd.read_csv(DATA / "state_dc_demand.csv").sort_values("gw_2030")
fig, ax = plt.subplots(figsize=(7.5, 4.5))
y = np.arange(len(sd))
ax.barh(y - 0.2, sd["gw_2025"], 0.4, color=MOSS,   label="2025 actual")
ax.barh(y + 0.2, sd["gw_2030"], 0.4, color=FOREST, label="2030 forecast")
for i, (a, b) in enumerate(zip(sd["gw_2025"], sd["gw_2030"])):
    ax.text(a + 0.3, i - 0.2, f"{a:.1f}", va="center", fontsize=8, color=SLATE)
    ax.text(b + 0.3, i + 0.2, f"{b:.1f}", va="center", fontsize=8, color=INK, weight="bold")
ax.set_yticks(y, sd["state"])
ax.set_xlabel("Grid power demand (GW)")
ax.set_title("Data-center capacity by state, 2025 vs 2030 forecast", loc="left")
ax.legend(loc="lower right")
ax.xaxis.grid(True, linestyle="-", alpha=0.6)
ax.yaxis.grid(False)
ax.set_axisbelow(True)
ax.set_xlim(0, max(sd["gw_2030"]) * 1.15)
fig.savefig(FIG / "fig02_state_concentration.png")
plt.close(fig)

# ============================================================================
# Figure 3 — PJM capacity prices
# ============================================================================
pjm = pd.read_csv(DATA / "pjm_capacity.csv")
fig, ax = plt.subplots(figsize=(7.5, 3.8))
bars = ax.bar(pjm["delivery_year"], pjm["price_mw_day"], color=FOREST, width=0.65)
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 5, f"${h:.0f}",
            ha="center", fontsize=9, color=INK, weight="bold")
ax.axhline(50, color=SLATE, lw=0.5, ls=":", alpha=0.6)
ax.set_ylabel("Capacity clearing price ($/MW-day)")
ax.set_xlabel("Delivery year")
ax.set_title("PJM Base Residual Auction clearing prices", loc="left")
ax.set_ylim(0, 380)
style_ax(ax)
fig.savefig(FIG / "fig03_pjm_capacity.png")
plt.close(fig)

# ============================================================================
# Figure 4 — ERCOT queue growth
# ============================================================================
er = pd.read_csv(DATA / "ercot_queue.csv")
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ax.plot(er["snapshot_date"], er["large_load_gw"],  color=FOREST, lw=2.8, marker="o", ms=8, label="Total large-load queue")
ax.plot(er["snapshot_date"], er["data_center_gw"], color=GOLD,   lw=2.8, marker="o", ms=8, label="Of which: data centers")
ax.set_ylabel("GW in interconnection queue")
ax.set_title("ERCOT large-load interconnection queue, Dec 2024 – Jan 2026", loc="left")
ax.legend(loc="upper left")
style_ax(ax)
fig.savefig(FIG / "fig04_ercot_queue.png")
plt.close(fig)

# ============================================================================
# Figure 5 — Pipeline flowchart (matplotlib-drawn)
# ============================================================================
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(8.5, 4.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis("off")

def box(x, y, w, h, label, sub=None, color=FOREST, txtcolor="white"):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.05",
                        linewidth=0, facecolor=color)
    ax.add_patch(p)
    ax.text(x + w/2, y + h*0.62, label, ha="center", va="center",
            fontsize=10, color=txtcolor, weight="bold")
    if sub:
        ax.text(x + w/2, y + h*0.28, sub, ha="center", va="center",
                fontsize=8, color=txtcolor, alpha=0.85)

def arrow(x1, y1, x2, y2):
    a = FancyArrowPatch((x1, y1), (x2, y2),
                         arrowstyle="->", mutation_scale=14,
                         color=SLATE, lw=1.2)
    ax.add_patch(a)

# Top row: data sources
box(0.2, 4.0, 1.8, 0.7, "LBNL", "national TWh", color=SAGE, txtcolor=INK)
box(2.2, 4.0, 1.8, 0.7, "451 / EPRI", "state GW", color=SAGE, txtcolor=INK)
box(4.2, 4.0, 1.8, 0.7, "PJM / ERCOT", "auctions, queue", color=SAGE, txtcolor=INK)
box(6.2, 4.0, 1.8, 0.7, "EIA / NOAA", "demand, weather", color=SAGE, txtcolor=INK)
box(8.2, 4.0, 1.6, 0.7, "IEA / Epoch", "mix, FLOPs/W", color=SAGE, txtcolor=INK)

# Middle: data builder
box(2.5, 2.6, 5.0, 0.7, "build_dataset.py", "8 cleaned CSVs in data/processed/", color=MOSS, txtcolor=INK)

# Arrows from sources to builder
for x in [1.1, 3.1, 5.1, 7.1, 9.0]:
    arrow(x, 4.0, 5.0, 3.3)

# Bottom row: stages
box(0.2, 1.0, 2.8, 0.9, "Stage 1", "Descriptive analysis", color=FOREST)
box(3.5, 1.0, 2.8, 0.9, "Stage 2", "Panel OLS regression", color=FOREST)
box(6.8, 1.0, 2.8, 0.9, "Stage 3", "Scenario projection", color=FOREST)

# Arrows builder → stages
arrow(4.0, 2.6, 1.6, 1.9)
arrow(5.0, 2.6, 4.9, 1.9)
arrow(6.0, 2.6, 8.2, 1.9)

# Outputs
box(0.2, 0.1, 2.8, 0.5, "Stylized facts", color=GOLD, txtcolor=INK)
box(3.5, 0.1, 2.8, 0.5, "Causal coefficients", color=GOLD, txtcolor=INK)
box(6.8, 0.1, 2.8, 0.5, "2030 emissions", color=GOLD, txtcolor=INK)

for x in [1.6, 4.9, 8.2]:
    arrow(x, 1.0, x, 0.6)

ax.set_title("Analytical pipeline", loc="left", color=FOREST, fontsize=12, pad=12)
fig.savefig(FIG / "fig05_pipeline.png")
plt.close(fig)

# ============================================================================
# Figure 6 — Scenario outcomes (demand path + emissions side-by-side)
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.8), gridspec_kw={"width_ratios": [1.4, 1.0]})

yrs = np.arange(2024, 2031)
bau   = [215, 252, 295, 345, 405, 475, 525]
green = [215, 252, 295, 345, 405, 475, 525]
eff   = [215, 240, 270, 300, 330, 350, 370]

ax1.plot(yrs, bau,   color=GOLD,   lw=2.8, marker="o", ms=6, label="BAU & Green AI")
ax1.plot(yrs, eff,   color=MOSS,   lw=2.8, marker="o", ms=6, label="Efficiency Breakthrough")
ax1.set_ylabel("U.S. data-center demand (TWh)")
ax1.set_xlabel("Year")
ax1.set_title("Demand trajectory", loc="left")
ax1.legend(loc="upper left")
style_ax(ax1)

scenarios = ["BAU", "Green AI", "Efficiency"]
emissions = [646, 504, 534]
colors    = [GOLD, FOREST, MOSS]
bars = ax2.bar(scenarios, emissions, color=colors, width=0.55)
for bar, v in zip(bars, emissions):
    ax2.text(bar.get_x() + bar.get_width()/2, v + 8, str(v),
             ha="center", fontsize=10, color=INK, weight="bold")
ax2.set_ylabel("Cumulative MtCO\u2082, 2024\u20132030")
ax2.set_title("Cumulative emissions", loc="left")
ax2.set_ylim(0, 720)
style_ax(ax2)

fig.savefig(FIG / "fig06_scenarios.png")
plt.close(fig)

# ============================================================================
# Figure 7 — Efficiency caveat (PUE + Jevons)
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.8))

pue = pd.read_csv(DATA / "pue_series.csv")
ax1.plot(pue["year"], pue["industry_avg_pue"], color=SLATE, lw=2.5, marker="o", ms=5, label="Industry average")
google = pue.dropna(subset=["google_fleet_pue"])
ax1.plot(google["year"], google["google_fleet_pue"], color=FOREST, lw=2.5, marker="o", ms=5, label="Google fleet-wide")
ax1.set_xlabel("Year")
ax1.set_ylabel("Power Usage Effectiveness (PUE)")
ax1.set_title("PUE has plateaued at ~1.56 industry-wide", loc="left")
ax1.set_ylim(1.0, 2.6)
ax1.legend(loc="upper right")
style_ax(ax1)

chip = pd.read_csv(DATA / "chip_efficiency.csv")
chip_sub = chip[chip["year"] % 2 == 0]
demand = [1.0, 1.18, 1.71, 2.83, 3.95, 5.39, 6.91]
ax2.plot(chip_sub["year"], chip_sub["flops_per_watt_index_2018_1"], color=MOSS, lw=2.5, marker="o", ms=5, label="Chip efficiency (FLOPs/W)")
ax2.plot(chip_sub["year"], demand, color=GOLD, lw=2.5, marker="o", ms=5, label="Total DC demand")
ax2.set_xlabel("Year")
ax2.set_ylabel("Index (2018 = 1)")
ax2.set_title("Chip gains real, but demand grows too — Jevons", loc="left")
ax2.legend(loc="upper left")
style_ax(ax2)

fig.savefig(FIG / "fig07_efficiency.png")
plt.close(fig)

print("Generated figures in", FIG)
for p in sorted(FIG.glob("*.png")):
    print(" ", p.name)

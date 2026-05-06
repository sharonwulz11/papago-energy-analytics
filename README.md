# Papago — Energy Implications of AI-Driven Data Centers

> INDENG 290 Energy Analytics · UC Berkeley · Spring 2026
> **Team Papago:** Linzhi (Sharon) Wu · Kelly Zeng

How the rapid build-out of AI-driven data centers is reshaping U.S. electricity demand, what it's doing to regional grids, and whether efficiency or clean-energy investment can offset the impact.

---

## 📋 Project deliverables

| Deliverable                      | Path                                                    |
| -------------------------------- | ------------------------------------------------------- |
| 📄 **Project report (PDF)**      | [`report/Papago_Project_Report.pdf`](report/Papago_Project_Report.pdf)                       |
| 🎯 **Presentation deck (PPTX)**  | [`docs/Papago_Energy_Analytics_Presentation.pptx`](docs/Papago_Energy_Analytics_Presentation.pptx) |
| 🎯 **Presentation deck (PDF)**   | [`docs/Papago_Energy_Analytics_Presentation.pdf`](docs/Papago_Energy_Analytics_Presentation.pdf)   |
| 🗣️ **Speaker notes**             | [`docs/SPEAKER_NOTES.md`](docs/SPEAKER_NOTES.md)        |

---

## 🔑 Key findings

**Stage 1 — Stylized facts (firm)**
- 80% of U.S. data-center load is in 15 states; Virginia alone hosts ~26% of national capacity AND consumes ~26% of its own state electricity for data centers.
- PJM capacity prices rose from $29 to $329 per MW-day in two auctions; the Independent Market Monitor attributes 63% of the 2025/26 increase to data-center load.
- ERCOT's large-load queue grew from 63 GW (Dec 2024) to 233 GW (Jan 2026); ~77% is data centers.

**Stage 2 — Panel regression (preliminary)**
- Pooled OLS, state fixed effects, N = 288, R² = 0.93.
- Coefficient on data-center capacity: **0.64 TWh/month/GW** (t = 26.8) — annualizes to ~7.7 TWh/yr/GW, matching engineering bottom-up estimates.

**Stage 3 — Scenario comparison (tentative)**

| Scenario                | 2030 TWh | Cumulative MtCO₂ (2024–2030) | Δ vs BAU |
| ----------------------- | -------- | ---------------------------- | -------- |
| Business-as-usual       | 525      | 646                          | —        |
| Green AI Transition     | 525      | 504                          | −22%     |
| Efficiency Breakthrough | 370      | 534                          | −17%     |

Each lever alone cuts ~20% of cumulative emissions vs BAU. Both combined would be roughly additive — but neither path returns emissions to 2024 levels.

---

## 🚀 Quick start

```bash
# Clone
git clone https://github.com/sharonwu/papago-energy-analytics.git
cd papago-energy-analytics

# Install dependencies
pip install -r requirements.txt

# Reproduce the full pipeline
python data/build_dataset.py        # build cleaned CSVs in data/processed/
python analysis/analysis.py         # run regression + scenarios
python analysis/make_figures.py     # regenerate figures
python report/build_report.py       # rebuild the PDF report
```

Requires Python 3.10+.

---

## 📁 Repository structure

```
papago-energy-analytics/
├── data/
│   ├── build_dataset.py              # single-source dataset builder
│   ├── raw/                          # source PDFs and raw extracts
│   └── processed/                    # 8 cleaned CSVs (output of build_dataset.py)
├── analysis/
│   ├── analysis.py                   # Stage 2 regression + Stage 3 scenarios
│   └── make_figures.py               # publication figures (PNG)
├── outputs/                          # regression results, scenario summaries
├── figures/                          # PNG figures (used in report + deck)
├── report/
│   ├── build_report.py               # ReportLab script
│   └── Papago_Project_Report.pdf     # final 17-page report
├── docs/                             # presentation deck, speaker notes
├── requirements.txt
├── README.md                         # this file
└── LICENSE
```

---

## 📊 Data sources

All sources are publicly available; full citations are listed in [Section 5 of the report](report/Papago_Project_Report.pdf).

| Source | Provides | Link |
| --- | --- | --- |
| Lawrence Berkeley National Lab (Dec 2024) | U.S. data-center electricity 2018–2028 | [eta-publications.lbl.gov](https://eta-publications.lbl.gov/publications/2024-united-states-data-center) |
| IEA Energy and AI (Apr 2025) | Global + U.S. demand projections to 2030 | [iea.org/reports/energy-and-ai](https://www.iea.org/reports/energy-and-ai) |
| EPRI Powering Intelligence (May 2024) | Workload composition; AI vs. cloud | [epri.com](https://www.epri.com/research/products/3002028905) |
| Goldman Sachs Research (Feb 2025) | +165% global growth by 2030 | [goldmansachs.com](https://www.goldmansachs.com/insights) |
| 451 Research / S&P Global (Sep 2025) | State-level capacity (GW) | [spglobal.com](https://www.spglobal.com/marketintelligence/451-research) |
| PJM Base Residual Auction releases | Capacity clearing prices | [pjm.com](https://www.pjm.com/markets-and-operations/rpm) |
| ERCOT Long-Term Load Forecast | Large-load queue volumes | [ercot.com](https://www.ercot.com/gridinfo/load/forecast) |
| U.S. EIA Form 861 + STEO | State electricity sales; rates | [eia.gov](https://www.eia.gov/electricity/data/eia861) |
| NRDC household bill analysis | PJM ratepayer cost estimates | [nrdc.org](https://www.nrdc.org) |
| Pew Research / EPRI synthesis | Geographic distribution | [pewresearch.org](https://www.pewresearch.org) |
| Uptime Institute Global Survey 2024 | PUE trends | [uptimeinstitute.com](https://uptimeinstitute.com) |
| Epoch AI (Rahman, 2024) | Chip efficiency trajectory | [epoch.ai](https://epoch.ai) |

---

## ⚠️ Important data caveat

The `data/processed/state_monthly_panel.csv` is a **constructed** monthly panel calibrated to documented annual totals (LBNL, 451 Research, EIA STEO) with a known data-generating process for the methodology demonstration. The panel-OLS coefficients in [`outputs/regression_results.txt`](outputs/regression_results.txt) reflect this calibration. We will re-estimate on actual EIA Form 861 monthly data once the 2024 release is final; the report flags this clearly in Section 5.3.

All other figures (PJM auction prices, ERCOT queue, LBNL/IEA/Goldman projections, hyperscaler PUE values, household bill impacts) come directly from cited primary or secondary sources.

---

## 🔧 Reproducibility

Every figure and number in the report is reproducible from this repository:

1. `data/build_dataset.py` reads source values (encoded in the script with citations) and writes cleaned CSVs.
2. `analysis/analysis.py` runs the panel-OLS regression and computes the three scenarios; outputs land in `outputs/`.
3. `analysis/make_figures.py` produces the seven publication PNGs in `figures/`.
4. `report/build_report.py` assembles the 17-page PDF.

Random seeds are set; outputs are deterministic.

---

## 📝 Citation

If you use this work, please cite:

```bibtex
@misc{wu_zeng_2026_papago,
  title  = {The Energy Implications of AI-Driven Data Centers:
            Demand Forecasting, Grid Stress, and Efficiency Trade-offs},
  author = {Wu, Linzhi and Zeng, Kelly},
  year   = {2026},
  note   = {INDENG 290 Energy Analytics, UC Berkeley},
  url    = {https://github.com/sharonwulz11/papago-energy-analytics}
}
```

---

## 📄 License

MIT — see [`LICENSE`](LICENSE).

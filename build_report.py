"""
build_report.py
Build the Papago project report PDF using ReportLab Platypus.

Style: light, prose-heavy, ~18 pages, forest-green palette consistent
with the project presentation deck.

Run from repo root:
    python report/build_report.py
"""

import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Image, KeepTogether, HRFlowable, Frame, PageTemplate, BaseDocTemplate,
    NextPageTemplate,
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parent.parent
FIG  = ROOT / "figures"
REPORT_DIR = ROOT / "report"
REPORT_DIR.mkdir(exist_ok=True)
OUT_PDF = REPORT_DIR / "Papago_Project_Report.pdf"

# -------- Palette (matches deck) --------
FOREST = HexColor("#1F4E2C")
MOSS   = HexColor("#97BC62")
SAGE   = HexColor("#B7CFA1")
SAGEBG = HexColor("#EEF3E6")
CREAM  = HexColor("#FAFAF6")
WHITE  = HexColor("#FFFFFF")
INK    = HexColor("#1A1A1A")
SLATE  = HexColor("#55615A")
MUTED  = HexColor("#8A958E")
RULE   = HexColor("#D8DDD0")
GOLD   = HexColor("#C8A951")

# -------- Styles --------
ss = getSampleStyleSheet()

styles = {
    "h1": ParagraphStyle("h1", fontName="Times-Bold", fontSize=20, leading=24,
                         textColor=FOREST, spaceAfter=10, spaceBefore=0),
    "h2": ParagraphStyle("h2", fontName="Times-Bold", fontSize=14, leading=18,
                         textColor=FOREST, spaceAfter=6, spaceBefore=14),
    "h3": ParagraphStyle("h3", fontName="Times-Bold", fontSize=11.5, leading=14,
                         textColor=FOREST, spaceAfter=3, spaceBefore=10),
    "body": ParagraphStyle("body", fontName="Times-Roman", fontSize=10.5, leading=14,
                           textColor=INK, alignment=TA_JUSTIFY, spaceAfter=8),
    "bodysmall": ParagraphStyle("bodysmall", fontName="Times-Roman", fontSize=9.5, leading=12,
                                textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6),
    "callout": ParagraphStyle("callout", fontName="Times-Italic", fontSize=10.5, leading=14,
                              textColor=FOREST, alignment=TA_LEFT,
                              leftIndent=12, spaceBefore=6, spaceAfter=6,
                              borderColor=FOREST, borderWidth=0,
                              borderPadding=0),
    "caption": ParagraphStyle("caption", fontName="Times-Italic", fontSize=9, leading=11,
                              textColor=SLATE, alignment=TA_LEFT, spaceAfter=10, spaceBefore=2),
    "kicker": ParagraphStyle("kicker", fontName="Helvetica-Bold", fontSize=8, leading=10,
                             textColor=MOSS, spaceAfter=4, spaceBefore=2),
    "muted": ParagraphStyle("muted", fontName="Times-Italic", fontSize=9, leading=11,
                            textColor=MUTED, alignment=TA_LEFT, spaceAfter=6),
    "bullet": ParagraphStyle("bullet", fontName="Times-Roman", fontSize=10.5, leading=14,
                             textColor=INK, alignment=TA_LEFT,
                             leftIndent=18, bulletIndent=4, spaceAfter=4),
    "tablecell": ParagraphStyle("tablecell", fontName="Times-Roman", fontSize=9.5,
                                leading=12, textColor=INK),
    "tablehdr": ParagraphStyle("tablehdr", fontName="Helvetica-Bold", fontSize=9.5,
                               leading=12, textColor=FOREST),
}

# -------- Page templates --------
def cover_page(canvas, doc):
    canvas.saveState()
    # Left vertical accent rule
    canvas.setFillColor(FOREST)
    canvas.rect(0.55*inch, 0.6*inch, 0.06*inch, letter[1] - 1.2*inch, fill=1, stroke=0)
    canvas.restoreState()

def regular_page(canvas, doc):
    canvas.saveState()
    # Header rule
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.3)
    canvas.line(0.75*inch, letter[1] - 0.65*inch, letter[0] - 0.75*inch, letter[1] - 0.65*inch)
    # Header text
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.75*inch, letter[1] - 0.5*inch, "PAPAGO  ·  ENERGY IMPLICATIONS OF AI-DRIVEN DATA CENTERS")
    canvas.drawRightString(letter[0] - 0.75*inch, letter[1] - 0.5*inch, "INDENG 290  ·  SPRING 2026")
    # Footer rule
    canvas.line(0.75*inch, 0.55*inch, letter[0] - 0.75*inch, 0.55*inch)
    # Footer text
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.75*inch, 0.4*inch, "Linzhi Wu  ·  Kelly Zeng")
    canvas.drawRightString(letter[0] - 0.75*inch, 0.4*inch, f"Page {doc.page}")
    canvas.restoreState()

# -------- Custom flowables --------
class HRule(Flowable):
    """A simple thin horizontal line."""
    def __init__(self, width, color=RULE, thickness=0.4):
        super().__init__()
        self.width = width
        self.color = color
        self.thickness = thickness
    def wrap(self, *args):
        return self.width, self.thickness
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)

class AccentRule(Flowable):
    """Short forest-green accent rule."""
    def __init__(self, width=0.5*inch, color=FOREST, thickness=2):
        super().__init__()
        self.width = width
        self.color = color
        self.thickness = thickness
    def wrap(self, *args):
        return self.width, self.thickness
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)

# -------- Helpers --------
def kicker(text):
    return Paragraph(text, styles["kicker"])

def h1(text):
    return Paragraph(text, styles["h1"])

def h2(text):
    return Paragraph(text, styles["h2"])

def h3(text):
    return Paragraph(text, styles["h3"])

def p(text):
    return Paragraph(text, styles["body"])

def cap(text):
    return Paragraph(text, styles["caption"])

def muted(text):
    return Paragraph(text, styles["muted"])

def callout(text):
    return Paragraph(text, styles["callout"])

def bullet_list(items, style_key="bullet"):
    style = styles[style_key]
    out = []
    for it in items:
        out.append(Paragraph(it, style, bulletText="\u2022"))
    return out

def fig(filename, width=6.5*inch):
    """Insert a figure scaled to width."""
    img_path = FIG / filename
    img = Image(str(img_path))
    aspect = img.imageHeight / float(img.imageWidth)
    img.drawWidth = width
    img.drawHeight = width * aspect
    return img

# -------- Build doc --------
class TwoTemplateDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        # Cover frame: full page, no header/footer
        cover_frame = Frame(0.85*inch, 0.6*inch, letter[0] - 1.7*inch, letter[1] - 1.2*inch,
                             leftPadding=0, rightPadding=0,
                             topPadding=0, bottomPadding=0, id="cover_frame")
        # Regular content frame: leaves room for header/footer
        content_frame = Frame(0.75*inch, 0.7*inch, letter[0] - 1.5*inch, letter[1] - 1.4*inch,
                               leftPadding=0, rightPadding=0,
                               topPadding=0, bottomPadding=0, id="content_frame")
        self.addPageTemplates([
            PageTemplate(id="Cover",   frames=[cover_frame], onPage=cover_page),
            PageTemplate(id="Regular", frames=[content_frame], onPage=regular_page),
        ])

doc = TwoTemplateDoc(
    str(OUT_PDF),
    pagesize=letter,
    title="The Energy Implications of AI-Driven Data Centers",
    author="Linzhi Wu, Kelly Zeng",
    subject="INDENG 290 Project Report",
)

story = []

# ============================================================================
# COVER PAGE
# ============================================================================
story.append(Spacer(1, 1.2*inch))

# Kicker
story.append(Paragraph(
    '<font name="Helvetica-Bold" size="10" color="#97BC62">INDENG 290 ENERGY ANALYTICS</font>',
    ParagraphStyle("cover_kicker", fontName="Helvetica", fontSize=10, leading=14)))
story.append(Spacer(1, 0.06*inch))
story.append(Paragraph(
    '<font name="Helvetica-Bold" size="10" color="#8A958E">PROJECT REPORT</font>',
    ParagraphStyle("cover_kicker2", fontName="Helvetica", fontSize=10, leading=14)))

story.append(Spacer(1, 0.7*inch))

story.append(Paragraph(
    "The Energy Implications of",
    ParagraphStyle("cover_title", fontName="Times-Bold", fontSize=36, leading=42, textColor=FOREST)))
story.append(Paragraph(
    "AI-Driven Data Centers",
    ParagraphStyle("cover_title2", fontName="Times-Bold", fontSize=36, leading=42, textColor=FOREST)))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph(
    "<i>Demand forecasting · grid stress · efficiency trade-offs</i>",
    ParagraphStyle("cover_sub", fontName="Times-Italic", fontSize=15, leading=18, textColor=SLATE)))

story.append(Spacer(1, 1.5*inch))

story.append(AccentRule(width=0.5*inch))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph(
    "<b>Team Papago</b>",
    ParagraphStyle("cover_team", fontName="Helvetica", fontSize=12, leading=15, textColor=INK)))
story.append(Spacer(1, 0.04*inch))
story.append(Paragraph(
    "Linzhi (Sharon) Wu  ·  Kelly Zeng",
    ParagraphStyle("cover_names", fontName="Helvetica", fontSize=11, leading=14, textColor=SLATE)))
story.append(Spacer(1, 0.04*inch))
story.append(Paragraph(
    "UC Berkeley  ·  Spring 2026  ·  Submitted May 11, 2026",
    ParagraphStyle("cover_meta", fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED)))

story.append(NextPageTemplate("Regular"))
story.append(PageBreak())

# ============================================================================
# 2. EXECUTIVE SUMMARY
# ============================================================================
story.append(kicker("SECTION 2"))
story.append(h1("Executive Summary"))
story.append(AccentRule(width=0.5*inch))
story.append(Spacer(1, 0.15*inch))

story.append(p(
    "Artificial intelligence is reshaping U.S. electricity demand at a pace that few utility "
    "planners anticipated. The Lawrence Berkeley National Laboratory's 2024 report estimates that "
    "U.S. data centers consumed roughly 176 TWh in 2023 — about 4.4% of national electricity sales — "
    "and projects consumption between 325 and 580 TWh by 2028. The IEA's 2025 <i>Energy and AI</i> "
    "report places 2030 U.S. data-center demand near 426 TWh; Goldman Sachs Research projects a 165% "
    "global increase by 2030. This report asks how that demand growth is being absorbed by regional "
    "grids, what it is costing ratepayers, and whether efficiency or clean-energy investment can "
    "offset the resulting emissions."
))

story.append(p(
    "Our project is written for state public utility commissions and grid operators — the Virginia "
    "SCC, Texas PUCT, California CPUC, and the operators of PJM, ERCOT, and CAISO. These bodies face "
    "concrete near-term decisions about generation procurement, cost allocation, interconnection "
    "rules, and reliability backstops; secondary stakeholders include institutional investors "
    "evaluating utility and hyperscaler exposure. Our methodology has three stages: a descriptive "
    "analysis of the geographic concentration of data-center load and its market consequences; a "
    "panel-OLS regression with state fixed effects estimating the marginal effect of one gigawatt of "
    "data-center capacity on monthly electricity demand and wholesale prices; and a 2024–2030 "
    "scenario projection comparing business-as-usual against \"Green AI Transition\" and "
    "\"Efficiency Breakthrough\" trajectories."
))

story.append(p(
    "Three findings stand out. First, demand growth is geographically concentrated, not diffuse — "
    "five states host roughly 65% of U.S. data-center load, and Virginia alone accounts for about 26% "
    "of national capacity and 26% of its own state's electricity. Second, where concentration is "
    "highest, capacity markets are already stressed: PJM clearing prices rose nearly tenfold between "
    "the 2024/25 and 2025/26 auctions, and ERCOT's large-load interconnection queue grew from 63 to "
    "233 GW in thirteen months. Third, our scenario analysis suggests neither efficiency gains nor "
    "cleaner fuel mix alone is sufficient: each lever, applied independently, cuts cumulative "
    "2024–2030 emissions roughly 17–22% versus business-as-usual, but emissions remain far above a "
    "2024 baseline in every scenario because the underlying demand wedge is large."
))

story.append(p(
    "We make four recommendations to our stakeholders: (1) require demand-response capability as a "
    "condition of large-load interconnection; (2) accelerate adoption of dedicated large-load rate "
    "classes that prevent cost socialization onto residential ratepayers; (3) require co-located "
    "generation or storage commitments in the most stressed zones; and (4) expand utility-grade "
    "disclosure of facility-level data-center electricity consumption so future policy can be based "
    "on observed rather than self-reported data."
))

story.append(PageBreak())

# ============================================================================
# 3. SCOPE
# ============================================================================
story.append(kicker("SECTION 3"))
story.append(h1("Scope"))
story.append(AccentRule(width=0.5*inch))
story.append(Spacer(1, 0.15*inch))

story.append(h2("Stakeholder"))
story.append(p(
    "This project is written primarily for <b>state public utility commissions and grid operators</b> "
    "in regions where data-center load growth is most concentrated — specifically the Virginia State "
    "Corporation Commission, the Texas Public Utility Commission, the California Public Utilities "
    "Commission, and the system operators of PJM, ERCOT, and CAISO. These institutions hold "
    "regulatory authority over generation procurement, transmission planning, retail rate design, and "
    "interconnection rules; they are the loci of the consequential decisions that AI-driven demand "
    "growth is forcing in 2025–2026. Secondary stakeholders include institutional investors with "
    "exposure to regulated utilities and to hyperscaler infrastructure, who require an assessment of "
    "whether the demand growth is structural or speculative."
))

story.append(h2("Stakeholder decisions"))
story.append(p(
    "Our analysis is intended to inform four classes of decision the stakeholder is currently making:"
))
story.extend(bullet_list([
    "<b>Capacity and transmission build-out.</b> Whether to approve new natural-gas, nuclear, or transmission infrastructure to serve hyperscaler-driven load — and on what timeline.",
    "<b>Cost allocation.</b> Whether to establish dedicated rate classes for large loads (as Virginia has with its GS-5 schedule and Oregon with its dedicated tariff for cryptocurrency and data-center customers) so capacity-market and infrastructure costs are recovered from the loads that cause them rather than from residential ratepayers.",
    "<b>Interconnection rules.</b> Whether to require demand response, on-site generation, or co-located storage as a condition of large-load interconnection, and how to define the threshold at which these requirements apply.",
    "<b>Reliability backstops.</b> Whether to extend or remove price caps on capacity markets, mandate flexible-load capability, fast-track generation procurement, or pursue other mechanisms when reserve margins fall below target.",
]))

story.append(h2("Focus questions"))
story.append(p(
    "Three questions structure the analysis:"
))
story.extend(bullet_list([
    "<b>Q1.</b> How much additional electricity demand will AI-driven data centers generate over the next 5–10 years?",
    "<b>Q2.</b> How does this demand affect wholesale electricity prices, peak load, and grid stability in regions with concentrated data-center activity?",
    "<b>Q3.</b> To what extent can renewable adoption and hardware efficiency offset the environmental impact?",
]))
story.append(muted(
    "These focus questions are unchanged from the project proposal and progress update."
))

story.append(PageBreak())

# ============================================================================
# 4. METHODOLOGY
# ============================================================================
story.append(kicker("SECTION 4"))
story.append(h1("Methodology"))
story.append(AccentRule(width=0.5*inch))
story.append(Spacer(1, 0.15*inch))

story.append(h2("4.1  Performance metrics"))
story.append(p(
    "The choice of performance metrics is driven by the stakeholder's decision context. We use three:"
))
story.extend(bullet_list([
    "<b>Marginal demand elasticity</b> — TWh of monthly electricity demand per GW of installed data-center capacity, with state fixed effects. This is the central quantity for capacity-build decisions; it tells the regulator how much new generation a one-gigawatt facility actually requires once seasonal and macroeconomic variation is netted out.",
    "<b>Marginal wholesale price effect</b> — change in $/MWh wholesale price per GW of added data-center capacity. This proxies the consumer-surplus cost of demand growth and is directly relevant to cost-allocation decisions.",
    "<b>Cumulative MtCO<sub>2</sub> emissions, 2024–2030</b> — total bottom-up emissions from data-center electricity consumption under each scenario, computed by blending fuel-mix shares with EPA-grade emission factors. This is the relevant metric for evaluating the climate cost of the demand wedge.",
]))

story.append(p(
    "We considered and rejected three alternative metrics. <b>Hourly capacity factor</b> is more "
    "common in power-systems engineering, but is unmeasurable for an aggregated state panel and would "
    "have required hourly load data we could not obtain. <b>Levelized cost of electricity (LCOE)</b> "
    "is the canonical metric in generation-investment analysis, but it is a supply-side construct and "
    "obscures the demand-shock dynamics this project is trying to surface. Finally, <b>marginal "
    "emissions intensity</b> (tCO<sub>2</sub> per marginal MWh) would be more accurate than our blended-mix "
    "approach, but requires hour-by-hour dispatch data across three ISOs that is not publicly "
    "available. Our blended-mix approach is conservative — it understates emissions in regions where "
    "marginal generation is gas, and overstates emissions where it is wind."
))

story.append(h2("4.2  Pipeline design"))
story.append(p(
    "Our analytical pipeline has three stages, each producing a distinct output that flows into the "
    "stakeholder's decision context. Figure 1 maps the full pipeline."
))

story.append(fig("fig05_pipeline.png", width=6.4*inch))
story.append(cap("Figure 1.  Analytical pipeline. Five public data sources feed a single dataset-construction script (<i>build_dataset.py</i>) which produces eight cleaned CSVs in <i>data/processed/</i>. These feed three analytical stages, each producing a distinct deliverable."))

story.append(h2("4.3  Analytical design"))

story.append(h3("Stage 1: Descriptive analysis"))
story.append(p(
    "We compile state-level data-center capacity (in GW), state-level annual electricity sales (in TWh), "
    "and zonal capacity-market and queue indicators for PJM and ERCOT. The output is a small set of "
    "stylized facts the model and scenarios must explain — three of which we report in Section 6."
))

story.append(h3("Stage 2: Panel OLS with state fixed effects"))
story.append(p(
    "The estimating equation is:"
))
story.append(Paragraph(
    "<font name=\"Times-Italic\">Demand</font><sub>r,t</sub> = α<sub>r</sub> + β·<font name=\"Times-Italic\">DC_GW</font><sub>r,t</sub> + γ·<font name=\"Times-Italic\">CDD</font><sub>r,t</sub> + δ·<font name=\"Times-Italic\">HDD</font><sub>r,t</sub> + ζ·<font name=\"Times-Italic\">Industrial</font><sub>r,t</sub> + ε<sub>r,t</sub>",
    ParagraphStyle("eqn", fontName="Times-Roman", fontSize=11, leading=14, alignment=TA_CENTER,
                   spaceBefore=4, spaceAfter=10, textColor=INK)))
story.append(p(
    "where <i>r</i> indexes states (Virginia, Texas, California), <i>t</i> indexes months from January "
    "2018 through December 2025, <i>α</i><sub>r</sub> are state fixed effects absorbing time-invariant "
    "differences between states, <i>DC_GW</i> is data-center installed capacity, and <i>CDD</i>/<i>HDD</i> "
    "are cooling/heating degree-day indices. Coefficients are estimated by within-group OLS after "
    "demeaning each variable by its state mean. The dependent variable is monthly electricity demand "
    "(TWh). A parallel specification is estimated with wholesale price ($/MWh) as the dependent "
    "variable. The forecast horizon is implicitly 2030 — the regression coefficient on data-center "
    "capacity is multiplied by the projected 2030 capacity stock in each scenario."
))
story.append(p(
    "<b>Evaluation logic.</b> The naïve benchmark is a model with state fixed effects only — i.e., "
    "demand explained purely by state differences and the time-trend implicit in the data. We test "
    "whether the data-center capacity coefficient is statistically distinguishable from zero, and "
    "more importantly whether its magnitude matches the engineering bottom-up benchmark of ~6.6–7.7 "
    "TWh/year per GW (corresponding to load factors of 75–88%). A coefficient that matches the "
    "bottom-up benchmark is evidence that the model is not picking up spurious correlations. We "
    "report robust standard errors and t-statistics."
))

story.append(h3("Stage 3: Scenario projection"))
story.append(p(
    "We define three 2024–2030 trajectories. <b>Business-as-usual (BAU)</b> follows the LBNL "
    "high-mid trajectory (525 TWh by 2030, +144% vs. 2024) with a fuel mix that gets only modestly "
    "cleaner (gas 41%→38%, coal 15%→7%, renewables 24%→36%). <b>Green AI Transition</b> uses the same "
    "demand path as BAU but assumes hyperscalers shift to 24/7 carbon-free procurement, driving "
    "renewables to 55% and gas to 20%. <b>Efficiency Breakthrough</b> assumes chip efficiency holds "
    "the 40%/year trajectory documented by Epoch AI and that industry-average PUE drops from 1.56 to "
    "1.30, cutting 2030 demand to 370 TWh while retaining the BAU mix. For each scenario we compute "
    "year-by-year emissions as TWh × blended emission factor (linearly interpolated from 2024 to 2030 "
    "mix), and sum across years for cumulative MtCO<sub>2</sub>."
))

story.append(h2("4.4  Tradeoffs we considered"))
story.append(p(
    "Three methodological tradeoffs shaped the design."
))
story.extend(bullet_list([
    "<b>Granularity vs. coverage.</b> An hourly model across three ISOs would be more informative than a monthly state panel, but requires hourly load and price data at facility-level granularity that hyperscalers do not disclose. We chose monthly state-level coverage to obtain a defensible identification strategy at the cost of granularity. The hourly co-simulation is identified as our top \"unbuilt\" analysis (Section 8).",
    "<b>Identification vs. realism.</b> We could have used a structural model of generator dispatch and load, but the burden of identification would have been much higher and the result would have been less comparable to the published forecasts our stakeholder reads. The reduced-form panel approach is intentionally simple and transparent.",
    "<b>Forecast point estimates vs. ranges.</b> LBNL's 2030 range is 325–580 TWh — almost as wide as the entire 2023 total. We chose to report the LBNL midpoint (525 TWh) as the BAU anchor for tractability, but flag the range explicitly throughout the report and in the deck.",
]))

story.append(PageBreak())

# ============================================================================
# 5. DATA
# ============================================================================
story.append(kicker("SECTION 5"))
story.append(h1("Data"))
story.append(AccentRule(width=0.5*inch))
story.append(Spacer(1, 0.15*inch))

story.append(h2("5.1  Evolution of the data search"))
story.append(p(
    "Our initial proposal contemplated using utility tariff filings, hyperscaler sustainability reports, "
    "and ISO/RTO load disclosures as primary sources. Each of these proved partially or wholly "
    "unworkable. Utility tariff filings disclose aggregate load by rate class but rarely break out "
    "data-center customers; the major hyperscalers (Google, Microsoft, AWS, Meta, Oracle) report "
    "Scope 2 emissions and renewable-procurement statistics in their annual sustainability reports "
    "but do not disclose facility-level kWh, capacity, or location at a granularity useful for state-"
    "level analysis. ISO/RTO load disclosures aggregate to the zone level at best."
))
story.append(p(
    "We pivoted to a triangulation approach combining national-aggregate research (LBNL, IEA, EPRI), "
    "syndicated commercial research (451 Research / S&amp;P Global) for state and facility capacity, and "
    "primary regulatory filings (PJM Base Residual Auction releases, ERCOT Long-Term Load Forecasts) "
    "for market and queue indicators. Two further sources — utility-customer-bill data from NRDC's "
    "October 2025 analysis, and Pew Research's October 2025 synthesis of EPRI's facility distribution "
    "— filled in the residential-rate-impact and geographic-distribution dimensions. We sought but "
    "could not obtain: (1) hourly facility-level kWh for any hyperscaler; (2) ERCOT large-load queue "
    "data with project-level identifiers (only aggregate GW is published); and (3) LMP-level price "
    "data at AI-cluster nodes in PJM Dominion. The first two gaps shape the limitations described in "
    "Section 4.4; the third would have enabled a stronger Stage 2 price model and is identified as "
    "remaining work."
))

story.append(h2("5.2  Data sources actually used"))
story.append(p("All data sources used in the project are listed below with live links."))

# Build a styled reference table
data_sources = [
    ["Source", "What it provides", "Link"],
    ["Lawrence Berkeley National Lab (2024)",
     "U.S. data-center electricity consumption, 2018–2028 (low/mid/high bands)",
     "eta-publications.lbl.gov/publications/2024-united-states-data-center"],
    ["IEA Energy and AI (April 2025)",
     "Global and U.S. data-center electricity demand projections to 2030 by scenario",
     "www.iea.org/reports/energy-and-ai"],
    ["EPRI Powering Intelligence (May 2024)",
     "Data-center workload composition; AI vs. general cloud share by region",
     "www.epri.com/research/products/3002028905"],
    ["Goldman Sachs Research (Feb 2025)",
     "Global data-center power demand growth projections (+165% by 2030 vs 2023)",
     "www.goldmansachs.com/insights"],
    ["451 Research / S&amp;P Global (Sep 2025)",
     "State and facility-level data-center installed capacity (GW), 2023–2030",
     "www.spglobal.com/marketintelligence/451-research"],
    ["PJM Base Residual Auction releases (2022–2025)",
     "Capacity clearing prices ($/MW-day) for delivery years 2022/23 through 2027/28",
     "pjm.com/markets-and-operations/rpm"],
    ["ERCOT Long-Term Load Forecast (2024–2026)",
     "Large-load interconnection queue volumes and 2032 peak forecast",
     "ercot.com/gridinfo/load/forecast"],
    ["U.S. EIA Form 861 + STEO",
     "State-level annual electricity sales; national STEO; residential rates",
     "eia.gov/electricity/data/eia861"],
    ["NRDC household bill analysis (Oct 2025)",
     "PJM ratepayer cost-allocation estimates by jurisdiction",
     "nrdc.org/resources/data-centers-electricity-bills"],
    ["Pew Research / EPRI synthesis (Oct 2025)",
     "Geographic distribution of U.S. data-center load and concentration ratios",
     "pewresearch.org/short-reads/data-center-energy"],
    ["Uptime Institute Global Survey (2024)",
     "Industry-average and hyperscale Power Usage Effectiveness (PUE) trends",
     "uptimeinstitute.com/resources/research-and-reports"],
    ["Epoch AI (Rahman, 2024)",
     "Chip energy efficiency trajectory (FLOPs per watt), 2018–2024",
     "epoch.ai/blog/trends-in-machine-learning-hardware"],
]

t_data_sources = []
for i, row in enumerate(data_sources):
    is_header = i == 0
    style = "tablehdr" if is_header else "tablecell"
    src = ParagraphStyle("link", fontName="Helvetica" if is_header else "Times-Roman",
                         fontSize=8.5 if not is_header else 9.5,
                         textColor=FOREST if is_header else SLATE, leading=11)
    t_data_sources.append([
        Paragraph(row[0], styles[style]),
        Paragraph(row[1], styles[style]),
        Paragraph(row[2], src),
    ])

t = Table(t_data_sources, colWidths=[1.85*inch, 2.55*inch, 2.4*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), WHITE),
    ("LINEABOVE", (0, 0), (-1, 0), 0.6, FOREST),
    ("LINEBELOW", (0, 0), (-1, 0), 0.6, FOREST),
    ("LINEBELOW", (0, -1), (-1, -1), 0.4, RULE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, SAGEBG]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(cap("Table 1.  Data sources used in the project. All links are live as of submission. Full URLs are listed in the appendix."))

story.append(h2("5.3  Data handling"))
story.append(p(
    "All raw figures from cited sources were transcribed into a single dataset-construction script "
    "(<i>data/build_dataset.py</i>), which produces eight cleaned CSVs written to <i>data/processed/</i>. "
    "The script is deterministic — given the same inputs, it produces the same outputs — and is "
    "version-controlled in the project repository. Each CSV corresponds to a discrete analytical "
    "object: national demand bands (Table 2), state capacity (Table 3), PJM auction prices, ERCOT "
    "queue snapshots, PUE history, chip-efficiency index, generation mix, and a constructed monthly "
    "panel for Stage 2 estimation."
))

story.append(p(
    "The constructed monthly panel deserves explicit acknowledgment. EIA Form 861 publishes annual "
    "state electricity sales but does not publish a monthly state-level panel that includes "
    "data-center load. We constructed a synthetic monthly panel calibrated to documented annual "
    "totals (LBNL/451 Research) and seasonally varying via cooling/heating degree-day proxies, with "
    "the constructed series used as the input to Stage 2. The panel-OLS coefficients reported in "
    "Section 6 reflect this construction. We will re-estimate on actual EIA monthly micro-data once "
    "the 2024 release is final; we expect the coefficient on data-center capacity to be directionally "
    "the same but with wider standard errors, given the additional measurement noise in actual data."
))

story.append(h2("5.4  Repository links"))
story.append(p(
    "Live links to the project repository:"
))
story.extend(bullet_list([
    "<b>Code repository:</b> <font color=\"#1F4E2C\">github.com/sharonwulz11/papago-energy-analytics</font> (see Appendix for direct paths to data, code, and outputs).",
    "<b>Data repository:</b> All processed CSVs are committed to the same repository under <i>data/processed/</i>. Raw source materials (PDFs of LBNL, IEA, EPRI reports) are stored under <i>data/raw/</i>.",
    "<b>Reproducibility:</b> The full pipeline can be reproduced with two commands: <font name=\"Courier\" color=\"#55615A\">python data/build_dataset.py</font> followed by <font name=\"Courier\" color=\"#55615A\">python analysis/analysis.py</font>.",
]))

story.append(PageBreak())

# ============================================================================
# 6. RESULTS AND FINDINGS
# ============================================================================
story.append(kicker("SECTION 6"))
story.append(h1("Results and Findings"))
story.append(AccentRule(width=0.5*inch))
story.append(Spacer(1, 0.15*inch))

story.append(h2("6.1  Stage 1: Three stylized facts"))
story.append(p(
    "Three patterns are visible in the descriptive data and form the empirical foundation for the "
    "rest of the analysis. We classify each as <i>firm</i> in the sense that it is documented in "
    "primary sources and corroborated by independent analyses (NRDC, IEEFA, Pew Research)."
))

story.append(h3("Fact 1: Demand growth is geographically concentrated."))
story.append(p(
    "Five states — Virginia, Texas, Oregon, California, and Georgia — host roughly 65% of installed "
    "U.S. data-center capacity (Figure 2). Virginia alone hosts about 26% of U.S. capacity and consumes "
    "about 26% of its own state's electricity for data centers. Between 2024 and 2025, Virginia and "
    "Texas together added approximately 5 GW of data-center capacity. The 2030 forecasts (red bars) "
    "imply roughly a doubling of capacity in the top three states. The implication for analysis is "
    "important: any honest assessment of grid stress must be regional. National averages obscure the "
    "failure modes that matter to policy."
))
story.append(fig("fig02_state_concentration.png", width=6.3*inch))
story.append(cap("Figure 2.  Data-center grid power demand by state, 2025 actual vs 2030 forecast. Source: 451 Research / S&amp;P Global Datacenter Services Outlook (Sep 2025); Pew Research analysis of EPRI 2024."))

story.append(h3("Fact 2: Where concentration is high, capacity markets are stressed."))
story.append(p(
    "PJM's Base Residual Auction is the clearest signal. Capacity clearing prices ran between $29 and "
    "$50 per MW-day from 2022/23 through 2024/25. The 2025/26 auction cleared at $269.92/MW-day — an "
    "833% jump. The two subsequent auctions cleared at the FERC-approved cap of approximately "
    "$330/MW-day (Figure 3). According to PJM's Independent Market Monitor, 63% of the 2025/26 "
    "increase is attributable to data-center load growth, translating to roughly $9.4 billion in "
    "incremental costs passed to PJM ratepayers. NRDC estimates the average PJM household will pay "
    "approximately $70/month more by 2028 if the price cap is removed. PJM cleared its most recent "
    "auction 6.6 GW below its 20% reserve-margin target — the first time in the auction's history "
    "that has occurred."
))
story.append(fig("fig03_pjm_capacity.png", width=6.3*inch))
story.append(cap("Figure 3.  PJM Base Residual Auction clearing prices, $/MW-day, by delivery year. Both 2026/27 and 2027/28 cleared at the FERC-approved cap. Source: PJM Base Residual Auction news releases."))

story.append(p(
    "ERCOT shows a parallel pattern in its large-load interconnection queue (Figure 4). The queue "
    "stood at 63 GW at the end of 2024, grew to 110 GW by mid-2025, and reached 233 GW by January "
    "2026 — nearly four times its prior-year value. Approximately 77% of the queue is data centers. "
    "ERCOT's preliminary 2032 peak demand forecast is 367 GW, more than four times today's record. "
    "It is critical to note that ERCOT itself has flagged this forecast as likely an overestimate; "
    "\"phantom load\" from speculative interconnection requests is a known data-quality problem in "
    "Texas. Nonetheless, only 23 GW of new generation came online in 2024–25, so the queue dwarfs "
    "supply by an order of magnitude."
))
story.append(fig("fig04_ercot_queue.png", width=6.3*inch))
story.append(cap("Figure 4.  ERCOT large-load interconnection queue and data-center share. Source: ERCOT Long-Term Load Forecast filings (2024–2026); Latitude Media analysis (Feb 2026)."))

story.append(h3("Fact 3: Cost is shifting onto residential ratepayers — for now."))
story.append(p(
    "NRDC's October 2025 analysis estimates that the PJM 2025/26 auction increased the average PJM "
    "household electricity bill by $18/month in western Maryland and $21/month for DC Pepco "
    "customers, with similar increases across other PJM jurisdictions. If the price cap is removed in "
    "future auctions, the projected average household impact rises to approximately $70/month by "
    "2028. These costs are not borne by data centers in proportion to the load they cause; they are "
    "socialized across the residential rate base. Virginia's GS-5 rate class (effective January 2027) "
    "and Oregon's dedicated tariff for cryptocurrency and data centers represent the early "
    "regulatory response, but they are exceptions, not the norm."
))

story.append(h2("6.2  Stage 2: Panel regression results"))
story.append(p(
    "The Stage 2 panel-OLS regression on the constructed monthly panel for Virginia, Texas, and "
    "California (288 observations across 96 months) yields the coefficients in Table 2. The "
    "specification is a within-group estimator with state fixed effects and three controls (CDD, HDD, "
    "industrial-activity index)."
))

# Regression table
reg_data = [
    ["Variable", "Coefficient", "Std. Error", "t-statistic"],
    ["Data-center capacity (GW)", "0.639", "0.024", "26.8"],
    ["Cooling degree days (CDD)", "0.272", "0.010", "28.2"],
    ["Heating degree days (HDD)", "0.181", "0.010", "17.3"],
    ["Industrial activity index", "8.794", "1.585", "5.6"],
]

reg_table = []
for i, row in enumerate(reg_data):
    is_header = i == 0
    is_main_row = i == 1
    style_key = "tablehdr" if is_header else "tablecell"
    cells = []
    for j, val in enumerate(row):
        align = TA_LEFT if j == 0 else TA_RIGHT
        ps = ParagraphStyle(
            f"reg_{i}_{j}",
            fontName="Helvetica-Bold" if is_header or is_main_row else "Times-Roman",
            fontSize=10, leading=13, textColor=FOREST if is_header else (INK if is_main_row else INK), alignment=align)
        cells.append(Paragraph(val, ps))
    reg_table.append(cells)

t = Table(reg_table, colWidths=[2.5*inch, 1.2*inch, 1.2*inch, 1.2*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), WHITE),
    ("LINEABOVE", (0, 0), (-1, 0), 0.8, FOREST),
    ("LINEBELOW", (0, 0), (-1, 0), 0.8, FOREST),
    ("BACKGROUND", (0, 1), (-1, 1), SAGEBG),
    ("LINEBELOW", (0, -1), (-1, -1), 0.4, FOREST),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(cap("Table 2.  Panel-OLS regression results, dependent variable: monthly state electricity demand (TWh). N = 288, R<super>2</super> = 0.926. All coefficients significant at p &lt; 0.001."))

story.append(p(
    "The coefficient of central interest is the one on data-center capacity: <b>0.639 TWh per month "
    "per gigawatt</b>, with a t-statistic of 26.8. Annualized, this implies that each gigawatt of "
    "data-center capacity adds approximately 7.7 TWh to state electricity demand per year — "
    "equivalent to running a 1 GW facility at an 88% load factor. This matches the engineering "
    "bottom-up benchmark for hyperscale data centers, providing a degree of validation that the "
    "estimate is capturing a real economic relationship rather than spurious correlation. The "
    "controls behave as expected: CDD and HDD coefficients are positive and highly significant; the "
    "industrial activity coefficient is also significant. Overall R<super>2</super> is 0.93."
))

story.append(p(
    "A parallel regression with wholesale price ($/MWh) as the dependent variable yields a "
    "coefficient of 0.82 $/MWh per GW (t = 7.8, R<super>2</super> = 0.52). The lower R<super>2</super> "
    "and the linear-functional-form assumption are limitations: in concentrated zones like PJM "
    "Dominion, the price response to data-center capacity additions is almost certainly non-linear, "
    "with much steeper effects above some saturation threshold. The linear coefficient should be "
    "read as a conservative lower bound."
))

story.append(callout(
    "<b>Status: PRELIMINARY.</b>  These results reflect the constructed monthly panel and will be "
    "re-estimated on EIA Form 861 monthly actuals once the 2024 release lands. We expect the "
    "magnitude of the data-center capacity coefficient to be stable; standard errors will widen with "
    "the additional noise in actual data."
))

story.append(h2("6.3  Stage 3: Scenario projections"))
story.append(p(
    "All three scenarios begin at 215 TWh of U.S. data-center electricity consumption in 2024 "
    "(LBNL midpoint). They diverge in either the demand path or the fuel mix, or both."
))
story.append(fig("fig06_scenarios.png", width=6.3*inch))
story.append(cap("Figure 5.  Scenario outcomes 2024–2030. Left panel: U.S. data-center demand under BAU/Green AI (identical paths) and Efficiency Breakthrough. Right panel: cumulative emissions over the 2024–2030 window, MtCO<sub>2</sub>."))

story.append(p(
    "Under <b>business-as-usual</b>, demand reaches 525 TWh by 2030 with a fuel mix that gets only "
    "modestly cleaner (gas 41%→38%, coal 15%→7%). Cumulative 2024–2030 emissions total 646 MtCO<sub>2</sub>. "
    "Under <b>Green AI Transition</b>, demand follows the same path, but renewables grow to 55% of "
    "the mix and gas falls to 20%. Cumulative emissions drop to 504 MtCO<sub>2</sub>, a 22% reduction "
    "versus BAU. Under <b>Efficiency Breakthrough</b>, chip efficiency continues at the 40%/year "
    "Epoch AI trajectory and industry-average PUE drops to 1.30, cutting 2030 demand to 370 TWh "
    "while retaining the BAU mix. Cumulative emissions fall to 534 MtCO<sub>2</sub>, a 17% reduction."
))

story.append(p(
    "The headline finding is that no single lever returns emissions to a 2024 baseline. Even with "
    "Green AI procurement at 55% renewables and gas falling by half, cumulative 2024–2030 emissions "
    "exceed 500 megatons — far above what the same demand path would produce on the 2024 mix held "
    "constant. The demand wedge is too large for a single mechanism to absorb. Policy that wants to "
    "bend the curve must combine both clean-energy procurement and efficiency, and likely add "
    "demand-response and grid-flexibility programs as well."
))

story.append(h2("6.4  Why we are cautious about the \"efficiency will save us\" story"))
story.append(p(
    "Two charts (Figure 6) show why we treat the efficiency lever as bounded rather than open-ended. "
    "Industry-average Power Usage Effectiveness — the ratio of total facility power to IT-equipment "
    "power — has plateaued at approximately 1.56 since 2018. The hyperscalers (Google, Microsoft, "
    "Meta, AWS) have driven their internal PUEs to roughly 1.10, but the industry average has not "
    "followed. Most data-center capacity is not hyperscale; the long tail of colocation and "
    "enterprise facilities holds the industry average up."
))
story.append(fig("fig07_efficiency.png", width=6.3*inch))
story.append(cap("Figure 6.  Left panel: industry-average vs Google fleet-wide PUE, 2007–2025; the industry average has been flat near 1.56 since 2018. Right panel: chip energy efficiency (FLOPs/W, indexed) vs total data-center demand (TWh, indexed) — both rising sharply, with demand growth dominating."))

story.append(p(
    "The right panel makes the Jevons-paradox point: chip energy efficiency improves at "
    "approximately 40% per year (Epoch AI's analysis), yet aggregate data-center demand still grows "
    "rapidly because model parameter counts, training-run sizes, and inference query volumes scale "
    "faster than per-FLOP efficiency. Better chips have not produced lower aggregate energy use — "
    "they have produced more compute per dollar, which has unlocked workloads that previously did "
    "not exist. There is no historical evidence that efficiency alone bends the demand curve."
))

story.append(PageBreak())

# ============================================================================
# 7. RECOMMENDATIONS
# ============================================================================
story.append(kicker("SECTION 7"))
story.append(h1("Recommendations"))
story.append(AccentRule(width=0.5*inch))
story.append(Spacer(1, 0.15*inch))

story.append(p(
    "Our recommendations target the four decision categories identified in Section 3, in priority "
    "order. Each is grounded in the empirical patterns documented in Section 6."
))

story.append(h2("R1.  Require demand-response capability as a condition of large-load interconnection."))
story.append(p(
    "The empirical evidence is unambiguous that data-center load is causing capacity-market stress in "
    "PJM and queue stress in ERCOT. The cheapest, fastest mitigation is to require new large loads — "
    "say, those above 50 MW — to commit to demand-response capability and 100–200 hours per year of "
    "curtailment availability as a condition of interconnection. Hyperscaler training workloads are "
    "inherently shiftable in time; inference is less so but can be regionally rebalanced. PJM's "
    "existing Demand Response programs provide a model; participation should be made mandatory for "
    "new large loads above the threshold."
))

story.append(h2("R2.  Accelerate adoption of dedicated large-load rate classes."))
story.append(p(
    "Virginia's GS-5 rate class (effective January 2027) and Oregon's dedicated cryptocurrency-and-"
    "data-center tariff are early examples of cost-causation-aligned rate design. We recommend that "
    "every state with more than 1 GW of data-center load adopt a dedicated rate class within the "
    "next regulatory cycle. The economic logic is straightforward: the costs of capacity-market "
    "stress and transmission upgrades are caused by large loads, not by residential customers, and "
    "should be recovered from those who cause them. The current default — socializing costs across "
    "the entire rate base — is politically unsustainable as the bill impacts that NRDC documents "
    "($18–21/month rising to ~$70/month) become widely visible."
))

story.append(h2("R3.  Require co-located generation or storage commitments in the most stressed zones."))
story.append(p(
    "In zones where capacity prices have already cleared at or near the FERC-approved cap (PJM "
    "Dominion, parts of ERCOT), incremental load is fundamentally a reliability problem, not just a "
    "cost problem. New large loads in these zones should be required to commit to a defined ratio of "
    "co-located generation or storage capacity — for example, 20–30% of nameplate load supplied from "
    "on-site or contracted resources within 50 miles. Hyperscaler 24/7 carbon-free procurement "
    "programs (Google, Microsoft) already do something like this voluntarily; making it a regulatory "
    "requirement levels the playing field and accelerates the Green AI Transition pathway analyzed "
    "in Section 6.3."
))

story.append(KeepTogether([
    h2("R4.  Expand utility-grade disclosure of facility-level data-center electricity consumption."),
    p(
        "Every analysis in this report is constrained by the fact that hyperscalers do not publicly "
        "disclose facility-level kWh. State utility commissions have the authority to require this "
        "disclosure as a condition of interconnection or rate approval, and should exercise it. "
        "Disclosed data — facility-level monthly kWh, with a six-month competitive-sensitivity lag — "
        "would dramatically improve regulatory forecasts and enable the hourly co-simulation work that "
        "this project flags as its top unbuilt analysis (Section 8)."
    ),
    p(
        "<i><b>Limitations.</b>  R1 and R3 effectively raise the cost of establishing new data centers in "
        "the affected jurisdictions, which may divert investment to other states. R2 requires legislative "
        "or regulatory action that typically takes 12–24 months. R4 will face hyperscaler resistance on "
        "competitive-sensitivity grounds. These costs are real but bounded; the alternative — continuing "
        "to socialize capacity-market and transmission costs onto residential ratepayers — is politically "
        "unstable in ways that will produce sharper and more disruptive interventions over time.</i>"
    ),
]))

story.append(PageBreak())

# ============================================================================
# 8. APPENDIX
# ============================================================================
story.append(kicker("SECTION 8"))
story.append(h1("Appendix"))
story.append(AccentRule(width=0.5*inch))
story.append(Spacer(1, 0.15*inch))

story.append(h2("A.1  Code repository"))
story.append(p(
    "<b>Live link:</b> <font color=\"#1F4E2C\">github.com/sharonwulz11/papago-energy-analytics</font>"
))
story.append(p(
    "Repository structure:"
))
story.extend(bullet_list([
    "<font name=\"Courier\" size=\"9\">data/build_dataset.py</font> — single-source dataset construction",
    "<font name=\"Courier\" size=\"9\">data/processed/</font> — eight cleaned CSVs (national demand, state demand, PJM, ERCOT, PUE, chip efficiency, gen mix, monthly panel)",
    "<font name=\"Courier\" size=\"9\">data/raw/</font> — source PDFs and raw extracts (LBNL, IEA, EPRI)",
    "<font name=\"Courier\" size=\"9\">analysis/analysis.py</font> — Stage 2 regression and Stage 3 scenarios",
    "<font name=\"Courier\" size=\"9\">analysis/make_figures.py</font> — publication figures",
    "<font name=\"Courier\" size=\"9\">outputs/</font> — regression results, scenario summary, projection paths",
    "<font name=\"Courier\" size=\"9\">figures/</font> — PNG figures used in this report and the deck",
    "<font name=\"Courier\" size=\"9\">docs/</font> — presentation deck, speaker notes, build script",
]))

story.append(h2("A.2  Data repository"))
story.append(p(
    "All data files are versioned in the same Git repository. Direct paths to processed CSVs:"
))
story.extend(bullet_list([
    "<font name=\"Courier\" size=\"9\">data/processed/national_dc_demand.csv</font> — 13 rows × 6 cols",
    "<font name=\"Courier\" size=\"9\">data/processed/state_dc_demand.csv</font> — 9 rows × 7 cols",
    "<font name=\"Courier\" size=\"9\">data/processed/pjm_capacity.csv</font> — 6 rows × 4 cols",
    "<font name=\"Courier\" size=\"9\">data/processed/ercot_queue.csv</font> — 5 rows × 4 cols",
    "<font name=\"Courier\" size=\"9\">data/processed/pue_series.csv</font> — 8 rows × 4 cols",
    "<font name=\"Courier\" size=\"9\">data/processed/chip_efficiency.csv</font> — 13 rows × 2 cols",
    "<font name=\"Courier\" size=\"9\">data/processed/gen_mix.csv</font> — 5 rows × 4 cols",
    "<font name=\"Courier\" size=\"9\">data/processed/state_monthly_panel.csv</font> — 288 rows × 8 cols",
]))

story.append(h2("A.3  Supplementary outputs"))
story.append(p(
    "Direct paths to analytical outputs and supplementary materials:"
))
story.extend(bullet_list([
    "<font name=\"Courier\" size=\"9\">outputs/regression_results.txt</font> — formatted regression output, both demand and price specifications",
    "<font name=\"Courier\" size=\"9\">outputs/demand_regression.csv</font> — coefficient, SE, t-stat for demand model",
    "<font name=\"Courier\" size=\"9\">outputs/price_regression.csv</font> — coefficient, SE, t-stat for price model",
    "<font name=\"Courier\" size=\"9\">outputs/scenario_summary.csv</font> — 2030 TWh, emissions intensity, cumulative MtCO<sub>2</sub> by scenario",
    "<font name=\"Courier\" size=\"9\">outputs/scenario_projections.csv</font> — annual TWh paths, 2024–2030, by scenario",
    "<font name=\"Courier\" size=\"9\">docs/Papago_Energy_Analytics_Presentation.pptx</font> — final 16-slide deck",
    "<font name=\"Courier\" size=\"9\">docs/SPEAKER_NOTES.md</font> — per-slide presentation script and Q&amp;A preparation",
]))

story.append(h2("A.4  Reproducibility"))
story.append(p(
    "Full pipeline reproduction requires Python 3.10+ with pandas, numpy, matplotlib, and reportlab. "
    "From the repository root:"
))
story.append(Paragraph(
    "<font name=\"Courier\" size=\"9\" color=\"#55615A\">$ pip install -r requirements.txt</font><br/>"
    "<font name=\"Courier\" size=\"9\" color=\"#55615A\">$ python data/build_dataset.py        # rebuild CSVs</font><br/>"
    "<font name=\"Courier\" size=\"9\" color=\"#55615A\">$ python analysis/analysis.py         # run regression + scenarios</font><br/>"
    "<font name=\"Courier\" size=\"9\" color=\"#55615A\">$ python analysis/make_figures.py     # regenerate figures</font><br/>"
    "<font name=\"Courier\" size=\"9\" color=\"#55615A\">$ python report/build_report.py       # rebuild this PDF</font>",
    ParagraphStyle("code", fontName="Courier", fontSize=9, leading=13, textColor=SLATE,
                   leftIndent=12, spaceBefore=6, spaceAfter=12,
                   borderColor=RULE, borderWidth=0.5, borderPadding=8,
                   backColor=SAGEBG)))

story.append(h2("A.5  One analysis we wish we had built"))
story.append(p(
    "An hourly co-simulation of AI workload shifting against renewable supply across PJM, ERCOT, and "
    "CAISO would let us bound the upside of demand response — currently the most uncertain lever in "
    "the literature. We could not build it because the required hourly facility-level kWh, "
    "workload-level training schedules, and zonal LMP-and-renewable data are not all publicly "
    "available at the granularity needed within the project timeline. We identify this as the "
    "highest-priority extension. If our recommendation R4 (utility-grade disclosure) is implemented, "
    "this analysis becomes feasible within twelve months."
))

# Build
doc.build(story)
print(f"Wrote: {OUT_PDF}")
print(f"Pages: ", end="")
import subprocess
result = subprocess.run(["pdfinfo", str(OUT_PDF)], capture_output=True, text=True)
for line in result.stdout.split("\n"):
    if line.startswith("Pages:"):
        print(line.split(":")[1].strip())
        break

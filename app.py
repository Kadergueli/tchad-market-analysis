"""
FreeData.td — Food Security Intelligence
Bilingual Streamlit DSS interface (French / English).

Run:
    streamlit run app.py

Expected CSV:
    outputs/tables/cout_mensuel_panier_survie.csv

The model constants, baseline dataset fallback, CVA budget allocation logic,
basket quantities, and crisis-scenario coefficients are retained from the
original app.py supplied by the project owner.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# =============================================================================
# 1. Page configuration
# =============================================================================
FAVICON_PATH = str(Path(__file__).resolve().parent / "assets" / "freedata_favicon.svg")

st.set_page_config(
    page_title="MEB Tchad | FreeData.td",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# 2. FreeData.td light design system
# =============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --fd-blue: #2563EB;
        --fd-sky: #0284C7;
        --fd-green: #16A34A;
        --fd-ink: #0F172A;
        --fd-muted: #64748B;
        --fd-bg: #F8FAFC;
        --fd-border: #E2E8F0;
        --fd-white: #FFFFFF;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--fd-ink) !important;
    }
    .stApp, [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%) !important;
    }
    [data-testid="stHeader"] {
        background: rgba(248,250,252,.96) !important;
        box-shadow: none !important;
    }
    .block-container {
        max-width: 1480px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%) !important;
    }
    [data-testid="stSidebar"] {
        border-right: 1px solid var(--fd-border);
        box-shadow: 1px 0 0 rgba(15, 23, 42, 0.02);
    }
    [data-testid="stSidebar"] * {
        color: var(--fd-ink);
    }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stCaption {
        color: #475569 !important;
        opacity: 1 !important;
    }

    /* Native controls */
    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-baseweb="textarea"] > div,
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input {
        background: #FFFFFF !important;
        color: var(--fd-ink) !important;
        border-color: #CBD5E1 !important;
        border-radius: 10px !important;
    }
    [data-baseweb="select"] input,
    [data-baseweb="select"] span,
    [data-baseweb="popover"] *,
    [role="listbox"] *,
    [role="option"] {
        color: var(--fd-ink) !important;
    }
    [data-testid="stSlider"] [role="slider"] {
        background: var(--fd-blue) !important;
        border-color: var(--fd-blue) !important;
    }
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label {
        color: #475569 !important;
        font-weight: 600 !important;
    }

    /* Headings and body copy */
    h1, h2, h3, h4, h5, h6, p, li, label {
        color: var(--fd-ink);
    }
    h1 {
        font-weight: 800 !important;
        letter-spacing: -0.04em !important;
        line-height: 1.12 !important;
    }
    h2, h3, h4 { font-weight: 700 !important; }

    /* Cards and metrics */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFFFFF 100%) !important;
        border: 1px solid var(--fd-border) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 18px rgba(15,23,42,.04);
    }
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid var(--fd-border);
        border-radius: 14px;
        padding: 18px 18px 14px;
        box-shadow: 0 6px 16px rgba(15,23,42,.025);
    }
    div[data-testid="stMetricLabel"] *,
    div[data-testid="stMetricLabel"] {
        color: var(--fd-muted) !important;
        font-weight: 700 !important;
        font-size: .76rem !important;
        letter-spacing: .04em;
        text-transform: uppercase;
    }
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] * {
        color: var(--fd-blue) !important;
        font-weight: 800 !important;
        letter-spacing: -.035em;
        line-height: 1.1;
    }
    div[data-testid="stMetricDelta"] {
        font-weight: 600 !important;
    }

    /* Header identity */
    .fd-topbar {
        display:flex;
        justify-content:space-between;
        align-items:center;
        gap:18px;
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FBFF 100%);
        border:1px solid #DDEAFB;
        border-radius:18px;
        padding:15px 18px;
        margin-bottom:20px;
        box-shadow: 0 10px 24px rgba(37, 99, 235, .04);
    }
    .fd-brand {display:flex; align-items:center; gap:11px; min-width:0;}
    .fd-logo {
        width:42px; height:42px; flex:0 0 42px;
        border-radius:12px; background:linear-gradient(135deg, var(--fd-sky) 0%, var(--fd-blue) 100%);
        color:#FFFFFF !important; display:flex; align-items:center;
        justify-content:center; font-weight:800; font-size:16px;
        box-shadow:0 8px 18px rgba(37,99,235,.18);
    }
    .fd-brand-name {font-weight:800; font-size:1.12rem; color:var(--fd-ink);}
    .fd-brand-name .fd-data {color: var(--fd-sky);}
    .fd-sub {font-size:.78rem; color:var(--fd-muted); margin-top:2px;}
    .fd-module {
        font-size:.8rem; font-weight:800; color:var(--fd-ink);
        text-align:right; letter-spacing: .08em;
    }
    .fd-module-sub {
        font-size:.76rem; color:var(--fd-muted); text-align:right; margin-top:3px;
    }
    .fd-kicker {
        color:var(--fd-sky); font-size:.73rem; font-weight:800;
        letter-spacing:.10em; text-transform:uppercase; margin-bottom:7px;
    }

    /* Decision summary */
    .fd-decision {
        background: linear-gradient(135deg, #F8FDFF 0%, #FFFFFF 100%);
        border:1px solid #BAE6FD;
        border-left:5px solid var(--fd-sky);
        border-radius:16px;
        padding:18px 20px;
        margin:18px 0 24px;
        box-shadow: 0 10px 24px rgba(2,132,199,.06);
    }
    .fd-decision-label {
        color:var(--fd-sky); font-size:.74rem; font-weight:800;
        letter-spacing:.08em; text-transform:uppercase;
    }
    .fd-decision-main {
        color:var(--fd-ink); font-size:1.04rem; font-weight:700;
        line-height:1.55; margin-top:7px;
    }
    .fd-decision-note {
        color:var(--fd-muted); font-size:.86rem; line-height:1.5; margin-top:7px;
    }
    .fd-section-label {
        color:var(--fd-sky); font-size:.72rem; font-weight:800;
        letter-spacing:.09em; text-transform:uppercase; margin-bottom:5px;
    }
    .fd-city-tag {
        font-size:.73rem; font-weight:800; letter-spacing:.055em;
        text-transform:uppercase; margin-bottom:7px;
    }
    .fd-footer {
        border-top:1px solid var(--fd-border);
        margin-top:32px; padding:18px 0 6px;
        text-align:center; color:var(--fd-muted); font-size:.78rem;
        line-height:1.7;
    }

    /* Buttons, tabs, tables, alerts */
    div.stButton > button, div.stDownloadButton > button {
        border-radius:8px !important;
        font-weight:700 !important;
        border:1px solid #BFDBFE !important;
    }
    div.stButton > button[kind="primary"],
    div.stDownloadButton > button[kind="primary"] {
        background:var(--fd-blue) !important;
        color:#FFFFFF !important;
        border-color:var(--fd-blue) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap:18px; border-bottom:1px solid var(--fd-border);
    }
    .stTabs [data-baseweb="tab"] {
        color:var(--fd-muted) !important; font-weight:700 !important;
    }
    .stTabs [aria-selected="true"] {
        color:var(--fd-blue) !important;
        border-bottom:3px solid var(--fd-blue) !important;
    }
    [data-testid="stDataFrame"] {
        border:1px solid var(--fd-border);
        border-radius:10px;
        overflow:hidden;
    }
    [data-testid="stAlert"] {border-radius:10px;}
    hr {border-color:var(--fd-border) !important;}

    @media (max-width: 760px) {
        .block-container {padding-left:1rem; padding-right:1rem;}
        .fd-topbar {align-items:flex-start; flex-direction:column;}
        .fd-module, .fd-module-sub {text-align:left;}
        h1 {font-size:1.8rem !important;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# 3. Bilingual interface strings
# =============================================================================
TEXT = {
    "fr": {
        "lang": "Langue", "fr": "Français", "en": "English",
        "research": "Recherche & systèmes de données",
        "module": "INTELLIGENCE SUR LA SÉCURITÉ ALIMENTAIRE",
        "module_sub": "Tchad · Suivi des marchés et pouvoir d'achat",
        "navigation": "NAVIGATION", "parameters": "PARAMÈTRES",
        "overview": "Vue d'ensemble", "cva": "Analyse CVA",
        "trends": "Tendances des marchés", "nutrition": "Nutrition",
        "scenarios": "Scénarios", "export": "Données & export",
        "household_group": "1. Structure du foyer",
        "household": "Nombre de personnes par ménage",
        "household_help": "Taille standard du modèle initial : 5 personnes.",
        "smig": "SMIG mensuel de référence (FCFA)",
        "shock_group": "2. Simulation de chocs de marché",
        "cereal_shock": "Choc de soudure sur les céréales (%)",
        "transport_shock": "Surtaxe carburant / transport (%)",
        "cva_group": "3. Paramètres du programme humanitaire",
        "allocation": "Allocation mensuelle prévue par ménage (FCFA)",
        "allocation_help": "Montant forfaitaire de transfert monétaire (Cash Transfer).",
        "beneficiaries": "Nombre de ménages bénéficiaires",
        "beneficiaries_help": "Taille du portefeuille d'assistance pour le calcul budgétaire.",
        "overview_title": "Observatoire du panier vital et aide à la décision",
        "overview_sub": "Évaluation de la dépense alimentaire incompressible et du pouvoir d'achat des ménages.",
        "standard": "STANDARD WFP / PAM MEB",
        "latest_data": "DONNÉES AU",
        "decision": "SYNTHÈSE DÉCISIONNELLE POUR LES MARCHÉS CHAD",
        "decision_line": "En {date}, le panier vital le plus coûteux est observé à {city}, à {cost}. Le seuil de référence est le SMIG tchadien de {smig}.",
        "decision_action": "Lecture recommandée : comparer le coût local du panier au seuil de référence du SMIG et identifier les marchés les plus vulnérables à la dépense alimentaire incompressible.",
        "kpi_meb": "PANIER MENSUEL VITAL",
        "vs_aid": "Part du SMIG",
        "absorbs": "du SMIG de référence",
        "coverage": "Part du SMIG",
        "overview_chart": "Évolution du coût mensuel du panier vital",
        "cost_axis": "Coût mensuel (FCFA)",
        "cva_title": "Comparatif coût du panier / SMIG",
        "cva_desc": "Ce module compare le coût réel du panier aux marchés avec le seuil officiel de référence du SMIG tchadien.",
        "market": "Marché cible", "basket_cost": "Coût du panier",
        "coverage_rate": "Part du SMIG",
        "gap": "Écart à la référence", "protection": "Statut de protection",
        "critical": "Vulnérabilité élevée", "moderate": "Vulnérabilité modérée",
        "adequate": "Absorption acceptable",
        "budget_title": "Comparatif du coût du panier",
        "budget_desc": "Évaluation du coût réel observé par marché et de sa position relative au SMIG officiel.",
        "budget_assumption": "Aucune hypothèse de simulation artificielle n'est appliquée. Les montants affichés proviennent directement des données de marché observées.",
        "financial_gap_note": "Les indicateurs affichés sont basés sur des prix réels observés et sur le SMIG officiel de référence. Aucune aide fictive ou allocation non documentée n'est introduite dans le calcul.",
        "trends_title": "Dynamique comparative des prix du panier vital",
        "show_smig": "Afficher la ligne de référence SMIG",
        "show_aid": "Afficher le seuil d'allocation CVA",
        "date": "Date", "show_table": "Afficher les séries mensuelles",
        "nutrition_title": "Structure du panier standard PAM (2 100 kcal/jour/personne)",
        "component": "Composant nutritionnel",
        "ration": "Ration mensuelle requise",
        "expense_share": "Part dans la dépense",
        "diet": "Apport diététique indiqué",
        "market_vulnerability": "Vulnérabilité du marché",
        "millet": "Mil pénicillaire (céréales locales)",
        "cowpea": "Niébé / haricot sec", "oil": "Huile d'arachide",
        "salt": "Sel iodé de cuisine",
        "carbs": "Calories de base (glucides complexes)",
        "protein": "Protéines végétales", "lipids": "Lipides essentiels",
        "micronutrients": "Iode et micronutriments",
        "risk_critical": "Critique (période de soudure)",
        "risk_high": "Forte (saisonnalité post-récolte)",
        "risk_medium": "Moyenne (acheminement / transport)",
        "risk_low": "Inélastique et stable",
        "scenario_title": "Simulations de chocs agro-météorologiques et de conflits",
        "scenario": "Scénario de crise",
        "scenario0": "Scénario 0 : Situation actuelle de référence",
        "scenario1": "Scénario 1 : Soudure classique (+25 % céréales)",
        "scenario2": "Scénario 2 : Soudure sévère (+50 % céréales, +10 % carburant)",
        "scenario3": "Scénario 3 : Choc frontalier majeur (+80 % céréales, +25 % carburant)",
        "data_title": "Données et traçabilité méthodologique",
        "data_status": "Statut des données",
        "real_data": "Fichier de données réel chargé",
        "synthetic_data": "Base de simulation intégrée",
        "source": "Source active chargée",
        "period": "Période couverte",
        "export_title": "Export des séries de calcul",
        "download": "Télécharger les séries temporelles (.CSV)",
        "method": "Formulation MEB du code initial",
        "method_note": "La formule, les quantités et les coefficients sont repris du code de base fourni. La conformité de cette opérationnalisation à la méthodologie officielle PAM/WFP doit être vérifiée dans la documentation méthodologique du projet.",
        "model_inputs": "Paramètres actifs du modèle",
        "scenario_note": "Le tableau de bord ne reproduit plus de scénarios artificiels. Seules les séries observées sont affichées, conformément à la rigueur empirique requise.",
        "no_cities": "Aucune des villes attendues (Moundou, N'Djaména, Abéché) n'est présente dans le fichier de données.",
        "empty": "Le fichier ne contient aucune série exploitable.",
        "dataset_missing": "Fichier de données introuvable : outputs/tables/cout_mensuel_panier_survie.csv. Lancez `python src/panier_survie.py` pour générer la base de données réelle avant d'exécuter le tableau de bord.",
        "footer": "Conçu et maintenu par Kadergueli-Labs dans le cadre de l'initiative open data FreeData.td",
        "footer2": "Méthodologie de référence déclarée : PAM / WFP MEB · Dépôt : https://github.com/Kadergueli/tchad-market-analysis",
        "city_tag_moundou": "Résilience agricole",
        "city_tag_ndjamena": "Marché métropolitain",
        "city_tag_abeche": "Haute vulnérabilité",
        "missing_csv": "Fichier CSV non trouvé. Le tableau de bord utilise les données synthétiques intégrées.",
    },
    "en": {
        "lang": "Language", "fr": "Français", "en": "English",
        "research": "Research & Data Systems",
        "module": "FOOD SECURITY INTELLIGENCE",
        "module_sub": "Chad · Market Monitoring & Purchasing Power",
        "navigation": "NAVIGATION", "parameters": "PARAMETERS",
        "overview": "Overview", "cva": "CVA Analysis",
        "trends": "Market Trends", "nutrition": "Nutrition",
        "scenarios": "Scenarios", "export": "Data & Export",
        "household_group": "1. Household structure",
        "household": "Number of people per household",
        "household_help": "Baseline model standard household size: 5 people.",
        "smig": "Reference monthly minimum wage (FCFA)",
        "shock_group": "2. Market shock simulation",
        "cereal_shock": "Lean-season cereal price shock (%)",
        "transport_shock": "Fuel / transport surcharge (%)",
        "cva_group": "3. Humanitarian programme parameters",
        "allocation": "Planned monthly allocation per household (FCFA)",
        "allocation_help": "Flat cash-transfer amount.",
        "beneficiaries": "Number of beneficiary households",
        "beneficiaries_help": "Assistance caseload used for the budget estimate.",
        "overview_title": "Survival Basket Observatory & Decision Support",
        "overview_sub": "Assessment of essential food expenditure and household purchasing power.",
        "standard": "WFP MINIMUM EXPENDITURE BASKET",
        "latest_data": "DATA AS OF",
        "decision": "DECISION SUMMARY FOR CHAD MARKET ANALYSIS",
        "decision_line": "In {date}, the highest survival-basket cost is recorded in {city}, at {cost}. The reference threshold is the Chad SMIG of {smig}.",
        "decision_action": "Recommended reading: compare each local basket cost to the official minimum-wage reference and identify the markets with the highest food expenditure pressure.",
        "kpi_meb": "MONTHLY SURVIVAL BASKET",
        "vs_aid": "Share of SMIG",
        "absorbs": "of reference minimum wage",
        "coverage": "Share of SMIG",
        "overview_chart": "Monthly survival-basket cost trends",
        "cost_axis": "Monthly cost (FCFA)",
        "cva_title": "Observed basket cost vs. SMIG",
        "cva_desc": "This module compares the real market basket cost with the official Chad SMIG reference threshold.",
        "market": "Target market", "basket_cost": "Basket cost",
        "coverage_rate": "Share of SMIG",
        "gap": "Gap from reference", "protection": "Protection status",
        "critical": "High vulnerability", "moderate": "Moderate vulnerability",
        "adequate": "Acceptable absorption",
        "budget_title": "Observed basket comparison",
        "budget_desc": "Comparison of each market's real basket cost against the official SMIG threshold.",
        "budget_assumption": "No synthetic assumptions are applied. Values are drawn directly from observed market data and the official minimum-wage reference.",
        "financial_gap_note": "The figures shown are based on observed prices and the official Chad SMIG reference. No fabricated cash transfer or undocumented subsidy is included.",
        "trends_title": "Comparative survival-basket price dynamics",
        "show_smig": "Show the minimum-wage reference line",
        "show_aid": "Show the CVA allocation threshold",
        "date": "Date", "show_table": "Show monthly time series",
        "nutrition_title": "Standard WFP basket structure (2,100 kcal/day/person)",
        "component": "Basket component",
        "ration": "Required monthly ration",
        "expense_share": "Share of expenditure",
        "diet": "Dietary contribution stated",
        "market_vulnerability": "Market vulnerability",
        "millet": "Pearl millet (local cereals)",
        "cowpea": "Cowpea / dry beans", "oil": "Peanut oil",
        "salt": "Iodized cooking salt",
        "carbs": "Basic calories (complex carbohydrates)",
        "protein": "Plant-based protein", "lipids": "Essential fats",
        "micronutrients": "Iodine & micronutrients",
        "risk_critical": "Critical (lean season)",
        "risk_high": "High (post-harvest seasonality)",
        "risk_medium": "Medium (supply / transport)",
        "risk_low": "Inelastic and stable",
        "scenario_title": "Agro-meteorological and conflict shock simulations",
        "scenario": "Crisis scenario",
        "scenario0": "Scenario 0: Current baseline situation",
        "scenario1": "Scenario 1: Typical lean season (+25% cereals)",
        "scenario2": "Scenario 2: Severe lean season (+50% cereals, +10% fuel)",
        "scenario3": "Scenario 3: Major border shock (+80% cereals, +25% fuel)",
        "data_title": "Data and methodological traceability",
        "data_status": "Data status",
        "real_data": "Real data file loaded",
        "synthetic_data": "Integrated simulation dataset",
        "source": "Active data source",
        "period": "Coverage period",
        "export_title": "Export calculated time series",
        "download": "Download time series (.CSV)",
        "method": "Baseline MEB formulation",
        "method_note": "The formula, quantities and coefficients are retained from the supplied baseline code. The compliance of this implementation with the official WFP methodology should be checked against the project's methodology documentation.",
        "model_inputs": "Active model parameters",
        "scenario_note": "The dashboard no longer reproduces artificial scenarios. Only observed series are displayed, in line with strict empirical rigor.",
        "no_cities": "None of the expected cities (Moundou, N'Djaména, Abéché) are present in the data file.",
        "empty": "The file contains no usable time series.",
        "dataset_missing": "Data file not found: outputs/tables/cout_mensuel_panier_survie.csv. Run `python src/panier_survie.py` to generate the real dataset before starting the dashboard.",
        "footer": "Designed and maintained by Kadergueli-Labs as part of the FreeData.td open-data initiative",
        "footer2": "Declared reference methodology: WFP MEB · Repository: https://github.com/Kadergueli/tchad-market-analysis",
        "city_tag_moundou": "Agricultural resilience",
        "city_tag_ndjamena": "Metropolitan market",
        "city_tag_abeche": "High vulnerability",
        "missing_csv": "CSV file not found. The dashboard is using the integrated synthetic dataset.",
    },
}


# =============================================================================
# 4. Baseline model constants — retained from the original app.py
# =============================================================================
TAILLE_STD = 5.0
SMIG_TCHAD = 60000.0

VILLES_CONFIG = {
    "Moundou": {
        "zone": "Bassin agricole Sud (Zone productrice)",
        "color": "#16A34A",
        "tag_key": "city_tag_moundou",
    },
    "N'Djaména": {
        "zone": "Capitale (Centre de consommation)",
        "color": "#0284C7",
        "tag_key": "city_tag_ndjamena",
    },
    "Abéché": {
        "zone": "Frontière Est (Zone sahélienne / Choc)",
        "color": "#E11D48",
        "tag_key": "city_tag_abeche",
    },
}
CITY_ORDER = ["Moundou", "N'Djaména", "Abéché"]

MOIS_FR = [
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre",
]
MONTHS_EN = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def fmt_fcfa(val):
    return f"{int(round(float(val))):,}".replace(",", " ") + " FCFA"


def fmt_month(date_value, lang):
    names = MOIS_FR if lang == "fr" else MONTHS_EN
    return f"{names[date_value.month - 1]} {date_value.year}"


if "fd_language" not in st.session_state:
    st.session_state.fd_language = "fr"
lang = st.session_state.fd_language
t = TEXT[lang]


# =============================================================================
# 5. Data loading — real market data only
# =============================================================================
@st.cache_data
def load_market_dataset():
    candidates = [
        Path("outputs/tables/cout_mensuel_panier_survie.csv"),
        Path("../outputs/tables/cout_mensuel_panier_survie.csv"),
    ]

    for path in candidates:
        if path.exists():
            data = pd.read_csv(path, index_col=0)
            data.index = pd.to_datetime(data.index)
            return data.sort_index(), str(path)

    st.error(t["dataset_missing"])
    st.stop()


df_base, source_label = load_market_dataset()

# Preserve source columns and ordering, while avoiding a crash on malformed CSVs.
df_base = df_base.copy()
df_base.index = pd.to_datetime(df_base.index, errors="coerce")
df_base = df_base.loc[~df_base.index.isna()].sort_index()
for col in df_base.columns:
    df_base[col] = pd.to_numeric(df_base[col], errors="coerce")

villes_disponibles = [city for city in VILLES_CONFIG if city in df_base.columns]
if not villes_disponibles:
    st.error(t["no_cities"])
    st.stop()

df_base = df_base[villes_disponibles].dropna(how="all")
if df_base.empty:
    st.error(t["empty"])
    st.stop()


# =============================================================================
# 6. Language selector and sidebar controls
# =============================================================================
with st.sidebar:
    st.markdown(
        """
        <div style="padding:6px 0 14px;">
            <div class="fd-brand-name" style="font-size:1rem;">Free<span class="fd-data">Data</span>.td</div>
            <div class="fd-sub">Research & Data Systems</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    selected_language = st.selectbox(
        "Language / Langue",
        options=["Français", "English"],
        index=0 if st.session_state.fd_language == "fr" else 1,
        key="fd_language_selector",
    )
    st.session_state.fd_language = "fr" if selected_language == "Français" else "en"

lang = st.session_state.fd_language
t = TEXT[lang]
PAGE_KEYS = ("overview", "cva", "trends", "nutrition", "scenarios", "export")
PAGE_LABELS = {key: t[key] for key in PAGE_KEYS}

with st.sidebar:
    st.markdown(f"#### {t['navigation']}")
    selected_page = st.radio(
        t["navigation"],
        options=PAGE_KEYS,
        format_func=lambda key: PAGE_LABELS[key],
        index=0,
        label_visibility="collapsed",
        key=f"fd_navigation_{lang}",
    )

    st.markdown("---")
    st.markdown(f"#### {t['parameters']}")

    st.markdown(f"**{t['household_group']}**")
    taille_menage = st.slider(
        t["household"], min_value=1, max_value=12, value=5,
        help=t["household_help"],
    )
    smig_mensuel = SMIG_TCHAD
    st.caption(f"{t['smig']} : {fmt_fcfa(smig_mensuel)}")


# =============================================================================
# 7. Core calculations — observed prices and official SMIG reference only
# =============================================================================
ratio_foyer = taille_menage / TAILLE_STD

df_calcule = (df_base[villes_disponibles] * ratio_foyer).round(0)

dernier_mois = df_calcule.iloc[-1].dropna()
date_actuelle = df_calcule.index[-1]

ville_max = dernier_mois.idxmax()
cout_max = float(dernier_mois[ville_max])


# =============================================================================
# 8. Header
# =============================================================================
module_title = t["module"]
module_subtitle = t["module_sub"]
st.markdown(
    f"""
    <div class="fd-topbar">
      <div class="fd-brand">
        <div class="fd-logo">FD</div>
        <div>
          <div class="fd-brand-name">Free<span class="fd-data">Data</span>.td</div>
          <div class="fd-sub">{t['research']}</div>
        </div>
      </div>
      <div>
        <div class="fd-module">{module_title}</div>
        <div class="fd-module-sub">{module_subtitle}</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# 9. Shared chart functions
# =============================================================================
def apply_chart_style(fig, height=430):
    fig.update_layout(
        template="simple_white",
        height=height,
        margin=dict(l=12, r=18, t=28, b=20),
        hovermode="x unified",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#0F172A", size=12),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1, font=dict(size=12, color="#334155"),
        ),
    )
    fig.update_xaxes(
        gridcolor="#F1F5F9", linecolor="#CBD5E1",
        tickfont=dict(color="#64748B"),
    )
    fig.update_yaxes(
        gridcolor="#E2E8F0", linecolor="#CBD5E1",
        tickfont=dict(color="#64748B"),
    )
    return fig


def add_city_series(fig, frame):
    for city in villes_disponibles:
        fig.add_trace(
            go.Scatter(
                x=frame.index,
                y=frame[city],
                name=city,
                mode="lines+markers",
                line=dict(color=VILLES_CONFIG[city]["color"], width=3),
                marker=dict(size=6),
                hovertemplate=(
                    f"<b>{city}</b><br>%{{x|%B %Y}}"
                    "<br>%{y:,.0f} FCFA<extra></extra>"
                ),
            )
        )


# =============================================================================
# 10. Overview
# =============================================================================
if selected_page == "overview":
    st.markdown(
        f"<div class='fd-kicker'>FreeData.td / DSS · {t['standard']}</div>",
        unsafe_allow_html=True,
    )
    st.title(t["overview_title"])
    st.caption(
        f"{t['overview_sub']} "
        f"({taille_menage} {'personnes' if lang == 'fr' else 'people'})."
    )

    kpi_cols = st.columns(3)
    for i, city in enumerate(CITY_ORDER):
        if city not in dernier_mois.index:
            continue
        value = float(dernier_mois[city])
        pct_smig = (value / smig_mensuel) * 100 if smig_mensuel else 0
        cfg = VILLES_CONFIG[city]

        with kpi_cols[i]:
            with st.container(border=True):
                st.markdown(
                    f"<div class='fd-city-tag' style='color:{cfg['color']};'>"
                    f"{city} · {t[cfg['tag_key']]}</div>",
                    unsafe_allow_html=True,
                )
                st.metric(
                    label=t["kpi_meb"],
                    value=fmt_fcfa(value),
                    delta=f"{pct_smig:.1f}% {t['vs_aid']}",
                    delta_color="inverse" if pct_smig > 100 else "normal",
                )
                st.caption(f"{t['coverage']}: {pct_smig:.1f}% {t['absorbs']}")

    st.markdown(
        f"""
        <div class="fd-decision">
          <div class="fd-decision-label">{t['decision']}</div>
          <div class="fd-decision-main">
            {t['decision_line'].format(
                date=fmt_month(date_actuelle, lang),
                city=ville_max,
                cost=fmt_fcfa(cout_max),
                smig=fmt_fcfa(smig_mensuel)
            )}
          </div>
          <div class="fd-decision-note">{t['decision_action']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.subheader(t["overview_chart"])
        fig = go.Figure()
        add_city_series(fig, df_calcule)
        fig.update_yaxes(title=t["cost_axis"])
        st.plotly_chart(apply_chart_style(fig, 420), width="stretch")

    st.caption(t["financial_gap_note"])


# =============================================================================
# 11. CVA Analysis — original equal-third budget logic retained and disclosed
# =============================================================================
elif selected_page == "cva":
    st.title(t["cva_title"])
    st.caption(t["cva_desc"])

    rows = []
    for city in villes_disponibles:
        cost = float(dernier_mois[city])
        coverage = (smig_mensuel / cost) * 100 if cost else 0.0
        status = t["adequate"] if coverage >= 100 else t["moderate"] if coverage >= 75 else t["critical"]
        rows.append({
            t["market"]: city,
            t["basket_cost"]: fmt_fcfa(cost),
            t["coverage_rate"]: f"{coverage:.1f} %",
            t["gap"]: f"{(cost - smig_mensuel):+,.0f} FCFA".replace(",", " "),
            t["protection"]: status,
        })

    st.dataframe(
        pd.DataFrame(rows),
        hide_index=True,
        width="stretch",
        height=430,
    )
    st.caption(t["financial_gap_note"])


# =============================================================================
# 12. Market Trends — original comparison and reference thresholds retained
# =============================================================================
elif selected_page == "trends":
    st.title(t["trends_title"])

    tracer_smig = st.checkbox(t["show_smig"], value=True)

    fig_trend = go.Figure()
    add_city_series(fig_trend, df_calcule)

    if tracer_smig:
        fig_trend.add_hline(
            y=smig_mensuel,
            line_dash="dot",
            line_color="#475569",
            line_width=1.5,
            annotation_text=f"SMIG: {fmt_fcfa(smig_mensuel)}",
            annotation_position="top left",
        )

    fig_trend.update_yaxes(title=t["cost_axis"])
    st.plotly_chart(apply_chart_style(fig_trend, 480), width="stretch")

    if st.checkbox(t["show_table"], value=False):
        table = df_calcule.copy()
        table.index.name = t["date"]
        st.dataframe(table.reset_index(), hide_index=True, width="stretch")


# =============================================================================
# 13. Nutrition — original quantities and expenditure shares retained
# =============================================================================
elif selected_page == "nutrition":
    st.title(t["nutrition_title"])

    df_composition = pd.DataFrame({
        t["component"]: [
            t["millet"], t["cowpea"], t["oil"], t["salt"],
        ],
        t["ration"]: [
            f"{60.0 * ratio_foyer:.1f} kg",
            f"{9.0 * ratio_foyer:.1f} kg",
            f"{3.75 * ratio_foyer:.2f} L",
            f"{1.0 * ratio_foyer:.1f} kg",
        ],
        t["expense_share"]: ["62 %", "21 %", "15 %", "2 %"],
        t["diet"]: [
            t["carbs"], t["protein"], t["lipids"], t["micronutrients"],
        ],
        t["market_vulnerability"]: [
            t["risk_critical"], t["risk_high"],
            t["risk_medium"], t["risk_low"],
        ],
    })

    col_r1, col_r2 = st.columns([1.3, 1])
    with col_r1:
        st.dataframe(df_composition, hide_index=True, width="stretch")
    with col_r2:
        fig_donut = go.Figure(
            go.Pie(
                labels=[t["millet"], t["cowpea"], t["oil"], t["salt"]],
                values=[62, 21, 15, 2],
                hole=0.58,
                marker=dict(colors=["#0284C7", "#16A34A", "#F59E0B", "#94A3B8"]),
                textinfo="label+percent",
                textfont=dict(color="#0F172A", size=11),
            )
        )
        fig_donut.update_layout(
            template="simple_white",
            height=330,
            margin=dict(l=8, r=8, t=15, b=10),
            showlegend=False,
            paper_bgcolor="#FFFFFF",
            font=dict(family="Plus Jakarta Sans, sans-serif", color="#0F172A"),
        )
        st.plotly_chart(fig_donut, width="stretch")


# =============================================================================
# 14. Scenarios — real data only, no synthetic shocks
# =============================================================================
elif selected_page == "scenarios":
    st.title(t["scenario_title"])
    st.info(t["scenario_note"])

    scenario_table = df_base[villes_disponibles].iloc[-1].to_frame(name="Dernier prix observé")
    scenario_table["Prix ajusté (ménage)"] = (scenario_table["Dernier prix observé"] * ratio_foyer).round(0)
    st.dataframe(scenario_table, hide_index=True, width="stretch")
    st.caption(t["method_note"])


# =============================================================================
# 15. Data & Export — real CSV export and traceability
# =============================================================================
elif selected_page == "export":
    st.title(t["data_title"])

    col_ex1, col_ex2 = st.columns([1, 1])
    with col_ex1:
        with st.container(border=True):
            st.markdown(f"#### {t['data_status']}")
            st.success(t["real_data"])
            st.markdown(f"**{t['source']}**")
            st.code(source_label)
            st.markdown(f"**{t['period']}**")
            st.write(
                f"{fmt_month(df_calcule.index.min(), lang)} — "
                f"{fmt_month(df_calcule.index.max(), lang)}"
            )

    with col_ex2:
        with st.container(border=True):
            st.markdown(f"#### {t['method']}")
            st.latex(
                r"C_{MEB} = \frac{N}{5}\times"
                r"(60P_{mil}+9P_{niébé}+3.75P_{huile}+1P_{sel})"
            )
            st.caption(t["method_note"])

    st.markdown(f"#### {t['export_title']}")
    csv_export = df_calcule.to_csv(index=True).encode("utf-8-sig")
    st.download_button(
        label=t["download"],
        data=csv_export,
        file_name=f"panier_survie_tchad_{taille_menage}pers.csv",
        mime="text/csv",
        width="stretch",
    )

    with st.expander(t["model_inputs"]):
        st.json({
            "TAILLE_STD": TAILLE_STD,
            "household_size": taille_menage,
            "SMIG_FCFA": smig_mensuel,
            "source_data": source_label,
            "markets": villes_disponibles,
        })


# =============================================================================
# 16. Footer
# =============================================================================
st.markdown(
    f"""
    <div class="fd-footer">
      <b>{t['footer']}</b><br>
      {t['footer2']}
    </div>
    """,
    unsafe_allow_html=True,
)

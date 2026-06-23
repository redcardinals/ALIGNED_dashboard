import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="ALIGNED – Reform Track", page_icon="📊", layout="wide")

# Single source of truth for the citable version. Bump on any data change.
# (Reused by the website build later.)
VERSION = "1.0.2"

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, .stApp, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background: #ffffff !important;
    color: #111111 !important;
}
.stApp { background: #ffffff !important; }
[data-testid="stHeader"] { background: #ffffff !important; border-bottom: 1px solid #e2e8f0; }
[data-testid="stToolbar"] { display: none !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }

/* Hide sidebar collapse button completely */
[data-testid="collapsedControl"],
[data-testid="baseButton-headerNoPadding"],
button[data-testid="collapsedControl"],
.st-emotion-cache-h4xjwg,
[aria-label="keyboard_double_arrow_left"],
[aria-label="keyboard_double_arrow_right"],
[title="keyboard_double_arrow_left"],
[title="keyboard_double_arrow_right"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

[data-testid="stIconMaterial"] {
    display: none !important;
}

.st-emotion-cache-13k62yr,
.st-emotion-cache-d2myc6,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background-color: #ffffff !important;
    color: #111111 !important;
}

/* Selected tags in multiselect */
[data-baseweb="tag"],
[data-baseweb="tag"] span,
span[data-baseweb="tag"],
div[data-baseweb="tag"] {
    background-color: #0d1f3c !important;
    color: #ffffff !important;
    border-radius: 4px !important;
    border: none !important;
}

/* Tag text specifically */
[data-baseweb="tag"] [data-testid="stMarkdownContainer"],
[data-baseweb="tag"] > span,
[data-baseweb="tag"] span:not([role="img"]) {
    color: #ffffff !important;
}

/* Also target by class pattern for newer Streamlit */
span[class*="tag"] {
    background-color: #0d1f3c !important;
    color: #ffffff !important;
}

[data-testid="stSidebar"] {
    background: #f8f9fa !important;
    border-right: 1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] * {
    color: #111111 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Force all tag-like elements in multiselect to be visible */
[data-testid="stMultiSelect"] span[class^="st-"],
[data-testid="stMultiSelect"] div[class^="st-"] > span,
[data-testid="stMultiSelect"] [role="option"],
[data-testid="stMultiSelect"] > div > div > div > div {
    color: #111111 !important;
    background-color: #e8edf2 !important;
}

.home .wp-block-buttons {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 1.2rem !important;
    max-width: 600px;
    margin: 0 auto !important;
    align-items: stretch !important;
}

/* ── Sidebar buttons ────────────────────────────────────────────────────────
   Streamlit 1.37.x paints the default focus ring as a box-shadow and recolours
   the border via :focus / :focus:not(:active) on the inner <button>, sometimes
   addressed by [data-testid="baseButton-secondary"]. We collapse every
   interaction state (hover/focus/active) into one intentional navy state and
   kill the box-shadow everywhere, so the ring never reverts to Streamlit blue. */
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {
    background-color: #ffffff !important;
    color: #2d3748 !important;
    border: 1.5px solid #cbd5e0 !important;
    border-radius: 6px !important;
    font-size: 0.76rem !important;
    font-weight: 500 !important;
    padding: 0.4rem 0.65rem !important;
    width: 100% !important;
    text-align: left !important;
    box-shadow: none !important;
    outline: none !important;
    margin-bottom: 2px !important;
    transition: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover,
[data-testid="stSidebar"] .stButton > button:focus,
[data-testid="stSidebar"] .stButton > button:focus-visible,
[data-testid="stSidebar"] .stButton > button:focus:not(:active),
[data-testid="stSidebar"] .stButton > button:active,
[data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover,
[data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:focus,
[data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:focus-visible,
[data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:active {
    background-color: #f0f4f8 !important;
    border-color: #0d1f3c !important;
    color: #0d1f3c !important;
    box-shadow: none !important;
    outline: none !important;
}

/* ── Download buttons ──────────────────────────────────────────────────────── */
.stDownloadButton > button,
.stDownloadButton button[data-testid="baseButton-secondary"] {
    background-color: #f8f9fa !important;
    color: #2d3748 !important;
    border: 1.5px solid #cbd5e0 !important;
    border-radius: 6px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    outline: none !important;
    transition: none !important;
}
.stDownloadButton > button:hover,
.stDownloadButton > button:focus,
.stDownloadButton > button:focus-visible,
.stDownloadButton > button:focus:not(:active),
.stDownloadButton > button:active,
.stDownloadButton button[data-testid="baseButton-secondary"]:hover,
.stDownloadButton button[data-testid="baseButton-secondary"]:focus,
.stDownloadButton button[data-testid="baseButton-secondary"]:focus-visible,
.stDownloadButton button[data-testid="baseButton-secondary"]:active {
    background-color: #0d1f3c !important;
    color: #ffffff !important;
    border-color: #0d1f3c !important;
    box-shadow: none !important;
    outline: none !important;
}

.sb-sec {
    font-size: 0.62rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
    color: #8a96a8 !important;
    font-weight: 600 !important;
    margin-top: 0.9rem !important;
    margin-bottom: 0.2rem !important;
    display: block;
}
.wsa-badge {
    display: inline-block; background: #B85C38; color: white;
    font-size: 0.58rem; padding: 1px 6px; border-radius: 10px;
    font-weight: 600; vertical-align: middle; margin-left: 4px;
}
.brand-name { font-size: 2rem; font-weight: 800; color: #0d1f3c; letter-spacing: -0.03em; line-height: 1; }
.brand-rule { height: 3px; width: 40px; background: #c5a84a; border-radius: 2px; margin: 6px 0 8px 0; }
.brand-sub  { font-size: 0.82rem; color: #5a7399; line-height: 1.45; }
.stat-card  { background: #f8f9fa; border: 1px solid #e2e8f0; border-top: 3px solid #c5a84a; border-radius: 8px; padding: 0.85rem 1rem; }
.stat-label { font-size: 0.63rem; color: #8a96a8; text-transform: uppercase; letter-spacing: 0.07em; font-weight: 600; margin-bottom: 0.2rem; }
.stat-value { font-size: 1.45rem; font-weight: 700; color: #0d1f3c; }
.stat-value.neg { color: #922b21; }
.stat-value.pos { color: #1a6b3c; }
.cite-label { font-size: 0.63rem; text-transform: uppercase; letter-spacing: 0.09em; color: #8a96a8; font-weight: 600; margin-top: 0.8rem; margin-bottom: 0.5rem; display: block; }
.cite-box { background: #f8f9fa; border: 1px solid #e2e8f0; border-left: 3px solid #c5a84a; border-radius: 0 6px 6px 0; padding: 0.8rem 1rem 0.8rem 2.6rem; text-indent: -1.6rem; font-size: 0.8rem; color: #2d3748; line-height: 1.6; }
.cite-box em { font-style: italic; }
.cite-box a { color: #5a7399; }
.mbox  { background: #f8f9fa; border-left: 3px solid #0d1f3c; border-radius: 0 6px 6px 0; padding: 0.7rem 1rem; font-size: 0.77rem; color: #4a5568; line-height: 1.55; margin-top: 1rem; }
.footer{ font-size: 0.71rem; color: #a0aec0; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #e2e8f0; }
.footer a { color: #5a7399; }
.wsa-note { background: #fff4e6; border-left: 3px solid #B85C38; border-radius: 0 4px 4px 0; padding: 0.5rem 0.7rem; font-size: 0.72rem; color: #7a3b1e; line-height: 1.4; margin-bottom: 0.5rem; }

/* ── Multiselect / dropdown widgets ─────────────────────────────────────────── */
[data-testid="stMultiSelect"] > label,
[data-testid="stSelectbox"] > label {
    font-size: 0.72rem !important;
    color: #8a96a8 !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
}
[data-testid="stMultiSelect"] > label::before,
[data-testid="stSelectbox"] > label::before {
    content: '⊞ ';
    color: #c5a84a;
    font-style: normal;
}
[data-baseweb="select"] > div,
[data-baseweb="select"] > div:focus-within {
    background-color: #ffffff !important;
    border-color: #cbd5e0 !important;
    border-radius: 6px !important;
}
[data-baseweb="select"] span,
[data-baseweb="select"] div {
    color: #111111 !important;
    background-color: transparent !important;
}
[data-baseweb="menu"] {
    background-color: #ffffff !important;
}
[data-baseweb="menu"] li {
    color: #111111 !important;
    background-color: #ffffff !important;
}
[data-baseweb="menu"] li:hover {
    background-color: #f0f4f8 !important;
    color: #0d1f3c !important;
}
/* Tags inside multiselect */
[data-baseweb="tag"] {
    background-color: #0d1f3c !important;
    color: #ffffff !important;
    border-radius: 4px !important;
}
[data-baseweb="tag"] span {
    color: #ffffff !important;
}
/* Slider track colour */
[data-testid="stSlider"] [role="slider"] {
    background-color: #0d1f3c !important;
}
div[data-baseweb="slider"] [data-testid="stTickBar"] {
    background: linear-gradient(to right, #0d1f3c, #c5a84a) !important;
}
</style>""", unsafe_allow_html=True)

# ─── TRANSLATION MAPS ──────────────────────────────────────────────────────────
DIM1_MAP = {
    'Политички критеријуми': 'Political Criteria',
    'Економски критеријуми': 'Economic Criteria',
}
DIM2_MAP = {
    'Политички критеријуми':                                    'Political Criteria',
    'Цивилно друштво':                                          'Civil Society',
    'Реформа јавне управе':                                     'Public Administration Reform',
    'Правосудни систем':                                        'Judiciary',
    'Борба против корупције':                                   'Fight Against Corruption',
    'Борба против организованог криминала':                     'Fight Against Organised Crime',
    'Основна права':                                            'Fundamental Rights',
    'Слобода изражавања':                                       'Freedom of Expression',
    'Економски критеријуми':                                    'Economic Criteria',
    'Притисак конкуренције и тржишних снага унутар ЕУ':         'Competitive Pressure and Market Forces',
    'Регионална сарадња':                                       'Regional Cooperation',
    'Нормализација односа са Косовом':                          'Normalisation of Relations with Kosovo',
    'Способност преузимања обавеза које проистичу из чланства': 'Capacity to Take on Membership Obligations',
    'Конкурентност и инклузивни раст':                          'Competitiveness and Inclusive Growth',
    'Зелена агенда и одрживо повезивање':                       'Green Agenda and Sustainable Connectivity',
    'Ресурси, пољопривреда и кохезија':                         'Resources, Agriculture and Cohesion',
    'Спољњи односи':                                            'External Relations',
    'Миграције':                                                'Migration',
    'Унутрашње тржиште':                                        'Internal Market',
    'Развој функционалне тржишне привреде':                     'Development of a Functional Market Economy',
}
EFFORT_MAP = {'Код куће': 'Domestic', 'Међународни': 'International'}

WSA_PRIMARY   = ['Migration', 'Normalisation of Relations with Kosovo',
                 'External Relations', 'Regional Cooperation']
WSA_SECONDARY = ['Civil Society', 'Public Administration Reform',
                 'Freedom of Expression', 'Fundamental Rights']
WSA_ALL       = WSA_PRIMARY + WSA_SECONDARY

COMBO_COLORS = {
    ('Political', 'Domestic'):      '#6B2737',
    ('Political', 'International'): '#B5832A',
    ('Economic',  'Domestic'):      '#1B3D6B',
    ('Economic',  'International'): '#2D5A3D',
}
SINGLE_DIM = {'Political': '#6B2737', 'Economic': '#1B3D6B'}
SINGLE_EFF = {'Domestic':  '#B85C38', 'International': '#2D5A3D'}
C_OVERALL   = '#0d1f3c'
C_PRIMARY   = '#B85C38'
C_SECONDARY = '#2D5A3D'
TOPIC_PAL   = ['#6B2737','#1B3D6B','#B85C38','#2D5A3D',
                '#B5832A','#2A6B6B','#5C2D6B','#8B4513','#2F4F8F','#556B2F']

# Maps a dimension label to its Serbian-derived English dim1 value.
DIM_VALUE = {'Political': 'Political Criteria', 'Economic': 'Economic Criteria'}

# ─── DATA LOADING ──────────────────────────────────────────────────────────────
# Change DATA_FILE / DATA_SHEET here if the dataset is ever renamed.
# Website build: replace the local load with a secrets-based remote fetch.
DATA_FILE  = "aligned_data.xlsx"
DATA_SHEET = "data"

@st.cache_data
def load_data():
    folder = os.path.dirname(os.path.abspath(__file__))
    path   = os.path.join(folder, DATA_FILE)
    if not os.path.exists(path):
        st.error(
            f"Dataset not found. Expected \"{DATA_FILE}\" "
            "in the same folder as aligned_app.py"
        )
        st.stop()
    df = pd.read_excel(path, sheet_name=DATA_SHEET)
    df = df.rename(columns={
        'Година': 'year', 'Димензија (Политика економија)': 'dim1_sr',
        'Димензија 2 (као што је у Извештају)': 'dim2_sr',
        'Реченица': 'sentence', 'Оцена': 'score',
        'Врста напора': 'effort_sr', 'Верификација': 'verified',
    })
    df['dim1']   = df['dim1_sr'].map(DIM1_MAP)
    df['dim2']   = df['dim2_sr'].map(DIM2_MAP)
    df['effort'] = df['effort_sr'].map(EFFORT_MAP)
    return df

df         = load_data()
ALL_YEARS  = sorted(df['year'].unique())
ALL_TOPICS = sorted(df['dim2'].dropna().unique())

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
DEFAULTS = {
    'mode':         'normal',
    'cb_pol':       False,
    'cb_econ':      False,
    'cb_dom':       False,
    'cb_intl':      False,
    'free_topics':  [],
    'wsa_interest': 'Both interests',
    'wsa_p_sel':    [],
    'wsa_s_sel':    [],
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── EXCLUSIVITY CALLBACKS ──────────────────────────────────────────────────────
# There are three mutually exclusive control families:
#   1. Checkboxes (Political / Economic / Domestic / International)
#   2. Free topic multiselect
#   3. World-Systems Analysis (radio + the two disaggregation multiselects)
# Rule: whichever family the user touches last takes over completely and clears
# the other two. This guarantees the sidebar can never display an inert control
# (e.g. a checked box that has no effect because WSA is driving the chart).

def _clear_checkboxes():
    st.session_state.cb_pol  = False
    st.session_state.cb_econ = False
    st.session_state.cb_dom  = False
    st.session_state.cb_intl = False

def _clear_wsa():
    st.session_state.wsa_p_sel   = []
    st.session_state.wsa_s_sel   = []
    st.session_state.wsa_interest = 'Both interests'

def on_checkbox_change():
    st.session_state.mode = 'normal'
    st.session_state.free_topics = []
    _clear_wsa()

def on_free_topics_change():
    # Keep the new free_topics selection; clear the other two families.
    st.session_state.mode = 'normal'
    _clear_checkboxes()
    _clear_wsa()

def on_wsa_interest_change():
    # Changing the interest type re-scopes which disaggregation lists are valid,
    # so clear both selections; clear the other two families.
    st.session_state.mode = 'wsa'
    _clear_checkboxes()
    st.session_state.free_topics = []
    st.session_state.wsa_p_sel = []
    st.session_state.wsa_s_sel = []

def on_wsa_select_change():
    # Keep the new WSA multiselect selection; clear the other two families.
    st.session_state.mode = 'wsa'
    _clear_checkboxes()
    st.session_state.free_topics = []

def set_preset(p):
    # Presets start from a fully cleared state, then set only what they need.
    _clear_checkboxes()
    st.session_state.free_topics = []
    st.session_state.wsa_p_sel = []
    st.session_state.wsa_s_sel = []
    st.session_state.wsa_interest = 'Both interests'
    if p == 'wsa':
        st.session_state.mode = 'wsa'
    else:
        st.session_state.mode = 'normal'
        if p == 'polecon':
            st.session_state.cb_pol  = True
            st.session_state.cb_econ = True
        elif p == 'domintl':
            st.session_state.cb_dom  = True
            st.session_state.cb_intl = True
        # 'full' leaves everything unchecked → overall/default view.

# ─── SELECTION RESOLVER (single source of truth) ────────────────────────────────
def resolve_groups(base):
    """
    Resolve the whole of session_state into the series/bars to display.

    Returns (groups, filtered, default):
      groups   : list of (label, color, subdf) — one entry per line/bar.
      filtered : subdf used by the stat cards (union of all groups, or `base`
                 in the default case). Groups never overlap, so the union is a
                 plain concat.
      default  : True only in normal mode with no checkbox/free-topic/WSA
                 selection. In that case `groups` is empty and each view renders
                 its own default (Trend → overall line; Ranking → per-topic bars).

    Both the Trend and Ranking views consume this, so the dimension/effort/WSA
    logic lives in exactly one place.

    Normal-mode dimension/effort rules:
      dims=2 & effs=2 → efforts cancel → one full line per dimension
      dims=1 & effs=2 → split that dimension by each effort → two lines
      dims=any & effs=1 → filter dimension(s) by that single effort
      dims=any & effs=0 → full dimension(s), no effort filter
      dims=0 & effs>0  → locality view: one line per effort
      dims=0 & effs=0  → default (handled by caller)
    """
    mode        = st.session_state.mode
    pol         = st.session_state.cb_pol
    econ        = st.session_state.cb_econ
    dom         = st.session_state.cb_dom
    intl        = st.session_state.cb_intl
    free_topics = st.session_state.free_topics
    wsa_int     = st.session_state.wsa_interest
    wsa_p_sel   = st.session_state.wsa_p_sel
    wsa_s_sel   = st.session_state.wsa_s_sel

    empty = base.iloc[0:0]

    def finish(groups):
        filt = pd.concat([g[2] for g in groups]) if groups else empty
        return groups, filt, False

    # ── WSA mode ────────────────────────────────────────────────────────────
    if mode == 'wsa':
        sel = wsa_p_sel + wsa_s_sel
        groups = []
        if sel:
            for i, t in enumerate(sel):
                groups.append((t, TOPIC_PAL[i % len(TOPIC_PAL)], base[base['dim2'] == t]))
        elif wsa_int == 'Primary interests':
            groups.append(("Primary interests", C_PRIMARY,
                           base[base['dim2'].isin(WSA_PRIMARY)]))
        elif wsa_int == 'Secondary interests':
            groups.append(("Secondary interests", C_SECONDARY,
                           base[base['dim2'].isin(WSA_SECONDARY)]))
        else:  # Both interests
            groups.append(("Primary interests",   C_PRIMARY,
                           base[base['dim2'].isin(WSA_PRIMARY)]))
            groups.append(("Secondary interests", C_SECONDARY,
                           base[base['dim2'].isin(WSA_SECONDARY)]))
        return finish(groups)

    # ── Normal mode: free topic picker ────────────────────────────────────────
    if free_topics:
        groups = [(t, TOPIC_PAL[i % len(TOPIC_PAL)], base[base['dim2'] == t])
                  for i, t in enumerate(free_topics)]
        return finish(groups)

    # ── Normal mode: checkbox logic ────────────────────────────────────────────
    dims = [d for d, c in [('Political', pol), ('Economic', econ)] if c]
    effs = [e for e, c in [('Domestic',  dom), ('International', intl)] if c]

    if dims:
        groups = []
        if len(dims) == 2 and len(effs) == 2:
            # All four selected: efforts cancel — one full line per dimension.
            for dim in dims:
                groups.append((dim, SINGLE_DIM[dim],
                               base[base['dim1'] == DIM_VALUE[dim]]))
        elif len(dims) == 1 and len(effs) == 2:
            # One dimension, both efforts: split that dimension by effort.
            dim = dims[0]
            for eff in effs:
                sub = base[(base['dim1'] == DIM_VALUE[dim]) & (base['effort'] == eff)]
                groups.append((f"{dim} ({eff.lower()} efforts)",
                               COMBO_COLORS.get((dim, eff), C_OVERALL), sub))
        elif len(effs) == 1:
            # One or two dimensions filtered by a single effort.
            eff = effs[0]
            for dim in dims:
                sub = base[(base['dim1'] == DIM_VALUE[dim]) & (base['effort'] == eff)]
                groups.append((f"{dim} ({eff.lower()} efforts)",
                               COMBO_COLORS.get((dim, eff), C_OVERALL), sub))
        else:
            # Dimensions only, no effort filter.
            for dim in dims:
                groups.append((dim, SINGLE_DIM[dim],
                               base[base['dim1'] == DIM_VALUE[dim]]))
        return finish(groups)

    if effs:
        # No dimensions: locality view, one line per effort.
        groups = [(f"{eff} efforts", SINGLE_EFF[eff], base[base['effort'] == eff])
                  for eff in effs]
        return finish(groups)

    # ── Normal mode: nothing selected → default ───────────────────────────────
    return [], base, True

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:0.5rem 0 0.8rem 0;'>
        <div style='font-size:1.2rem;font-weight:800;color:#0d1f3c;letter-spacing:-0.02em;'>ALIGNED</div>
        <div style='font-size:0.67rem;color:#8a96a8;margin-top:2px;line-height:1.4;'>
            Assessing Legal and Institutional<br>Governance Norms in European Democracies
        </div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<span class='sb-sec'>Presentation Presets</span>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.button("Full Picture",  key="pr_full",    use_container_width=True,
                  on_click=set_preset, args=('full',))
        st.button("Dom. vs Intl.", key="pr_domintl", use_container_width=True,
                  on_click=set_preset, args=('domintl',))
    with c2:
        st.button("Pol. vs Econ.", key="pr_polecon", use_container_width=True,
                  on_click=set_preset, args=('polecon',))
        st.button("World-Systems", key="pr_wsa",     use_container_width=True,
                  on_click=set_preset, args=('wsa',))

    st.markdown("---")

    st.markdown("<span class='sb-sec'>Year Range</span>", unsafe_allow_html=True)
    start_year, end_year = st.select_slider(
        "years", options=ALL_YEARS, value=(ALL_YEARS[0], ALL_YEARS[-1]),
        label_visibility="collapsed",
        help="No separate report was published for 2017. "
             "Data from that period is included in the 2018 report."
    )
    st.markdown("---")

    mode = st.session_state.mode
    wsa_badge = " <span class='wsa-badge'>WSA active</span>" if mode == 'wsa' else ""
    st.markdown(f"<span class='sb-sec'>Customise{wsa_badge}</span>", unsafe_allow_html=True)

    cc1, cc2 = st.columns(2)
    with cc1:
        st.checkbox("Political",     key='cb_pol',  on_change=on_checkbox_change)
        st.checkbox("Domestic",      key='cb_dom',  on_change=on_checkbox_change)
    with cc2:
        st.checkbox("Economic",      key='cb_econ', on_change=on_checkbox_change)
        st.checkbox("International", key='cb_intl', on_change=on_checkbox_change)

    st.multiselect(
        "Free topic selection", ALL_TOPICS,
        key='free_topics', placeholder="Search and select topics…",
        on_change=on_free_topics_change,
    )

    st.markdown("---")

    active_badge = " <span class='wsa-badge'>Active</span>" if mode == 'wsa' else ""
    st.markdown(
        f"<span class='sb-sec'>World-Systems Analysis{active_badge}</span>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='wsa-note'>Primary and secondary interests of the EU core. "
        "Theoretical classification — work in progress.</div>",
        unsafe_allow_html=True
    )

    # The radio shows a greyed-out hint when WSA is not active,
    # and only becomes the controlling input once WSA mode is engaged.
    # Clicking any option activates WSA mode automatically.
    wsa_options = ['Both interests', 'Primary interests', 'Secondary interests']
    if mode != 'wsa':
        st.markdown(
            "<div style='font-size:0.72rem;color:#b0bac8;font-style:italic;"
            "margin-bottom:0.3rem;'>Activate by selecting an option below</div>",
            unsafe_allow_html=True
        )
    st.radio(
        "Interest type",
        wsa_options,
        key='wsa_interest',
        label_visibility="collapsed",
        on_change=on_wsa_interest_change,
    )

    wsa_int = st.session_state.wsa_interest

    if wsa_int in ('Both interests', 'Primary interests'):
        st.multiselect(
            "Disaggregate: primary interests", WSA_PRIMARY,
            key='wsa_p_sel', placeholder="Select topics…", on_change=on_wsa_select_change,
        )
    if wsa_int in ('Both interests', 'Secondary interests'):
        st.multiselect(
            "Disaggregate: secondary interests", WSA_SECONDARY,
            key='wsa_s_sel', placeholder="Select topics…", on_change=on_wsa_select_change,
        )

    st.markdown("---")

    st.markdown("<span class='sb-sec'>View</span>", unsafe_allow_html=True)
    view_choice = st.radio(
        "view", ['Trend over time', 'Overall ranking'],
        label_visibility="collapsed"
    )
    view_mode = 'Trend' if view_choice == 'Trend over time' else 'Ranking'

# ─── RESOLVE STATE ──────────────────────────────────────────────────────────────
base = df[(df['year'] >= start_year) & (df['year'] <= end_year)].copy()

groups, filtered, default = resolve_groups(base)

if filtered.empty:
    st.info("No data matches the current selection."); st.stop()

# ─── MAIN HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom:1.2rem;'>
    <div class='brand-name'>ALIGNED</div>
    <div class='brand-rule'></div>
    <div class='brand-sub'>Tracking how the European Commission evaluates reform progress
    in EU candidate countries — sentence by sentence, year by year.</div>
</div>""", unsafe_allow_html=True)

# ─── STAT CARDS ────────────────────────────────────────────────────────────────
avg  = filtered['score'].mean()
n    = len(filtered)
pneg = (filtered['score'] < 0).mean() * 100
cls  = "neg" if avg < -0.05 else ("pos" if avg > 0.05 else "")

c1, c2, c3, c4 = st.columns(4)
for col, lbl, val, c in [
    (c1, "Average Score", f"{avg:+.3f}", cls),
    (c2, "Sentences",     str(n),        ""),
    (c3, "Years",         f"{start_year}–{end_year}", ""),
    (c4, "Negative",      f"{pneg:.0f}%", "neg" if pneg > 50 else ""),
]:
    with col:
        st.markdown(
            f'<div class="stat-card"><div class="stat-label">{lbl}</div>'
            f'<div class="stat-value {c}">{val}</div></div>',
            unsafe_allow_html=True
        )

st.markdown("<div style='height:1.1rem;'></div>", unsafe_allow_html=True)

# ─── CHART ─────────────────────────────────────────────────────────────────────
Y_RANGE = [-1.1, 1.1]
Y_TICKS = [-1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0]

AFONT = dict(color='#111111', size=11, family='Inter,sans-serif')
BASE_LAYOUT = dict(
    template='simple_white',
    showlegend=True,
    font=dict(family='Inter,sans-serif', color='#111111', size=12),
    paper_bgcolor='white', plot_bgcolor='white',
    margin=dict(t=20, b=90, l=20, r=60),
    legend=dict(
        orientation='h', yanchor='top', y=-0.18, xanchor='center', x=0.5,
        font=dict(color='#111111', size=11, family='Inter,sans-serif'),
        bgcolor='rgba(0,0,0,0)', borderwidth=0,
    ),
    hoverlabel=dict(bgcolor='white', bordercolor='#e2e8f0',
                    font=dict(family='Inter', size=12, color='#111111')),
)

fig     = go.Figure()
traces  = []                 # Trend series; also consumed by the CSV export.
df_rank = pd.DataFrame()     # Ranking rows; also consumed by the CSV export.

if view_mode == 'Trend':
    # Build the year-aggregated series from the resolved groups.
    if default:
        d = base.groupby('year')['score'].mean().reset_index()
        if not d.empty:
            traces.append(("Overall average", C_OVERALL, d))
    else:
        for label, color, sub in groups:
            d = sub.groupby('year')['score'].mean().reset_index()
            if not d.empty:
                traces.append((label, color, d))

    if not traces:
        st.info("No data to display for this selection."); st.stop()

    all_scores, year_vals = [], set()
    for label, color, data in traces:
        fig.add_trace(go.Scatter(
            x=data['year'], y=data['score'],
            mode='lines+markers', name=label,
            line=dict(color=color, width=2.5),
            marker=dict(size=7, color=color, line=dict(color='white', width=1.5)),
            hovertemplate=f'<b>%{{x}}</b><br>{label}: %{{y:.3f}}<extra></extra>',
        ))
        all_scores.extend(data['score'].tolist())
        year_vals.update(data['year'].tolist())

    # Zero reference line as an in-plot guide. The x-axis sits at the bottom
    # (see layout below), so this line and the year ticks no longer collide.
    fig.add_hline(y=0, line_color='#333333', line_width=1.2)

    if all_scores:
        mn, mx = min(all_scores), max(all_scores)
        fig.add_hline(y=mn, line_dash='dot', line_color='#bbbbbb', line_width=1)
        fig.add_annotation(x=1.01, y=mn, xref='paper', yref='y', showarrow=False,
                           text=f"{mn:+.2f}",
                           font=dict(color='#aaaaaa', size=9, family='Inter'),
                           xanchor='left', yanchor='middle')
        if abs(mx - mn) > 0.01:
            fig.add_hline(y=mx, line_dash='dot', line_color='#bbbbbb', line_width=1)
            fig.add_annotation(x=1.01, y=mx, xref='paper', yref='y', showarrow=False,
                               text=f"{mx:+.2f}",
                               font=dict(color='#aaaaaa', size=9, family='Inter'),
                               xanchor='left', yanchor='middle')

    fig.update_layout(
        **BASE_LAYOUT,
        xaxis=dict(tickvals=sorted(year_vals),
                   tickfont=AFONT, linecolor='#111111', linewidth=1.5,
                   showgrid=False, zeroline=False, title=None),
        yaxis=dict(range=Y_RANGE, tickvals=Y_TICKS, tickfont=AFONT,
                   linecolor='#111111', linewidth=1, gridcolor='#eeeeee',
                   gridwidth=1, zeroline=False, title=None),
    )

else:  # Ranking
    rows = []
    if default:
        # Per-topic ranking, coloured by sign of the mean score.
        for t in ALL_TOPICS:
            s = base[base['dim2'] == t]['score'].mean()
            if not pd.isna(s):
                clr = '#922b21' if s < -0.05 else ('#c5a84a' if abs(s) <= 0.05 else '#1a6b3c')
                rows.append({'label': t, 'score': s, 'color': clr})
    else:
        # Same groups as the Trend view, aggregated overall instead of by year.
        for label, color, sub in groups:
            s = sub['score'].mean()
            rows.append({'label': label, 'score': s, 'color': color})

    if not rows:
        st.info("No data to display."); st.stop()

    df_rank = pd.DataFrame(rows).dropna(subset=['score']).sort_values('score', ascending=True)
    fig.add_trace(go.Bar(
        x=df_rank['score'], y=df_rank['label'], orientation='h',
        marker_color=df_rank['color'].tolist(), marker_line_width=0,
        text=[f"{s:+.2f}" for s in df_rank['score']],
        textposition='outside',
        textfont=dict(size=11, color='#111111', family='Inter,sans-serif'),
        hovertemplate='<b>%{y}</b><br>Score: %{x:.3f}<extra></extra>',
    ))
    fig.add_vline(x=0, line_color='#333333', line_width=1.2)
    fig.update_layout(**{
        **BASE_LAYOUT,
        'xaxis': dict(range=[-1.3, 1.3], tickvals=Y_TICKS, tickfont=AFONT,
                      linecolor='#111111', linewidth=1, gridcolor='#eeeeee',
                      zeroline=False, title=None),
        'yaxis': dict(tickfont=AFONT, linecolor='#111111', linewidth=1, title=None),
        'margin': dict(t=20, b=20, l=260, r=90),
        'height': max(280, len(df_rank) * 48),
    })

st.plotly_chart(fig, use_container_width=True)

# ─── DOWNLOADS ─────────────────────────────────────────────────────────────────
d1, d2 = st.columns(2)
with d1:
    try:
        svg = fig.to_image(format='svg', engine='kaleido')
        st.download_button("⬇ Download Chart (SVG)", data=svg,
                           file_name="aligned_chart.svg", mime="image/svg+xml")
    except Exception:
        # Fallback: export chart as self-contained HTML
        html_bytes = fig.to_html(include_plotlyjs='cdn', full_html=True).encode()
        st.download_button("⬇ Download Chart (HTML)", data=html_bytes,
                           file_name="aligned_chart.html", mime="text/html")
with d2:
    if view_mode == 'Trend' and traces:
        frames = [data[['year','score']].rename(columns={'score': label})
                  for label, _, data in traces]
        csv_df = frames[0]
        for f in frames[1:]: csv_df = csv_df.merge(f, on='year', how='outer')
        csv_bytes = csv_df.sort_values('year').to_csv(index=False).encode()
    elif not df_rank.empty:
        csv_bytes = (df_rank[['label','score']]
                     .rename(columns={'label':'Category','score':'Average Score'})
                     .to_csv(index=False).encode())
    else:
        csv_bytes = b"No data\n"
    st.download_button("⬇ Download Data (CSV)", data=csv_bytes,
                       file_name="aligned_data.csv", mime="text/csv")

# ─── CITATION ──────────────────────────────────────────────────────────────────
# APA 7 dataset reference + BibTeX, both driven by VERSION and DOI.
apa_cite = (
    f"Karadžić, O. (2026). Assessing Legal and Institutional Governance Norms "
    f"in European Democracies (ALIGNED) (Version {VERSION}) [Data set]. "
    f"Reform Track. https://doi.org/10.5281/zenodo.20820079"
)
bibtex_cite = (
    "@misc{karadzic2026aligned,\n"
    "  author  = {Karad\\v{z}i\\'c, Ognjen},\n"
    "  title   = {{Assessing Legal and Institutional Governance Norms in "
    "European Democracies (ALIGNED)}},\n"
    "  year    = {2026},\n"
    f"  version = {{{VERSION}}},\n"
    "  note    = {Data set},\n"
    "  url     = {https://reformtrack.org},\n"
    "  doi     = {10.5281/zenodo.20820079}\n"
    "}"
)
st.markdown("<span class='cite-label'>Cite this dataset</span>", unsafe_allow_html=True)
st.markdown(
    "<div class='cite-box'>Karadžić, O. (2026). "
    "<em>Assessing Legal and Institutional Governance Norms in European Democracies "
    f"(ALIGNED)</em> (Version {VERSION}) [Data set]. Reform Track. "
    "<a href='https://doi.org/10.5281/zenodo.20820079'>https://doi.org/10.5281/zenodo.20820079</a></div>",
    unsafe_allow_html=True
)
with st.expander("Copy citation (APA 7 · BibTeX)"):
    st.caption("APA 7")
    st.code(apa_cite, language=None)
    st.caption("BibTeX")
    st.code(bibtex_cite, language="bibtex")

# ─── METHODOLOGY ───────────────────────────────────────────────────────────────
st.markdown("""
<div class='mbox'>
    <strong>Methodology:</strong> Scores derive from core-sentence analysis of EC Progress
    Reports for Serbia (2015–2023). Each evaluative sentence is coded −1 (strongly negative)
    to +1 (strongly positive) with intermediary values at −0.5 and +0.5.
    Inter-coder reliability: 0.81 simple agreement (≈15% of corpus, 3 coders).
    Neutral (0) and non-evaluative sentences excluded. Results reflect EC framing —
    not an objective measure of reform progress.
    World-Systems Analysis classification is theoretical and a work in progress.
</div>""", unsafe_allow_html=True)

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    <strong>ALIGNED</strong> — Assessing Legal and Institutional Governance Norms
    in European Democracies &nbsp;·&nbsp;
    <a href='https://reformtrack.org'>reformtrack.org</a> &nbsp;·&nbsp;
    © 2026 Reform Track. Not for commercial use.
</div>""", unsafe_allow_html=True)

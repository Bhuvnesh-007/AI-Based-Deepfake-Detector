"""
style.py
Central place for all CSS used across the app, so Home / How It Works / About
all stay visually consistent. Import get_css() and inject it with st.markdown.
"""

CUSTOM_CSS = """
<style>
/* ---------- Google Font ---------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

/* ---------- App background ---------- */
.stApp {
    background: radial-gradient(circle at 20% 0%, #161226 0%, #0a0a14 45%, #07070d 100%);
    color: #e6e6f0;
}

/* Hide default Streamlit chrome we don't want */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background: transparent;
}

/* Tone down default top padding so navbar sits high */
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1600px;
}

/* ---------- Top Navbar ---------- */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 28px;
    background: rgba(20, 18, 35, 0.75);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    margin-bottom: 28px;
    backdrop-filter: blur(10px);
}

.navbar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 800;
    font-size: 1.15rem;
    letter-spacing: 0.5px;
    color: #f5f5ff;
}

.navbar-brand .logo-badge {
    width: 34px;
    height: 34px;
    border-radius: 9px;
    background: linear-gradient(135deg, #6b5bff 0%, #36c9ff 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 1rem;
    color: white;
    box-shadow: 0 0 18px rgba(107, 91, 255, 0.55);
}

.navbar-brand .brand-sub {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 2px;
    color: #8a87a8;
    display: block;
    margin-top: -2px;
}

/* ---------- Section headers ---------- */
.page-title {
    font-size: 2.1rem;
    font-weight: 800;
    color: #f7f7ff;
    margin-bottom: 4px;
}

.page-subtitle {
    color: #9c98b8;
    font-size: 0.98rem;
    margin-bottom: 28px;
    max-width: 640px;
}

/* ---------- Generic glass card ---------- */
.glass-card {
    background: linear-gradient(160deg, rgba(34,30,58,0.65), rgba(20,18,35,0.55));
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 26px;
    margin-bottom: 18px;
}

.glass-card h3 {
    color: #f5f5ff;
    font-size: 1.15rem;
    margin-bottom: 6px;
}

.glass-card p {
    color: #9c98b8;
    font-size: 0.9rem;
    line-height: 1.5;
}

/* Streamlit's native st.container(border=True) — style it identically to
   .glass-card so real containers (which actually wrap their children,
   unlike raw markdown divs) get the same visual treatment. */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(160deg, rgba(34,30,58,0.65), rgba(20,18,35,0.55));
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 16px !important;
    padding: 6px 20px 20px 20px;
    margin-bottom: 18px;
}

/* ---------- Step item (How It Works) ---------- */
.step-row {
    display: flex;
    gap: 16px;
    margin-bottom: 14px;
}

.step-num {
    flex-shrink: 0;
    width: 42px;
    height: 42px;
    border-radius: 50%;
    border: 1px solid rgba(120,110,255,0.5);
    background: rgba(80,70,160,0.18);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: #b9b3ff;
}

.step-icon {
    flex-shrink: 0;
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: rgba(70,60,140,0.25);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
}

.step-content {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 16px 20px;
    flex: 1;
}

.step-content h4 {
    color: #f5f5ff;
    margin: 0 0 4px 0;
    font-size: 1.02rem;
}

.step-content p {
    color: #9c98b8;
    margin: 0;
    font-size: 0.87rem;
    line-height: 1.5;
}

/* ---------- Feature mini cards (About) ---------- */
.mini-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 18px;
    text-align: left;
}

.mini-card .icon-circle {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
    font-size: 1.1rem;
}

.mini-card h4 {
    color: #f0f0fa;
    font-size: 0.95rem;
    margin: 0 0 4px 0;
}

.mini-card p {
    color: #8d89ab;
    font-size: 0.82rem;
    margin: 0;
    line-height: 1.45;
}

/* ---------- Stat tiles ---------- */
.stat-tile {
    text-align: center;
    padding: 18px 10px;
}

.stat-tile .stat-num {
    font-size: 1.7rem;
    font-weight: 800;
    color: #f5f5ff;
}

.stat-tile .stat-label {
    color: #8d89ab;
    font-size: 0.8rem;
    margin-top: 2px;
}

/* ---------- Confidence badge ---------- */
.badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
    border: 1px solid rgba(74, 222, 128, 0.35);
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
}

.badge-pill.fake {
    background: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border: 1px solid rgba(248, 113, 113, 0.35);
}

/* ---------- Upload dropzone look-alike ---------- */
.upload-hint {
    text-align: center;
    color: #8d89ab;
    font-size: 0.82rem;
    margin-top: 8px;
}

/* Style the actual Streamlit file uploader to feel like the mockup dropzone */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1.5px dashed rgba(140,130,255,0.4) !important;
    border-radius: 14px !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] svg {
    color: #8c82ff !important;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #6b5bff 0%, #36c9ff 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 1.1rem;
    font-weight: 600;
    transition: opacity 0.15s ease;
}

div.stButton > button:hover {
    opacity: 0.88;
    color: white;
}

/* Secondary / back button style */
div[data-testid="stButton"] button[kind="secondary"] {
    background: rgba(255,255,255,0.06);
    color: #d8d6ee;
    border: 1px solid rgba(255,255,255,0.12);
}

hr {
    border-color: rgba(255,255,255,0.08);
}

/* ---------- Defensive: prevent any stray empty Streamlit containers
   from showing a visible border/background. Without this, certain
   Streamlit versions render an empty rounded box for columns/containers
   that have no visible child yet (e.g. during a rerun transition). ---------- */
div[data-testid="stVerticalBlockBorderWrapper"]:empty,
div[data-testid="stVerticalBlock"]:empty,
div[data-testid="stColumn"]:empty,
div[data-testid="stHorizontalBlock"]:empty {
    display: none !important;
    border: none !important;
    background: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}

.footer-text {
    text-align: center;
    color: #6c6886;
    font-size: 0.78rem;
    margin-top: 30px;
}
</style>
"""


def get_css() -> str:
    """Return the full CSS block to inject once per page via st.markdown."""
    return CUSTOM_CSS

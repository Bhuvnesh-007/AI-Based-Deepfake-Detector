"""
app.py
Deepfake Detector — single-file-routed Streamlit app (Home / How It Works / About).

Run with:
    streamlit run app.py
"""

import streamlit as st
from PIL import Image
import plotly.graph_objects as go

from style import get_css
from model_utils import load_model, predict
from pages_content import render_how_it_works, render_about

# -----------------------------------------------------------------
# Page config — must be the first Streamlit call
# -----------------------------------------------------------------
st.set_page_config(
    page_title="Deepfake Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(get_css(), unsafe_allow_html=True)

# Hide Streamlit's default sidebar nav / sidebar entirely since we use a custom navbar
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------
# Session state — routing + history
# -----------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {name, label, confidence, thumb}
if "result" not in st.session_state:
    st.session_state.result = None
if "model" not in st.session_state:
    st.session_state.model, st.session_state.model_load_error = load_model()


def go_to(page_name: str):
    st.session_state.page = page_name


# -----------------------------------------------------------------
# Custom navbar (rendered with real Streamlit buttons laid out via columns,
# styled via CSS to look like the navbar in the mockups)
# -----------------------------------------------------------------

def render_navbar(active: str):
    nav_html_open = """
    <div class="navbar">
        <div class="navbar-brand">
            <div class="logo-badge">D</div>
            <div>
                DEEPFAKE
                <span class="brand-sub">DETECTOR</span>
            </div>
        </div>
    </div>
    """
    # We render brand via HTML, and nav buttons via Streamlit columns positioned
    # right after, to keep click handling native and reliable.
    st.markdown(nav_html_open, unsafe_allow_html=True)

    cols = st.columns([5, 1, 1.3, 1, 1.6])
    with cols[1]:
        if st.button("Home", width='stretch',
                      type="primary" if active == "home" else "secondary"):
            go_to("home")
            st.rerun()
    with cols[2]:
        if st.button("How It Works", width='stretch',
                      type="primary" if active == "how" else "secondary"):
            go_to("how")
            st.rerun()
    with cols[3]:
        if st.button("About", width='stretch',
                      type="primary" if active == "about" else "secondary"):
            go_to("about")
            st.rerun()
    with cols[4]:
        if st.button("+ New Analysis", width='stretch', type="primary"):
            st.session_state.result = None
            go_to("home")
            st.rerun()


# -----------------------------------------------------------------
# Confidence donut chart (Plotly) — mimics the circular gauge in mockup
# -----------------------------------------------------------------
def render_confidence_donut(confidence: float, label: str):
    color = "#36c9ff" if label == "FAKE" else "#4ade80"
    status_text = "AI GENERATED" if label == "FAKE" else "AUTHENTIC"
    fig = go.Figure(go.Pie(
        values=[confidence, 100 - confidence],
        hole=0.78,
        rotation=90,
        marker=dict(colors=[color, "rgba(255,255,255,0.06)"]),
        textinfo="none",
        hoverinfo="skip",
        sort=False,
    ))
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[
            dict(
                text=status_text,
                x=0.5, y=0.58, showarrow=False,
                font=dict(size=13, color="#cfcfe6", family="Inter, sans-serif"),
                xanchor="center", yanchor="middle",
            ),
            dict(
                text=f"{confidence:.0f}%",
                x=0.5, y=0.48, showarrow=False,
                font=dict(size=36, color="white", family="Inter, sans-serif"),
                xanchor="center", yanchor="middle",
            ),
            dict(
                text="CONFIDENCE SCORE",
                x=0.5, y=0.38, showarrow=False,
                font=dict(size=10, color="#9c98b8", family="Inter, sans-serif"),
                xanchor="center", yanchor="middle",
            ),
        ],
    )
    st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})


# -----------------------------------------------------------------
# HOME PAGE
# -----------------------------------------------------------------
def render_home():
    st.markdown('<div class="page-title">Welcome to Deepfake Detector</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Upload an image and our AI model will analyze it for signs of AI generation or manipulation.</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.get("model_load_error"):
        err_text = st.session_state.model_load_error
        err_preview = err_text if len(err_text) < 300 else err_text[:300] + "... (see terminal for full traceback)"
        st.error(
            f"⚠️ Found `model/deepfake_model.pth` but failed to load it:\n\n"
            f"`{err_preview}`\n\n"
            f"Check that the architecture in `model_utils.py` (timm `vit_base_patch16_224`, "
            f"num_classes=2) matches how the model was trained.",
            icon="🚨",
        )

    left, right = st.columns([1, 1.05], gap="large")

    with left:
        with st.container(border=True):
            st.markdown("### Upload Image")
            st.markdown(
                '<p style="color:#9c98b8;font-size:0.9rem;">Upload an image to analyze whether it has been AI generated or manipulated.</p>',
                unsafe_allow_html=True,
            )

            uploaded_file = st.file_uploader(
                "Drag & drop an image here, or click to browse",
                type=["jpg", "jpeg", "png", "webp"],
                label_visibility="visible",
            )
            st.markdown(
                '<div class="upload-hint">Supported formats: JPG, PNG, WEBP (Max 10MB)</div>',
                unsafe_allow_html=True,
            )

            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded image", width='stretch')

                analyze_clicked = st.button("🔍 Analyze Image", width='stretch', type="primary")
                if analyze_clicked:
                    with st.spinner("Running deepfake analysis..."):
                        result = predict(st.session_state.model, image)
                        result["filename"] = uploaded_file.name
                        st.session_state.result = result

                        # store a small thumbnail copy for "recently analyzed"
                        st.session_state.history.insert(0, {
                            "name": uploaded_file.name,
                            "label": result["label"],
                            "confidence": result["confidence"],
                        })
                        st.session_state.history = st.session_state.history[:6]
                    st.rerun()

            # Recently analyzed strip
            if st.session_state.history:
                st.markdown("---")
                st.markdown("**Recently Analyzed**")
                hist_cols = st.columns(len(st.session_state.history))
                for c, item in zip(hist_cols, st.session_state.history):
                    with c:
                        badge_class = "badge-pill" if item["label"] == "REAL" else "badge-pill fake"
                        st.markdown(
                            f"<div style='font-size:0.7rem;color:#9c98b8;text-align:center;'>{item['name'][:12]}</div>"
                            f"<div style='text-align:center;'><span class='{badge_class}'>{item['label']} {item['confidence']:.0f}%</span></div>",
                            unsafe_allow_html=True,
                        )

            st.markdown(
                '<p style="color:#6c6886;font-size:0.78rem;margin-top:14px;">🔒 Your images are private and secure. We do not store or share your uploads.</p>',
                unsafe_allow_html=True,
            )

    with right:
        with st.container(border=True):
            result = st.session_state.result

            header_l, header_r = st.columns([3, 1])
            with header_l:
                st.markdown("### Analysis Results")
                st.markdown(
                    '<p style="color:#9c98b8;font-size:0.9rem;">Our AI has analyzed the image</p>',
                    unsafe_allow_html=True,
                )
            with header_r:
                if result is not None:
                    st.markdown(
                        '<div style="text-align:right;margin-top:8px;"><span class="badge-pill">✓ Completed</span></div>',
                        unsafe_allow_html=True,
                    )

            if result is None:
                st.markdown(
                    '<div style="text-align:center;padding:60px 10px;color:#6c6886;">'
                    'Upload and analyze an image to see results here.</div>',
                    unsafe_allow_html=True,
                )
            else:
                if result.get("demo"):
                    st.info("⚠️ Demo mode: no trained model weights found at `model/deepfake_model.pth` yet. Showing placeholder results — upload your `.pth` file to get real predictions.", icon="⚠️")

                render_confidence_donut(result["confidence"], result["label"])

                st.markdown("**Confidence Level**")
                st.slider(
                    "Confidence", 0, 100, int(result["confidence"]),
                    disabled=True, label_visibility="collapsed",
                )

    st.markdown(
        '<div class="footer-text">© 2026 Deepfake Detector. All rights reserved.</div>',
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------
# ROUTER
# -----------------------------------------------------------------
render_navbar(st.session_state.page)

if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "how":
    render_how_it_works(go_to)
elif st.session_state.page == "about":
    render_about(go_to)

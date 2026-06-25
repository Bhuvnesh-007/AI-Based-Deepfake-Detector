"""
pages_content.py
Render functions for the "How It Works" and "About" pages.
Both take a `go_to` callback so the Back button can route to Home.
"""

import streamlit as st


def render_how_it_works(go_to):
    if st.button("← Back to Home"):
        go_to("home")
        st.rerun()

    st.markdown('<div class="page-title">How It Works</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Our AI analyzes multiple indicators to detect deepfakes with high accuracy.</div>',
        unsafe_allow_html=True,
    )

    steps = [
        ("1", "📤", "Upload Your Image",
         "Upload an image you want to analyze. We support JPG, PNG, and WEBP formats (Max 10MB)."),
        ("2", "🧠", "AI Analysis",
         "Our advanced AI model examines multiple aspects of the image including facial patterns, texture, lighting, shadows, and more."),
        ("3", "🔍", "Pattern Detection",
         "We detect subtle inconsistencies and anomalies that are often invisible to the human eye but indicate AI generation or manipulation."),
        ("4", "🛡️", "Results & Confidence Score",
         "Get a clear result with a confidence score and detailed breakdown of our analysis across key factors."),
    ]

    for num, icon, title, desc in steps:
        st.markdown(
            f"""
            <div class="step-row">
                <div class="step-num">{num}</div>
                <div class="step-icon">{icon}</div>
                <div class="step-content">
                    <h4>{title}</h4>
                    <p>{desc}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="glass-card" style="display:flex;align-items:center;gap:16px;margin-top:8px;">
            <div style="font-size:1.6rem;">💡</div>
            <div>
                <h3 style="margin:0;">Built with Advanced AI</h3>
                <p style="margin:0;">Our model is trained on thousands of real and AI-generated images to deliver reliable and up-to-date detection.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="footer-text">© 2026 Deepfake Detector. All rights reserved.</div>', unsafe_allow_html=True)


def render_about(go_to):
    if st.button("← Back to Home"):
        go_to("home")
        st.rerun()

    st.markdown('<div class="page-title">About Deepfake Detector</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Deepfake Detector is an AI-powered tool designed to help you identify AI-generated or manipulated images with accuracy and ease.</div>',
        unsafe_allow_html=True,
    )

    # --- Top 3 mini feature cards ---
    feats = [
        ("🎯", "#a78bfa", "High Accuracy", "Advanced AI models trained on millions of images."),
        ("🛡️", "#38bdf8", "Privacy Focused", "Your uploads are private and never stored or shared."),
        ("⚡", "#facc15", "Fast Results", "Get results in seconds with detailed analysis and insights."),
    ]
    cols = st.columns(3)
    for c, (icon, color, title, desc) in zip(cols, feats):
        with c:
            st.markdown(
                f"""
                <div class="mini-card">
                    <div class="icon-circle" style="background:{color}22;color:{color};">{icon}</div>
                    <h4>{title}</h4>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Mission / Why it matters / Technology ---
    # NOTE: Personalize the text below with your own story — why you built this,
    # what inspired the idea, your background, etc.
    sections = [
        ("🚩", "Our Mission",
         "To build a safer digital world by empowering people with tools to detect AI-generated content and misinformation."),
        ("✅", "Why It Matters",
         "AI-generated content is becoming more advanced every day. My goal is to bring transparency and trust to digital media by making deepfake detection accessible to everyone."),
        ("💻", "Technology",
         "This detection engine uses a deep learning model built with PyTorch that analyzes multiple visual cues — including facial structure, pixel patterns, lighting, texture, and more — allowing it to identify even subtle signs of manipulation."),
    ]
    for icon, title, desc in sections:
        st.markdown(
            f"""
            <div style="display:flex;gap:14px;margin-bottom:18px;">
                <div style="font-size:1.3rem;">{icon}</div>
                <div>
                    <h3 style="margin:0;color:#f5f5ff;font-size:1.05rem;">{title}</h3>
                    <p style="margin:0;color:#9c98b8;font-size:0.9rem;">{desc}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- TODO: your personal story ---
    st.markdown(
        """
        <div class="glass-card">
            <h3>My Story</h3>
            <p>
                I have always been fascinated by how incredibly realistic AI-generated images look. However, I soon realized the darker side of this technology—how easily these synthetic images can be misused in cybercrimes, identity fraud, and misinformation campaigns. Driven to find a solution to this growing threat, I decided to counter AI with AI. During my internship, I channeled this idea into developing a Deep Learning-based Deepfake Face Detector, creating a robust tool designed to identify and flag synthetic media effectively.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- Stat tiles ---
    st.markdown("<br>", unsafe_allow_html=True)
    stat_cols = st.columns(4)
    stats = [
        ("👥", "1Lac+", "Images Analyzed"),
        ("📈", "95.4%+", "Detection Accuracy"),
        ("⏱️", "2s", "Average Analysis Time"),
        ("🛡️", "24/7", "Always Improving"),
    ]
    for c, (icon, num, label) in zip(stat_cols, stats):
        with c:
            st.markdown(
                f"""
                <div class="glass-card stat-tile">
                    <div style="font-size:1.3rem;">{icon}</div>
                    <div class="stat-num">{num}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="footer-text">© 2026 Deepfake Detector. All rights reserved.</div>', unsafe_allow_html=True)

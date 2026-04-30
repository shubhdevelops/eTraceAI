# app/dashboard.py

import os
import sys
import subprocess

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from Bio import SeqIO

# Allow imports from project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# =====================================================================
# PAGE CONFIG
# =====================================================================
st.set_page_config(
    page_title="eTraceAI",
    page_icon="🧬",
    layout="wide"
)

# =====================================================================
# CUSTOM CSS - MODERN DESIGN
# =====================================================================
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;600;700&display=swap');

/* Global Styles */
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Sidebar Styling */
.sidebar .sidebar-content {
    background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    color: white;
}

/* Main Title with Gradient */
.main-title {
    font-size: 56px;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-family: 'Poppins', sans-serif;
    letter-spacing: -1px;
    margin-bottom: 0;
    animation: fadeInDown 1s ease-out;
}

/* Subtitle */
.subtitle {
    font-size: 20px;
    color: #64748b;
    margin-top: 8px;
    font-weight: 400;
    animation: fadeIn 1.5s ease-out;
}

/* Section Title */
.section-title {
    font-size: 32px;
    font-weight: 700;
    margin-top: 30px;
    margin-bottom: 20px;
    color: #1e293b;
    font-family: 'Poppins', sans-serif;
    position: relative;
    padding-bottom: 12px;
}

.section-title::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 60px;
    height: 4px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border-radius: 2px;
}

/* Modern Card Design */
.card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    padding: 30px;
    border-radius: 20px;
    border: none;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
    margin-bottom: 25px;
    transition: all 0.3s ease;
    animation: fadeInUp 0.6s ease-out;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.15);
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 25px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: scale(1.05);
    box-shadow: 0 12px 48px rgba(102, 126, 234, 0.4);
}

/* Button Styling */
.stButton>button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 32px;
    font-weight: 600;
    font-size: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* File Uploader */
.uploadedFile {
    border-radius: 12px;
    border: 2px dashed #667eea;
    padding: 20px;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    margin-top: 60px;
    padding: 25px;
    font-size: 15px;
    border-top: 1px solid #e2e8f0;
    background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
    border-radius: 16px;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Progress Bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}

/* Radio Buttons */
.stRadio > label {
    background: white;
    padding: 12px 20px;
    border-radius: 10px;
    margin: 5px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

.stRadio > label:hover {
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.2);
    transform: translateY(-2px);
}

/* DataFrames */
.dataframe {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* Success/Info Messages */
.stSuccess, .stInfo, .stWarning {
    border-radius: 12px;
    padding: 16px;
    animation: fadeInUp 0.5s ease-out;
}
</style>
""", unsafe_allow_html=True)

# Hide Streamlit chrome
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# NAVIGATION
# =====================================================================
st.markdown("""
<style>
.nav-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 15px 25px;
    border-radius: 16px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
}
</style>
""", unsafe_allow_html=True)

nav_options = ["🏠 Home", "📊 Results", "🎨 Visualizations", "🧬 FASTA Preview", "👨‍💻 Developer Info"]
page = st.selectbox("🧭 Navigate to Section", nav_options)
st.markdown("<br>", unsafe_allow_html=True)

# =====================================================================
# PATHS
# =====================================================================
UPLOAD_PATH = "data/sample1.fasta"
RESULT_CSV = "output/match_results.csv"
EMB_PATH = "output/dbn_embeddings.npy"

# Multi-level taxonomy images generated by phylum_barplot.py
TAXON_IMAGES = {
    "Phylum": ("output/phylum_barplot_total.png", "output/phylum_barplot_novel.png"),
    "Class": ("output/class_barplot_total.png", "output/class_barplot_novel.png"),
    "Order": ("output/order_barplot_total.png", "output/order_barplot_novel.png"),
    "Family": ("output/family_barplot_total.png", "output/family_barplot_novel.png"),
    "Genus": ("output/genus_barplot_total.png", "output/genus_barplot_novel.png"),
}

# =====================================================================
# HEADER
# =====================================================================
st.markdown('<div class="main-title">eTraceAI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-powered Environmental DNA Analysis & Deep-Sea Novelty Detection</div>',
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)

# =====================================================================
# HOME TAB
# =====================================================================
if page == "🏠 Home":

    st.markdown('<div class="section-title">Upload FASTA</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">Upload your eDNA FASTA file to begin AI-based classification.</div>',
                unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Select FASTA File", type=["fasta", "fa"])

    if uploaded_file:
        with open(UPLOAD_PATH, "wb") as f:
            f.write(uploaded_file.read())

        st.success("FASTA uploaded successfully.")

        with st.spinner("Running eTraceAI pipeline…"):
            subprocess.run(["python", "app/taxonomy_matcher.py"])
            subprocess.run(["python", "app/cluster.py"])
            subprocess.run(["python", "app/phylum_barplot.py"])

        st.success("Processing complete. Check Results & Visualizations tabs.")

# =====================================================================
# RESULTS TAB
# =====================================================================
elif page == "📊 Results":

    st.markdown('<div class="section-title">Taxonomic Match Results</div>', unsafe_allow_html=True)

    if os.path.exists(RESULT_CSV):

        df = pd.read_csv(RESULT_CSV)

        # Ensure all expected model columns exist
        required_cols = [
            "DL_MarineScore", "HybridScore", "NoveltyScore",
            "NoveltyType", "HabitatConsensus", "ConfidenceScore"
        ]
        for col in required_cols:
            if col not in df.columns:
                df[col] = 0.0 if "Score" in col else "Unknown"

        total = len(df)
        n_marine = (df["DL_MarineScore"] > 0.7).sum()
        n_novel = (df["NoveltyScore"] > 0.6).sum()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total sequences", total)
        c2.metric("Marine-like (DL > 0.7)", n_marine)
        c3.metric("Potential novel (Novelty > 0.6)", n_novel)

        st.markdown("### 🔍 Filter Results")

        filter_type = st.radio(
            "Choose filter:",
            [
                "Show All",
                "Novel Sequences (NoveltyScore > 0.6)",
                "High-Confidence Marine (DL_MarineScore > 0.7)",
                "High-Confidence Non-Marine (DL_MarineScore < 0.3)",
                "Ambiguous (0.3–0.7 Marine Probability)",
            ],
            horizontal=True,
        )

        filtered = df.copy()
        if filter_type == "Novel Sequences (NoveltyScore > 0.6)":
            filtered = df[df["NoveltyScore"] > 0.6]
        elif filter_type == "High-Confidence Marine (DL_MarineScore > 0.7)":
            filtered = df[df["DL_MarineScore"] > 0.7]
        elif filter_type == "High-Confidence Non-Marine (DL_MarineScore < 0.3)":
            filtered = df[df["DL_MarineScore"] < 0.3]
        elif filter_type == "Ambiguous (0.3–0.7 Marine Probability)":
            filtered = df[(df["DL_MarineScore"] >= 0.3) & (df["DL_MarineScore"] <= 0.7)]

        st.write(f"### Showing **{len(filtered)}** sequences")
        st.dataframe(filtered, use_container_width=True)

        st.download_button(
            "Download Filtered CSV",
            data=filtered.to_csv(index=False).encode(),
            file_name="filtered_results.csv",
        )

        # =====================================================
        # TAXONOMY MULTI-LEVEL BARPLOTS (Phylum → Genus)
        # =====================================================
        st.markdown('<div class="section-title">Taxonomy Insights (Phylum → Genus)</div>',
                    unsafe_allow_html=True)

        with st.expander("📊 Show Biodiversity Barplots (All Ranks)"):
            for rank, (total_path, novel_path) in TAXON_IMAGES.items():
                st.markdown(f"### {rank} Distribution")

                cols = st.columns(2)
                if os.path.exists(total_path):
                    cols[0].image(total_path, caption=f"{rank} (All)", use_column_width=True)
                if os.path.exists(novel_path):
                    cols[1].image(novel_path, caption=f"{rank} (Novel Only)", use_column_width=True)

    else:
        st.info("Upload a FASTA file first.")

# =====================================================================
# VISUALIZATION TAB
# =====================================================================
elif page == "🎨 Visualizations":

    st.markdown('<div class="section-title">UMAP Cluster Visualization</div>', unsafe_allow_html=True)

    if os.path.exists(EMB_PATH) and os.path.exists(RESULT_CSV):

        df = pd.read_csv(RESULT_CSV)
        embeddings = np.load(EMB_PATH)

        reducer = __import__("umap").UMAP(n_components=2, random_state=42)
        reduced = reducer.fit_transform(embeddings)

        plot_df = pd.DataFrame({
            "x": reduced[:, 0],
            "y": reduced[:, 1],
            "Organism": df["Organism"],
            "DL_MarineScore": df["DL_MarineScore"],
            "NoveltyScore": df["NoveltyScore"],
            "NoveltyType": df["NoveltyType"],
        })

        fig = px.scatter(
            plot_df,
            x="x", y="y",
            color="NoveltyScore",
            hover_data=["Organism", "DL_MarineScore", "NoveltyScore", "NoveltyType"],
            color_continuous_scale="Turbo",
            title="UMAP Projection (DBN Embeddings + Novelty Analysis)",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Potential Novel Sequences")
        novels = plot_df[plot_df["NoveltyScore"] > 0.6]
        if len(novels) > 0:
            st.warning(f"🔍 {len(novels)} potential novel sequences detected")
            st.dataframe(novels)
        else:
            st.success("No strongly novel sequences identified.")

    else:
        st.info("Run analysis first.")

# =====================================================================
# FASTA PREVIEW TAB
# =====================================================================
elif page == "🧬 FASTA Preview":
    st.markdown('<div class="section-title">FASTA Preview</div>', unsafe_allow_html=True)

    if os.path.exists(UPLOAD_PATH):
        seqs = list(SeqIO.parse(UPLOAD_PATH, "fasta"))
        st.write(f"Total sequences detected: **{len(seqs)}**")

        for rec in seqs[:5]:
            st.code(f">{rec.id}\n{str(rec.seq)[:300]}...")

    else:
        st.info("Upload FASTA first.")

# =====================================================================
# DEVELOPER TAB
# =====================================================================
elif page == "👨‍💻 Developer Info":
    st.markdown('<div class="section-title">About eTraceAI</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3 style="color: #667eea; margin-bottom: 15px;">🧬 Project Overview</h3>
        <p style="font-size: 16px; line-height: 1.6; color: #475569;">
        eTraceAI is an advanced AI-powered platform for Environmental DNA (eDNA) analysis and
        deep-sea biodiversity assessment. The system combines deep learning models with traditional
        bioinformatics tools to identify and classify marine species from eDNA samples.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="color: #667eea; margin-bottom: 15px;">👥 Team Information</h3>
            <p><strong>Team Name:</strong> CRISPR_CREW</p>
            <p><strong>Competition:</strong> Smart India Hackathon – Grand Finale</p>
            <p><strong>Institution:</strong> NIT Raipur</p>
            <p><strong>Developer:</strong> Shubham Thakur</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3 style="color: #667eea; margin-bottom: 15px;">🛠️ Technology Stack</h3>
            <p><strong>Frontend:</strong> Streamlit</p>
            <p><strong>ML/DL:</strong> PyTorch, Scikit-learn</p>
            <p><strong>Bioinformatics:</strong> BioPython, BLAST+</p>
            <p><strong>Visualization:</strong> Plotly, UMAP</p>
            <p><strong>Deployment:</strong> Docker</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3 style="color: #667eea; margin-bottom: 15px;">✨ Key Features</h3>
        <ul style="font-size: 16px; line-height: 1.8; color: #475569;">
            <li>🔬 Deep learning-based marine species classification</li>
            <li>🧪 Novel sequence detection and analysis</li>
            <li>📊 Multi-level taxonomic visualization (Phylum to Genus)</li>
            <li>🎯 UMAP-based clustering and dimensionality reduction</li>
            <li>⚡ Real-time processing pipeline</li>
            <li>📈 Interactive data exploration and filtering</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =====================================================================
# FOOTER
# =====================================================================
st.markdown(
    '<div class="footer">© eTraceAI | Deep Sea Biodiversity Intelligence Platform</div>',
    unsafe_allow_html=True,
)

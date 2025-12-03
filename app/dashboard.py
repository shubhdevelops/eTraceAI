import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import os
import subprocess



from Bio import SeqIO

# =====================================================================
# PAGE CONFIG
# =====================================================================
st.set_page_config(
    page_title="eTraceAI",
    page_icon="🧬",
    layout="wide"
)

# =====================================================================
# CUSTOM CSS (clean scientific UI)
# =====================================================================
st.markdown("""
<style>
body {
    font-family: 'Segoe UI', sans-serif;
}

.sidebar .sidebar-content {
    background-color: #f3f6f9;
}

.main-title {
    font-size: 42px;
    font-weight: 700;
    color: #2E7D32;
    padding-bottom: 0;
}

.subtitle {
    font-size: 18px;
    color: #555;
    margin-top: -12px;
}

.section-title {
    font-size: 26px;
    font-weight: 600;
    margin-top: 15px;
    color: #1B5E20;
}

.card {
    background-color: #f7f9fc;
    color:#000;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #e6e6e6;
    margin-bottom: 20px;
}

.footer {
    text-align:center;
    color:#777;
    margin-top:40px;
    padding: 15px;
    font-size:14px;
}
</style>
""", unsafe_allow_html=True)


# =====================================================================
# SIDEBAR
# =====================================================================
st.sidebar.title("eTraceAI")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Results", "Visualizations", "FASTA Preview", "Developer Info"]
)

# Paths
UPLOAD_PATH = "data/sample1.fasta"
RESULT_CSV = "output/match_results.csv"
CLUSTER_IMG = "output/clusters_umap.png"

# =====================================================================
# HEADER
# =====================================================================
st.markdown('<div class="main-title">eTraceAI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered Environmental DNA Analysis & Biodiversity Intelligence</div>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# =====================================================================
# HOME TAB
# =====================================================================
if page == "Home":

    st.markdown('<div class="section-title">Upload FASTA</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">Upload your eDNA FASTA file to begin AI-based classification.</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Select FASTA File", type=["fasta", "fa"])

    if uploaded_file:
        with open(UPLOAD_PATH, "wb") as f:
            f.write(uploaded_file.read())

        st.success("FASTA uploaded successfully.")

        with st.spinner("Running eTraceAI pipeline…"):
            subprocess.run(["python", "app/taxonomy_matcher.py"])
            subprocess.run(["python", "app/cluster.py"])

        st.success("Processing complete. Check Results & Visualizations tabs.")

# =====================================================================
# RESULTS TAB
# =====================================================================
elif page == "Results":

    st.markdown('<div class="section-title">Taxonomic Match Results</div>', unsafe_allow_html=True)

    if os.path.exists(RESULT_CSV):
        df = pd.read_csv(RESULT_CSV)
        st.dataframe(df, use_container_width=True)

        # Download CSV
        csv_bytes = df.to_csv(index=False).encode()
        st.download_button("Download Results CSV", data=csv_bytes, file_name="taxonomy_results.csv")

        # Phylum distribution
        st.markdown('<div class="section-title">Phylum Distribution</div>', unsafe_allow_html=True)
        df["Phylum"] = df["Lineage"].str.split().str[2]
        counts = df["Phylum"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 4))
        counts.plot(kind="bar", color="#2E7D32", ax=ax)
        st.pyplot(fig)
    else:
        st.info("Upload a FASTA file first.")

# =====================================================================
# VISUALIZATION TAB
# =====================================================================
elif page == "Visualizations":

    st.markdown('<div class="section-title">UMAP Cluster Visualization</div>', unsafe_allow_html=True)

    if os.path.exists(RESULT_CSV) and os.path.exists("vector_matrix.npy"):

        df = pd.read_csv(RESULT_CSV)
        matrix = np.load("vector_matrix.npy")

        # Use Plotly for interactive UMAP
        if os.path.exists(CLUSTER_IMG):  # show static PNG too
            st.image(CLUSTER_IMG, caption="Static UMAP Plot", use_column_width=True)

        # Interactive UMAP if 2+ points
        if matrix.shape[0] > 1:
            reducer = __import__("umap").UMAP(n_components=2, random_state=42)
            reduced = reducer.fit_transform(matrix)

            plot_df = pd.DataFrame({
                "x": reduced[:, 0],
                "y": reduced[:, 1],
                "Organism": df["Organism"]
            })

            fig = px.scatter(
                plot_df, x="x", y="y", hover_data=["Organism"],
                title="Interactive UMAP Visualization",
                color="Organism"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Only one sequence found — clustering not applicable.")
    else:
        st.info("Run analysis first.")

# =====================================================================
# FASTA PREVIEW TAB
# =====================================================================
elif page == "FASTA Preview":

    st.markdown('<div class="section-title">FASTA Preview</div>', unsafe_allow_html=True)

    if os.path.exists(UPLOAD_PATH):
        st.markdown('<div class="card">Showing first few sequences from uploaded FASTA.</div>', unsafe_allow_html=True)

        seqs = list(SeqIO.parse(UPLOAD_PATH, "fasta"))
        st.write(f"Total sequences detected: **{len(seqs)}**")

        for i, record in enumerate(seqs[:5]):
            st.code(f">{record.id}\n{str(record.seq)[:200]}...")
    else:
        st.info("Upload a FASTA file first.")

# =====================================================================
# DEVELOPER TAB
# =====================================================================

elif page == "Developer Info":

    st.subheader("Team: CRISPR_CREW")

    st.write("### Smart India Hackathon (SIH) – Grand Finale")
    st.write("National Institute of Technology, Raipur")
    st.write("---")

    st.write("### Developer")
    st.write("**Shubham Thakur**  \n(nitian.shubh@gmail.com)")

    st.write("### Team Members")
    st.write("- Sameer Srivastava")
    st.write("- Abhishek Kumar")
    st.write("- Sanju Rohilla")
    st.write("- Ritu Bhoi")
    st.write("- Saloni Chauhan")







# =====================================================================
# FOOTER
# =====================================================================
st.markdown('<div class="footer">© eTraceAI | Deep Sea Biodiversity Intelligence Platform</div>', unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Bio import SeqIO
import os
import subprocess

# Paths
UPLOAD_PATH = "data/sample1.fasta"
RESULT_CSV = "output/match_results.csv"
CLUSTER_IMG = "output/clusters_umap.png"

st.title("eDNA Taxonomy Explorer")

# --- Upload FASTA ---
uploaded_file = st.file_uploader("Upload a FASTA File", type=["fasta", "fa"])
if uploaded_file is not None:
    with open(UPLOAD_PATH, "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ File uploaded. Running analysis...")

    # --- Run your pipeline ---
    with st.spinner("🔬 Running backend analysis..."):
        subprocess.run(["python", "app/taxonomy_matcher.py"])
        subprocess.run(["python", "app/cluster.py"])

    st.success("✅ Analysis complete!")

    # --- Display Table ---
    if os.path.exists(RESULT_CSV):
        df = pd.read_csv(RESULT_CSV)
        st.subheader("📋 Match Results")
        st.dataframe(df)

        # --- Bar Plot of Phylum ---
        st.subheader("🧬 Phylum Distribution")
        df["Phylum"] = df["Lineage"].str.split().str[2]  # Simplified
        phylum_counts = df["Phylum"].value_counts()
        fig, ax = plt.subplots()
        phylum_counts.plot(kind="bar", ax=ax)
        ax.set_ylabel("Count")
        st.pyplot(fig)

        # --- Cluster Visualization ---
        if os.path.exists(CLUSTER_IMG):
            st.subheader("📊 Clustering Visualization")
            st.image(CLUSTER_IMG, caption="eDNA Clusters", use_column_width=True)

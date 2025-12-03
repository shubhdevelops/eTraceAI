import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from sklearn.cluster import AgglomerativeClustering
import umap

MATRIX_PATH = "vector_matrix.npy"
LABELS_PATH = "output/match_results.csv"
OUTPUT_PATH = "output/clusters_umap.png"

def load_data():
    matrix = np.load(MATRIX_PATH)
    df = pd.read_csv(LABELS_PATH)
    labels = df["Organism"].tolist()
    return matrix, labels

def cluster_and_plot(matrix, labels, n_clusters=4):
    reducer = umap.UMAP(n_components=2, random_state=42)
    reduced = reducer.fit_transform(matrix)

    clusterer = AgglomerativeClustering(n_clusters=n_clusters)
    clusters = clusterer.fit_predict(reduced)

    plt.figure(figsize=(10, 7))
    for i in range(n_clusters):
        points = reduced[clusters == i]
        plt.scatter(points[:, 0], points[:, 1], label=f"Cluster {i+1}")

    for i, label in enumerate(labels):
        plt.annotate(label, (reduced[i, 0], reduced[i, 1]), fontsize=7, alpha=0.6)

    plt.title("eDNA Clusters (UMAP + Agglomerative Clustering)")
    plt.legend()
    plt.tight_layout()
    os.makedirs("output", exist_ok=True)
    plt.savefig(OUTPUT_PATH)
    print(f"✅ Saved UMAP cluster plot to {OUTPUT_PATH}")

if __name__ == "__main__":
    matrix, labels = load_data()
    cluster_and_plot(matrix, labels)

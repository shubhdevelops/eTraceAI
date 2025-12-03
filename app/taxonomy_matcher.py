from Bio import SeqIO, Entrez
from collections import Counter
import os
import numpy as np
import ssl
import csv
from sklearn.metrics.pairwise import cosine_similarity

# Fix SSL issues for NCBI
ssl._create_default_https_context = ssl._create_unverified_context

# --- Parameters ---
K = 5
SAMPLE_FASTA = "data/sample1.fasta"
REF_FASTA = "data/ref_10.fasta"
Entrez.email = "nitian.shubh@gmail.com"
Entrez.api_key = "83f10df2a4a230047ef71cc9d48043c63508"

# --- k-mer extraction ---
def get_kmers(seq, k):
    return [seq[i:i + k] for i in range(len(seq) - k + 1)]

# --- Parse FASTA and convert to vectors ---
def fasta_to_vectors(fasta_file, k):
    vectors = []
    labels = []
    count = 0
    for record in SeqIO.parse(fasta_file, "fasta"):
        kmers = get_kmers(str(record.seq).upper(), k)
        if not kmers:
            continue
        freq = Counter(kmers)
        vectors.append(freq)
        labels.append(record.id)
        count += 1
        if count % 100 == 0:
            print(f"  Processed {count} sequences from {fasta_file}")
    if not vectors:
        raise ValueError(f"❌ No valid sequences parsed from {fasta_file}")
    return vectors, labels

# --- Convert sparse k-mer dicts to dense matrix ---
def to_dense_matrix_pair(sample_vecs, ref_vecs):
    all_kmers = sorted(set(k for vec in (sample_vecs + ref_vecs) for k in vec))
    def vec_to_row(vec):
        return [vec.get(k, 0) for k in all_kmers]
    sample_matrix = np.array([vec_to_row(v) for v in sample_vecs])
    ref_matrix = np.array([vec_to_row(v) for v in ref_vecs])
    return sample_matrix, ref_matrix

# --- Fetch taxonomy details from NCBI ---
def fetch_taxonomy_details(genbank_id):
    try:
        handle = Entrez.efetch(db="nucleotide", id=genbank_id, rettype="gb", retmode="text")
        gb_text = handle.read()
        handle.close()

        lines = gb_text.splitlines()
        organism = "Unknown"
        lineage_lines = []
        capture = False

        for line in lines:
            if line.strip().startswith("ORGANISM"):
                organism = line.strip().split("  ")[-1]
                capture = True
                continue
            if capture:
                if line.startswith(" " * 12):  # Continuation lines
                    lineage_lines.append(line.strip())
                else:
                    break

        lineage = " ".join(lineage_lines).replace(";", "")
        return organism, lineage
    except Exception as e:
        return "Error", f"Error: {str(e)}"

# --- Main execution ---
if __name__ == "__main__":
    print("Vectorizing sample...")
    sample_vecs, sample_ids = fasta_to_vectors(SAMPLE_FASTA, K)

    print("Vectorizing reference...")
    ref_vecs, ref_ids = fasta_to_vectors(REF_FASTA, K)

    print("Finished vectorization. Computing similarities...")
    sample_matrix, ref_matrix = to_dense_matrix_pair(sample_vecs, ref_vecs)
    sim_matrix = cosine_similarity(sample_matrix, ref_matrix)

    os.makedirs("output", exist_ok=True)
    np.save("vector_matrix.npy", sample_matrix)
    with open("vector_labels.txt", "w") as f:
        for sid in sample_ids:
            f.write(sid + "\n")

    print("\nMatches:")
    with open("output/match_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["SampleID", "MatchedID", "Organism", "Lineage", "Score"])
        for i, row in enumerate(sim_matrix):
            best_match = np.argmax(row)
            confidence = row[best_match]
            genbank_id = ref_ids[best_match]
            organism, lineage = fetch_taxonomy_details(genbank_id)
            print(f"{sample_ids[i]} → {genbank_id} ({organism}) (Score: {confidence:.3f})")
            writer.writerow([sample_ids[i], genbank_id, organism, lineage, f"{confidence:.3f}"])

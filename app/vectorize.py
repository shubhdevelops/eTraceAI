from Bio import SeqIO
from collections import Counter
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

K = 6
SAMPLE_FASTA = "data/sample1.fasta"
REF_FASTA = "data/strong_reference.fasta"  # make sure this path matches your merged file
MATCH_THRESHOLD = 0.05  # optional threshold to filter noise

def get_kmers(seq, k):
    return [seq[i:i+k] for i in range(len(seq) - k + 1)]

def fasta_to_vectors(fasta_file, k):
    vectors = []
    labels = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        kmers = get_kmers(str(record.seq).upper(), k)
        freq = Counter(kmers)
        vectors.append(freq)
        labels.append(record.id)
    return vectors, labels

def to_dense_matrix_pair(sample_vecs, ref_vecs):
    all_kmers = sorted(set(k for vec in (sample_vecs + ref_vecs) for k in vec))
    
    def vec_to_row(vec):
        return [vec.get(k, 0) for k in all_kmers]
    
    sample_matrix = np.array([vec_to_row(v) for v in sample_vecs])
    ref_matrix = np.array([vec_to_row(v) for v in ref_vecs])
    
    return sample_matrix, ref_matrix

if __name__ == "__main__":
    print("Vectorizing sample...")
    sample_vecs, sample_ids = fasta_to_vectors(SAMPLE_FASTA, K)

    print("Vectorizing reference...")
    ref_vecs, ref_ids = fasta_to_vectors(REF_FASTA, K)

    sample_matrix, ref_matrix = to_dense_matrix_pair(sample_vecs, ref_vecs)

    print("\nMatches:")
    sim_matrix = cosine_similarity(sample_matrix, ref_matrix)
    for i, row in enumerate(sim_matrix):
        best_match_idx = np.argmax(row)
        best_score = row[best_match_idx]
        best_id = ref_ids[best_match_idx]

        if best_score >= MATCH_THRESHOLD:
            print(f"{sample_ids[i]} → {best_id} (Score: {best_score:.3f})")
        else:
            print(f"{sample_ids[i]} → No strong match found (Score: {best_score:.3f})")

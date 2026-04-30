# app/build_training_full.py
# Read ALL FASTA files in correct data folder (absolute path)

from Bio import SeqIO
import hashlib
import os

# Force absolute DATA directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))

print(f"\n📌 Using DATA FOLDER: {DATA_DIR}")

OUT_MARINE = os.path.join(DATA_DIR, "train_full", "marine.fasta")
OUT_NONMARINE = os.path.join(DATA_DIR, "train_full", "nonmarine.fasta")

# --- rules  ---
marine_genera = [
    # already strongly marine / coastal genera
    "roseovarius", "marinobacter", "halomonas", "vibrio",
    "pseudoalteromonas", "alteromonas", "shewanella",
    "alcanivorax", "salinivibrio", "marinimicrobium",
    "marinifilum", "marinobacterium", "maritimibacter",
    "mariniphaga", "marinospirillum", "oceanimonas",
    "photobacterium", "colwellia", "psychromonas",

    # extra marine/open-ocean associated genera
    "roseobacter", "marinomonas", "oceanimonas",
    "pelagibacter", "pelagibaca", "prochlorococcus",
    "synechococcus", "thiomicrospira", "thalassospira",
    "oceanospirillum", "marinobacterium", "marinobacter",
    "oceanicaulis", "salinibacter", "saccharospirillum",""
]


nonmarine_genera = [
    # already mostly soil / terrestrial / host-associated
    "bacillus", "streptomyces", "nocardiopsis", "pseudomonas",
    "planosporangium", "methylobacterium", "comamonas",
    "mycobacterium", "enterobacter", "serratia",
    "lactobacillus", "rhizobium", "azotobacter",

    # extra strongly non-marine genera
    "escherichia", "salmonella", "shigella", "klebsiella",
    "citrobacter", "yersinia", "proteus", "morganella",
    "staphylococcus", "streptococcus", "lactococcus",
    "micrococcus", "corynebacterium", "brevibacterium",
    "bradyrhizobium", "azospirillum", "clostridium",
    "bifidobacterium", "propionibacterium",
]


marine_morphology = [
    "maritimus", "maritima", "marinus", "marina",
    "sediminimaris", "pelagi", "ocean", "abyssi",
    "hydrothermal", "vent", "salinus", "halophilus"
]

nonmarine_morphology = [
    "soli", "soil", "terrae", "lactis",
    "freshwater", "river", "lake", "pond", "plantarum"
]


def classify(header):
    h = header.lower().split()
    genus = h[1] if len(h) > 1 else ""
    full = " ".join(h)
    if genus in marine_genera: return 1
    if genus in nonmarine_genera: return 0
    if any(m in full for m in marine_morphology): return 1
    if any(m in full for m in nonmarine_morphology): return 0
    return None

def hash_sequence(seq):
    return hashlib.md5(seq.encode()).hexdigest()

def load_all_sequences():
    fasta_files = [f for f in os.listdir(DATA_DIR)
                   if f.lower().endswith(".fasta") or f.lower().endswith(".fa")]

    print("\n📌 FASTA FILES FOUND:")
    for f in fasta_files:
        print(" →", f)

    seen = set()
    unique_records = []

    for fname in fasta_files:
        path = os.path.join(DATA_DIR, fname)
        for rec in SeqIO.parse(path, "fasta"):
            h = hash_sequence(str(rec.seq).upper())
            if h not in seen:
                seen.add(h)
                unique_records.append(rec)

    print(f"\n✔ Unique sequences loaded: {len(unique_records)}")
    return unique_records

def main():
    records = load_all_sequences()

    marine, nonmarine, ignored = [], [], 0

    print("\n🔍 Classifying...")
    for rec in records:
        label = classify(rec.description)
        if label == 1: marine.append(rec)
        elif label == 0: nonmarine.append(rec)
        else: ignored += 1

    print("\n==============================")
    print(f"✔ Marine sequences:      {len(marine)}")
    print(f"✔ Non-marine sequences:  {len(nonmarine)}")
    print(f"✔ Unknown:               {ignored}")
    print("==============================")

    os.makedirs(os.path.join(DATA_DIR, "train_full"), exist_ok=True)
    SeqIO.write(marine, OUT_MARINE, "fasta")
    SeqIO.write(nonmarine, OUT_NONMARINE, "fasta")

    print("\n🎉 DATA READY")
    print(" →", OUT_MARINE)
    print(" →", OUT_NONMARINE)

if __name__ == "__main__":
    main()

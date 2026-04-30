import os
from Bio import SeqIO
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from models.deep_model import CNN_DBM_Model, DNAEncoder

# ==========================
# CONFIG
# ==========================
SEQ_LEN = 1500
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "train_full")

MARINE_FASTA = os.path.join(DATA_DIR, "marine.fasta")
NONMARINE_FASTA = os.path.join(DATA_DIR, "nonmarine.fasta")

MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "pretrained", "marine_classifier.pt")

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ==========================
# Dataset
# ==========================
class EvalDataset(torch.utils.data.Dataset):
    def __init__(self, fasta_paths, labels, seq_len=1500):
        self.data = []
        self.encoder = DNAEncoder(seq_len)
        for path, label in zip(fasta_paths, labels):
            for rec in SeqIO.parse(path, "fasta"):
                self.data.append((str(rec.seq), label))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        seq, label = self.data[idx]
        x = self.encoder.encode(seq)
        y = torch.tensor(label, dtype=torch.long)
        return x, y


# ==========================
# Load Model
# ==========================
def load_model():
    model = CNN_DBM_Model(seq_len=SEQ_LEN)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()
    return model


# ==========================
# Evaluation
# ==========================
def evaluate():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model weights not found!")

    model = load_model()

    dataset = EvalDataset(
        [MARINE_FASTA, NONMARINE_FASTA],
        [1, 0]
    )

    loader = DataLoader(dataset, batch_size=32, shuffle=False)

    total = 0
    correct = 0

    with torch.no_grad():
        for batch_x, batch_y in loader:
            batch_x = batch_x.to(DEVICE)
            batch_y = batch_y.to(DEVICE)

            logits = model(batch_x)
            preds = torch.argmax(logits, dim=1)

            correct += (preds == batch_y).sum().item()
            total += batch_x.size(0)

    acc = correct / total
    print(f"\n🎯 Model Accuracy on Training Dataset: {acc:.4f}")
    print(f"   ({correct}/{total} correct predictions)\n")


if __name__ == "__main__":
    evaluate()

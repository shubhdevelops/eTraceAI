import pandas as pd
import matplotlib.pyplot as plt
import os

# Load match results
df = pd.read_csv("output/match_results.csv")

# Extract phylum from the lineage column (3rd word typically)
df["Phylum"] = df["Lineage"].str.split().str[2]

# Count occurrences of each phylum
phylum_counts = df["Phylum"].value_counts()

# Create output folder if not exists
os.makedirs("output", exist_ok=True)

# Plot bar chart
plt.figure(figsize=(8, 6))
phylum_counts.plot(kind="bar", color="skyblue")
plt.title("Detected Phyla in Sample")
plt.ylabel("Read Count")
plt.xlabel("Phylum")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Save the plot
output_file = "output/phylum_barplot.png"
plt.savefig(output_file)
print(f"✅ Phylum barplot saved to {output_file}")

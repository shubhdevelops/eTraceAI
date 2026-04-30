from celery import Celery
import os
import random
import time

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("edna_tasks", broker=redis_url, backend=redis_url)

@celery_app.task
def run_inference(job_id: str, file_path: str):
    print(f"Starting advanced inference for job {job_id} on file {file_path}")
    
    # Simulate processing delay
    time.sleep(3)
    
    # Generate rich mock data representing the ML outputs
    num_sequences = random.randint(150, 300)
    
    # 1. Sequences Table Data
    sequences = []
    for i in range(10): # Send top 10 for table
        marine_score = random.uniform(0.1, 0.99)
        novelty_score = random.uniform(0.1, 0.99)
        sequences.append({
            "id": f"SEQ_{i+1000}",
            "organism": random.choice(["Vibrio sp.", "Pseudomonas", "Unknown Marine", "Prochlorococcus", "Synechococcus"]),
            "dl_marine_score": round(marine_score, 3),
            "novelty_score": round(novelty_score, 3),
            "status": "Marine" if marine_score > 0.7 else ("Novel" if novelty_score > 0.6 else "Ambiguous")
        })

    # 2. UMAP Projection Data (2D Scatter)
    umap_data = []
    for i in range(100):
        # Create some clusters
        cluster = random.choice([0, 1, 2])
        x_base = [2.0, -3.0, 5.0][cluster]
        y_base = [3.0, -1.0, -4.0][cluster]
        
        novelty = random.uniform(0.1, 0.9)
        if cluster == 2: novelty = random.uniform(0.7, 0.99) # Make one cluster highly novel
        
        umap_data.append({
            "x": round(x_base + random.gauss(0, 1.5), 2),
            "y": round(y_base + random.gauss(0, 1.5), 2),
            "novelty": round(novelty, 2),
            "label": "Cluster A" if cluster == 0 else ("Cluster B" if cluster == 1 else "Novel Cluster")
        })

    # 3. Taxonomic Phylum Distribution (Bar Chart)
    taxonomy = [
        {"phylum": "Proteobacteria", "count": int(num_sequences * 0.4)},
        {"phylum": "Cyanobacteria", "count": int(num_sequences * 0.25)},
        {"phylum": "Bacteroidetes", "count": int(num_sequences * 0.15)},
        {"phylum": "Actinobacteria", "count": int(num_sequences * 0.10)},
        {"phylum": "Unknown/Novel", "count": int(num_sequences * 0.10)}
    ]

    # 4. Biotech Metrics (GC Content & Length Distribution)
    gc_distribution = [
        {"bin": "30-35%", "count": int(num_sequences * 0.05)},
        {"bin": "35-40%", "count": int(num_sequences * 0.15)},
        {"bin": "40-45%", "count": int(num_sequences * 0.40)},
        {"bin": "45-50%", "count": int(num_sequences * 0.30)},
        {"bin": "50-55%", "count": int(num_sequences * 0.10)}
    ]
    
    length_distribution = [
        {"length": "100-150bp", "count": int(num_sequences * 0.1)},
        {"length": "150-200bp", "count": int(num_sequences * 0.25)},
        {"length": "200-250bp", "count": int(num_sequences * 0.45)},
        {"length": "250-300bp", "count": int(num_sequences * 0.15)},
        {"length": "300+ bp", "count": int(num_sequences * 0.05)}
    ]
    
    avg_gc = round(random.uniform(41.5, 46.2), 1)
    shannon_index = round(random.uniform(3.5, 4.8), 2) # Typical alpha diversity range

    print(f"Completed inference for job {job_id}")
    
    return {
        "job_id": job_id,
        "metrics": {
            "total_sequences": num_sequences,
            "marine_like": int(num_sequences * 0.65),
            "potential_novel": int(num_sequences * 0.15),
            "avg_gc": f"{avg_gc}%",
            "shannon_index": shannon_index
        },
        "sequences": sequences,
        "umap_data": umap_data,
        "taxonomy": taxonomy,
        "gc_distribution": gc_distribution,
        "length_distribution": length_distribution
    }

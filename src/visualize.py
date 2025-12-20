import sys
import matplotlib.pyplot as plt
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import src.config as config


def generate_plot(results, query_text, phase_name, log_path):
    """
    Generates a 3-color bar chart:
    - Blue: Safe Documents
    - Orange: Malicious Document (Benign Content)
    - Red: The Active Poison Payload
    """
    ids = results['ids'][0]
    distances = results['distances'][0]
    metadatas = results['metadatas'][0]
    documents = results['documents'][0]
    
    colors = []
    clean_distances = []
    
    # The malicious string to color the poisoned chunk
    POISON_SIGNATURE = "support-portal-auth-fix.com"
    
    for i, meta in enumerate(metadatas):
        source = meta['source']
        text = documents[i]
        dist = distances[i]
        clean_distances.append(dist)
        
        # Color Logic
        if "patch" in source.lower() or "malicious" in source.lower():
            if POISON_SIGNATURE in text:
                colors.append('#d62728')  # Red: The poison
            else:
                colors.append('#ff7f0e')  # Orange: The carrier content
        else:
            colors.append('#1f77b4')  # Blue: Safe docs

    # Setup
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(clean_distances)), clean_distances, color=colors, alpha=0.8)
    
    # Styling
    safe_phase_name = phase_name.replace("/", "-")
    plt.title(f"Retrieval Distances: {phase_name}\nQuery: '{query_text[:50]}...'", fontsize=14)
    plt.xlabel("Rank (1 = Best Match)", fontsize=12)
    plt.ylabel("Cosine Distance (Lower is Closer)", fontsize=12)
    plt.xticks(range(len(clean_distances)), [str(i+1) for i in range(len(clean_distances))])
    
    # Add Cutoff Line
    plt.axvline(x=config.TOP_K_CONTEXT - 0.5, color='gray', linestyle='--', alpha=0.7)
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#d62728', label='Active Poison Payload'),
        Patch(facecolor='#ff7f0e', label='Malicious Doc (Context)'),
        Patch(facecolor='#1f77b4', label='Safe Doc'),
        plt.Line2D([0], [0], color='gray', linestyle='--', label='LLM Context Window')
    ]
    plt.legend(handles=legend_elements)
    
    # Save plot
    base_name = log_path.stem
    plot_filename = f"{base_name}_{safe_phase_name.replace(' ', '_')}.png"
    output_path = config.LOGS_DIR / plot_filename
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Plot saved: {plot_filename}")
    
    return plot_filename

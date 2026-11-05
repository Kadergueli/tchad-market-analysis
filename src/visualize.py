"""src/visualize.py : Export de la figure officielle pour LinkedIn et mémoires."""
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def plot_millet_comparison(pivot: pd.DataFrame, output_path: str | Path):
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    couleurs = {"N'Djaména": "#1f77b4", "Abéché": "#d62728", "Moundou": "#2ca02c"}
    
    for marche in ["N'Djaména", "Abéché", "Moundou"]:
        if marche in pivot.columns:
            serie = pivot[marche].dropna()
            ax.plot(serie.index, serie.values, label=marche, color=couleurs.get(marche, '#333'), linewidth=2.2, marker='o', markersize=4)

    ax.set_title("Dynamique des prix du Mil de détail au Tchad (2024–2026)\nCapitale vs Frontière Est (Abéché) vs Bassin Sud (Moundou)", fontsize=12, fontweight='bold', pad=15, loc='left')
    ax.set_xlabel("Date de relevé", fontsize=10, labelpad=10)
    ax.set_ylabel("Prix moyen (FCFA / kg)", fontsize=10, labelpad=10)
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#e0e0e0", loc="upper left")
    
    fig.text(0.06, -0.02, "Source : FreeData.td • Relevés PAM (VAM) et FEWS NET • Licence CC BY 4.0", fontsize=8, color="#555555")
    
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"[Succès] Graphique sauvegardé : {out}")

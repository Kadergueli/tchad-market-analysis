"""main.py : Exécution du pipeline complet sur freedatatd-markets-full.csv"""
from src.loader import load_and_clean_markets
from src.analytics import get_millet_series, compute_spreads_and_lean
from src.visualize import plot_millet_comparison
from pathlib import Path

def main():
    csv_file = Path("data/raw/freedatatd-markets-full.csv")
    print("1. Nettoyage et structuration des 45 000+ observations...")
    df = load_and_clean_markets(csv_file)
    print(f"   -> {len(df)} enregistrements valides chargés.")

    print("2. Extraction des séries du mil et calculs économiques...")
    pivot = get_millet_series(df)
    spreads, lean = compute_spreads_and_lean(pivot)

    # Sauvegarde des tableaux de sortie
    Path("outputs/tables").mkdir(parents=True, exist_ok=True)
    pivot.to_csv("outputs/tables/prix_millet_ndjamena_abeche_moundou.csv")
    spreads.to_csv("outputs/tables/spreads_relatifs_millet.csv")
    lean.to_csv("outputs/tables/impact_soudure_annuel.csv")
    print("   -> Tableaux exportés dans outputs/tables/")

    print("3. Export du visuel haute résolution (300 DPI)...")
    plot_millet_comparison(pivot, "outputs/figures/dynamique_prix_mil_tchad.png")
    print("\n[Terminé] Pipeline exécuté avec succès.")

if __name__ == "__main__":
    main()

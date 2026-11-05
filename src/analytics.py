"""src/analytics.py : Métriques de marché et dynamique de soudure."""
import pandas as pd

def get_millet_series(df: pd.DataFrame) -> pd.DataFrame:
    millet = df[df['indicator'].str.contains('Millet', case=False, na=False)].copy()
    
    def simplify_market(m):
        if "Abeche" in m: return "Abéché"
        if "Moundou" in m: return "Moundou"
        if "N'Djamena" in m: return "N'Djaména"
        return m
        
    millet['marche_clean'] = millet['marche'].apply(simplify_market)
    cibles = ["N'Djaména", "Abéché", "Moundou"]
    sub = millet[millet['marche_clean'].isin(cibles)]
    
    pivot = sub.pivot_table(index='date', columns='marche_clean', values='prix_fcfa', aggfunc='mean')
    return pivot.sort_index()

def compute_spreads_and_lean(pivot: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    spreads = pd.DataFrame(index=pivot.index)
    if "N'Djaména" in pivot.columns:
        for c in ["Abéché", "Moundou"]:
            if c in pivot.columns:
                spreads[f"spread_{c}_vs_Ndjamena_pct"] = ((pivot[c] - pivot["N'Djaména"]) / pivot["N'Djaména"] * 100).round(1)

    # Choc de soudure : on cible UNIQUEMENT les colonnes numériques des marchés
    cols_marches = [c for c in pivot.columns if c in ["Abéché", "Moundou", "N'Djaména"]]
    pivot_reset = pivot.reset_index()
    pivot_reset['mois'] = pivot_reset['date'].dt.month
    pivot_reset['annee'] = pivot_reset['date'].dt.year
    
    soudure = pivot_reset[pivot_reset['mois'].isin([7, 8])].groupby('annee')[cols_marches].mean()
    recolte = pivot_reset[pivot_reset['mois'].isin([12, 1])].groupby('annee')[cols_marches].mean()
    
    # Division numérique stricte sans colonne temporelle
    lean_impact = ((soudure - recolte) / recolte * 100).round(1)
    return spreads, lean_impact

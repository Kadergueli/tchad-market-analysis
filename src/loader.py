"""src/loader.py : Chargement et normalisation de freedatatd-markets-full.csv"""
import pandas as pd
import re
from pathlib import Path

def parse_region(region_str: str) -> tuple[str, str]:
    if not isinstance(region_str, str):
        return ("Inconnu", "Inconnu")
    if "N'Djamena" in region_str:
        if "Marche A Mil" in region_str:
            return ("N'Djamena (Mil)", "N'Djamena")
        return ("N'Djamena", "N'Djamena")
    match = re.match(r"^(.*?)\s*\((.*?)\)$", region_str.strip())
    if match:
        return (match.group(1).strip(), match.group(2).strip())
    return (region_str.strip(), region_str.strip())

def load_and_clean_markets(filepath: str | Path) -> pd.DataFrame:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    df = pd.read_csv(path)
    df = df[df['value'] > 0].copy()
    
    # Normalisation au 1er du mois pour fusionner PAM et FEWS NET
    df['date'] = pd.to_datetime(df['reference_date'], errors='coerce')
    df = df.dropna(subset=['date', 'value'])
    df['date'] = df['date'].dt.to_period('M').dt.to_timestamp()

    marches_provinces = df['region'].apply(parse_region)
    df['marche'] = [mp[0] for mp in marches_provinces]
    df['province'] = [mp[1] for mp in marches_provinces]
    df['prix_fcfa'] = df['value']
    
    return df

# Analyse des Marchés Vivriers au Tchad (2020–2026)
### Infrastructure de données ouvertes — FreeData.td

Ce projet propose une analyse empirique des séries mensuelles de prix de détail des céréales (mil, sorgho, maïs) sur 56 marchés locaux au Tchad.

## Structure du Projet
- `src/loader.py` : Contrôle qualité, détection d'anomalies et typage des données.
- `src/analytics.py` : Calculs des différentiels régionaux (spreads) et impact de la soudure.
- `src/visualize.py` : Export des visualisations haute résolution (300 DPI).
- `CODEBOOK.md` : Dictionnaire complet des variables et normes de citation.

## Installation et Exécution
```bash
pip install -r requirements.txt
python main.py
pytest tests/
```

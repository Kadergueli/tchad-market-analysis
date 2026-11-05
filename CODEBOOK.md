# Dictionnaire des Données (Codebook) : Séries des Marchés Vivriers au Tchad (2024–2026)

**Plateforme émettrice** : FreeData.td  
**Licence des données** : Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Sources primaires** : Programme Alimentaire Mondial (PAM / VAM DataBridges) et Réseau de systèmes d'alerte précoce contre la famine (FEWS NET)  
**Couverture temporelle** : Janvier 2024 à Août 2026  
**Fréquence d'observation** : Mensuelle  
**Couverture géographique** : 72 marchés locaux et 23 provinces administratives du Tchad  

---

## 1. Schéma du Fichier Brut (`data/raw/freedatatd-markets-full.csv`)

Le fichier source consolidé regroupe 45 177 observations brutes issues des moissonnages automatisés de FreeData.td.

| Nom de colonne | Type | Description détaillée | Format / Valeurs admises | Exemples observés |
| :--- | :--- | :--- | :--- | :--- |
| `id` | Entier | Identifiant unique de l'observation dans la base centrale FreeData.td | Entier positif | `377670`, `390124` |
| `sector` | Chaîne | Domaine sectoriel de l'observation | Chaîne fixe | `markets` |
| `indicator` | Chaîne | Libellé normalisé de la denrée ou de la métrique suivie | Nom du produit + type de prix + source | `Millet retail price (WFP)`, `Sorghum (red) retail price (WFP)` |
| `value` | Décimal | Valeur numérique constatée du relevé | Flottant strictement positif | `280.0`, `608.0`, `192700.0` |
| `unit` | Chaîne | Unité physique de transaction économique | Standardisée | `XAF/KG`, `XAF/ea`, `% of GDP` |
| `reference_date` | Date | Date calendaire du relevé (début de mois WFP ou fin de mois FEWS NET) | `YYYY-MM-DD` | `2024-02-01`, `2024-05-31` |
| `country_code` | Chaîne | Code ISO 3166-1 alpha-3 du pays | Code à 3 lettres | `TCD` |
| `region` | Chaîne | Localité/marché de collecte et province administrative associée | Format composite : `Ville (Province)` | `Abeche (Ouaddai)`, `Moundou (Logone Occidental)`, `Dembe (N'Djamena)` |
| `source` | Chaîne | Institution ou agence source du relevé primaire | Catégoriel | `WFP`, `FEWS NET`, `World Bank` |
| `source_url` | Chaîne | URL du point d'accès d'origine (si disponible) | URL ou `NaN` | `NaN` |
| `license` | Chaîne | Licence juridique de réutilisation des données | Mention de licence | `CC BY 4.0` |
| `notes` | Chaîne | Mentions de traçabilité et clause d'attribution du collecteur | Texte libre | `Source: World Food Programme (WFP), via HDX.` |
| `collected_at` | Horodatage | Date et heure ISO de l'ingestion par les agents de collecte | Horodatage ISO 8601 | `2026-09-12T10:06:08.838661` |

---

## 2. Schéma des Tables Dérivées (`outputs/tables/`)

Les tables suivantes sont produites automatiquement par le script d'analyse `main.py` :

### A. Séries mensuelles de prix (`prix_millet_ndjamena_abeche_moundou.csv`)
* `date` : Date normalisée ramenée au 1er jour du mois civil d'observation (`YYYY-MM-01`).
* `Abéché` : Prix moyen au détail du mil pénicillaire à Abéché (en FCFA / kg).
* `Moundou` : Prix moyen au détail du mil pénicillaire à Moundou (en FCFA / kg).
* `N'Djaména` : Prix moyen au détail du mil pénicillaire dans la capitale (en FCFA / kg).

### B. Différentiels régionaux (`spreads_relatifs_millet.csv`)
* `date` : Mois d'observation (`YYYY-MM-01`).
* `spread_Abéché_vs_Ndjamena_pct` : Écart relatif en pourcentage entre Abéché et la référence N'Djaména :  
  $$\text{Spread} = \frac{\text{Prix}_{\text{Abéché}} - \text{Prix}_{\text{N'Djaména}}}{\text{Prix}_{\text{N'Djaména}}} \times 100$$
* `spread_Moundou_vs_Ndjamena_pct` : Écart relatif en pourcentage entre Moundou et la référence N'Djaména :  
  $$\text{Spread} = \frac{\text{Prix}_{\text{Moundou}} - \text{Prix}_{\text{N'Djaména}}}{\text{Prix}_{\text{N'Djaména}}} \times 100$$

### C. Indicateur de soudure agricole (`impact_soudure_annuel.csv`)
* `annee` : Année civile d'observation (`2024`, `2025`).
* `Abéché`, `Moundou`, `N'Djaména` : Hausse relative en pourcentage entre la moyenne des mois de pic de soudure (juillet et août) et la moyenne des mois de post-récolte (décembre et janvier) :  
  $$\Delta_{\text{soudure}} = \frac{\bar{P}_{\text{juil-août}} - \bar{P}_{\text{déc-janv}}}{\bar{P}_{\text{déc-janv}}} \times 100$$

---

## 3. Règles de Nettoyage et Contrôle Qualité Appliquées

* **Suppression des anomalies** : Filtrage strict des valeurs de prix nulles ou négatives (`value > 0`)[cite: 2].
* **Réconciliation temporelle** : Les relevés du PAM (datés au premier du mois) et ceux de FEWS NET (datés au dernier jour du mois) sont harmonisés à une même clé mensuelle `YYYY-MM-01` pour permettre les calculs d'écarts spatiaux synchrones.
* **Extraction toponymique** : Parsing régulier de la colonne `region` pour isoler la place de marché physique de sa province de rattachement.
* **Harmonisation des marchés de N'Djaména** : Consolidation des relevés provenant de plusieurs points de vente intra-urbains (Dembé, Atrone, Marché à Mil) sous une moyenne représentative de la capitale.

---

## 4. Modalités de Citation Obligatoire

En cas d'utilisation de ces données dans un article de recherche, mémoire académique, rapport d'évaluation ou support cartographique, mentionner la source sous l'un des formats suivants[cite: 2] :

### Format APA (7e édition)
> FreeData.td. (2026). *Base des prix de détail des marchés vivriers au Tchad (2024–2026)* [Jeu de données]. Plateforme ouverte FreeData.td, sous licence CC BY 4.0. https://freedata-td.onrender.com

### Format BibTeX
```bibtex
@misc{freedata_marches_tchad_2026,
  author = {{FreeData.td}},
  title = {Base des prix de détail des marchés vivriers au Tchad (2024--2026)},
  year = {2026},
  publisher = {FreeData.td},
  url = {[https://freedata-td.onrender.com](https://freedata-td.onrender.com)},
  note = {Licence Creative Commons Attribution 4.0 International (CC BY 4.0)}
}

# Méthodologie de calcul du panier alimentaire de survie au Tchad

## Objet documentaire

Ce document formalise la méthode de calcul du coût mensuel du panier alimentaire de survie utilisé dans le projet `tchad-market-analysis`, en cohérence avec la logique en vigueur dans `src/panier_survie.py` et dans l’interface de visualisation `app.py`. Il vise à verrouiller la crédibilité scientifique du dispositif en explicitant les hypothèses, la chaîne de traitement des données et les limites d’interprétation sans introduire d’éléments extérieurs à la base de données et au code projet.

Le projet repose sur des séries de prix observés au niveau de marchés tchadiens et utilise une formulation de type Minimum Expenditure Basket (MEB), au sens du volet alimentaire, dans une perspective de survie minimale. Les calculs ne produisent pas une estimation d’aide fictive ou de transfert forfaitaire, mais un coût de référence a posteriori fondé sur des prix du marché.

---

## 1. Cadre Général & Fondements Théoriques

### 1.1 Définition du cadre méthodologique

Le cadre retenu est celui du Minimum Expenditure Basket (MEB), au sens du volet alimentaire. Cette approche correspond à la logique de référence du Programme Alimentaire Mondial (PAM) et de l’initiative VAM (Vulnerability Analysis and Mapping), qui consiste à estimer le coût minimal nécessaire pour couvrir les besoins essentiels d’un ménage, sans prise en compte des dépenses non alimentaires dans le périmètre de base du calcul.

Dans le projet, cette logique est appliquée à un panier alimentaire de survie, formé de quatre denrées de base : mil pénicillaire local, niébé / haricot sec local, huile végétale et sel iodé. Il s’agit donc d’un Food MEB, et non d’un MEB complet dans son acception large qui inclurait aussi l’eau, le combustible, l’hygiène, les soins et l’éducation.

### 1.2 Objectif de mesure

L’objectif de mesure est de reconstruire, par marché et par période, le coût mensuel incompressible d’un ménage moyen sahélien pour couvrir un niveau nutritionnel vital. Le référentiel explicite dans le projet une norme de survie minimale correspondant à environ 2 100 kcal par jour et par personne, sur une période de 30 jours.

Cette référence n’est pas utilisée comme hypothèse de production de données artificielles, mais comme cadre d’interprétation du panier standard. Le calcul du coût est donc une tentative de monétisation d’un besoin vital alimentaire, à partir de prix de marché observés, selon la composition standardisée du panier.

### 1.3 Principe d’agrégation retenu

À la racine du projet, le coût du panier est calculé sur la base de séries mensuelles de prix par marché, puis agrégées dans une formulation standardisée. Le code applique une logique de regroupement spatial suivie d’une projection dans un format mensuel unique par marché, avant d’aboutir au coût du panier pour chaque période étudiée.

---

## 2. Spécification Mathématique & Rations du Panier

### 2.1 Formulation mathématique

Le code de la vue d’analyse et des exports établit explicitement la formulation suivante pour un foyer de $N$ personnes :

$$
\text{Coût}(t, m) = \frac{N}{5} \times \left( 60 \cdot P_{\text{mil}}(t, m) + 9 \cdot P_{\text{niébé}}(t, m) + 3{,}75 \cdot P_{\text{huile}}(t, m) + 1{,}0 \cdot P_{\text{sel}}(t, m) \right)
$$

où :

- $t$ désigne le mois d’observation ;
- $m$ désigne le marché considéré ;
- $N$ est la taille du ménage ;
- $P_{\text{mil}}$, $P_{\text{niébé}}$, $P_{\text{huile}}$ et $P_{\text{sel}}$ représentent les prix unitaires observés par denrée pour le marché $m$ à la date $t$.

La structure du calcul est entièrement cohérente avec le code : le panier de base est de 60 kg de mil, 9 kg de niébé, 3,75 litres d’huile végétale et 1 kg de sel, et le coût est ensuite ajusté proportionnellement à la taille du ménage selon le rapport $N/5$.

### 2.2 Rationnement et composition du panier

Le projet considère un ménage-type de 5 personnes, à partir de la structure standard fixée dans le code (`TAILLE_STD = 5.0`). Les quantités retenues sont donc celles d’un panier standard PAM / VAM basé sur une consommation alimentaire minimale de survie.

| Denrée | Rôle nutritionnel | Quantité standard | Rôle dans le panier |
|---|---|---:|---|
| Mil pénicillaire local | Céréale de base, glucides complexes, énergie durable | 60 kg | Contribution dominante au coût total et à la ration énergétique |
| Niébé / haricot sec local | Légumineuse, protéines végétales, apport azoté | 9 kg | Complément protéique du régime alimentaire de survie |
| Huile végétale d’arachide | Lipides essentiels, densité calorique | 3,75 L | Apport énergétique concentré et densité calorique |
| Sel iodé | Micronutriments, prévention des carences | 1 kg | Élément de couverture minimale et de sécurité micronutritionnelle |

Les pondérations incorporées au calcul révèlent clairement la domination de la céréale dans le coût total : le mil représente environ 60 % de la facture totale du panier selon la formulation retenue, tandis que le niébé, l’huile et le sel complètent la ration.

### 2.3 Intégration de la norme nutritionnelle

Le projet ne se contente pas d’un simple assemblage de prix. Il insère cette composition dans un cadre nutritionnel de survie, en cohérence avec la norme de 2 100 kcal/jour/personne. Cette référence est explicitement mobilisée dans l’interface de l’application comme l’élément permettant de présenter le panier comme un seuil de survie, et non comme un panier de consommation courante ou un panier de bien-être.

---

## 3. Typologie Spatiale des Marchés Étudiés

Le projet suit trois marchés clés, explicitement identifiés dans le code du tableau de bord et dans les formes de calcul : `Moundou`, `N'Djaména` et `Abéché`.

### 3.1 Moundou (Logone Occidental)

Moundou est classé dans le code comme un marché situé dans le bassin agricole soudanien, donc dans une zone productrice et tendanciellement plus résiliente sur le plan de l’offre. Son rôle est de servir de plancher des prix et de référentiel de résilience d’accès alimentaire. Cette logique correspond à la composition des données et à la présence de séries observées sur ce marché dans l’agrégation finale.

### 3.2 N’Djaména

N’Djaména est présenté comme capitale et centre de consommation majeur. Son coût du panier est sensible aux coûts de transport, aux marges commerciales et aux mécanismes d’acheminement depuis les zones productrices. C’est donc un marché de grande consommation et de forte pression sur les prix de détail, qui joue le rôle de point de référence urbanisé dans le système.

### 3.3 Abéché (Ouaddaï)

Abéché est classé comme marché sahélien oriental soumis à des contraintes logistiques et de demande. Le code décrit explicitement cette ville comme située dans une zone de vulnérabilité accrue, sous double contrainte : l’enclavement logistique saisonnier et la pression frontalière sur la demande. Ceci l’expose à des variations de prix plus marquées et à des pics de coût plus abrupts.

### 3.4 Représentativité du panel spatial

Le périmètre du projet n’est pas un maillage national complet. Il couvre trois marchés centraux du réseau d’observation projectuel, choisis pour leur rôle de référence observée dans les flux de production, les marchés urbains de consommation et les points sahéliens de tension logistique. Cette structure constitue un point fort pour l’analyse comparative, mais impose aussi des limites de portée géographique, comme indiqué plus bas.

---

## 4. Pipeline de Traitement des Données (`src/panier_survie.py`)

### 4.1 Source des données brutes

La donnée brute est issue de la base `freedatatd-markets-full.csv`, dans le répertoire de données du projet. Le code de `src/panier_survie.py` charge le fichier, puis normalise les champs de date et de valeur. La base est explicitement présentée comme une série de plus de 45 000 relevés mensuels. La logique de calcul exploite en particulier les champs `reference_date`, `region`, `indicator` et `value`.

### 4.2 Lecture et préparation de la base

Le flux de traitement est le suivant :

1. identification du chemin de la donnée brute ;
2. lecture du fichier CSV dans un DataFrame pandas ;
3. conversion de `reference_date` en dates `datetime` ;
4. conversion de `value` en numérique, avec exclusion des valeurs manquantes ;
5. préparation de colonnes de marché et d’indicateur pour la suite du calcul.

Le code impose un traitement explicite des valeurs numériques vacantes avant l’agrégation. Cela garantit que le calcul de coût ne s’appuie pas sur des observations non numériques ou non renseignées.

### 4.3 Nettoyage textuel et attribution des marchés

La fonction `clean_str()` normalise les chaînes en retirant les accents, apostrophes et espaces, afin d’assigner proprement les marchés à partir des libellés `region` et `indicator`.

Le mécanisme d’assignation est volontairement robuste :

- `N'Djaména` : reconnaissance de `ndjamena` ;
- `Abéché` : reconnaissance de `abeche`, `ouaddai` ;
- `Moundou` : reconnaissance de `moundou`, `logoneoccidental`, `logoneocc`.

Cette étape est essentielle au bon fonctionnement du pipeline, car le calcul du panier repose sur la bonne attribution d’une observation à un marché précis, ce qui conditionne ensuite la qualité de la série mensuelle aggregée.

### 4.4 Sélection des marchés cibles

Le code définit explicitement un périmètre de calcul sur les trois marchés suivis :

- `N'Djaména`
- `Abéché`
- `Moundou`

Cette sélection est ensuite réutilisée pour la construction des séries mensuelles et pour l’affichage comparatif dans le tableau de bord.

### 4.5 Filtrage des denrées et agrégation par produit

Le calcul du panier repose sur un filtrage exact des sous-séries par produit, à partir de motifs d’indicateurs :

- `mil` → `Millet`
- `niebe` → `niebe`
- `huile` → `Oil (groundnut)`
- `sel` → `Salt`

Le code crée ensuite des tables croisées (`pivot_table`) en indexant les prix par date et par marché, puis agrège la série mensuelle avec `resample('ME')` (ou équivalent de fin de mois). Ce mécanisme permet de transformer les observations brutes en séries mensuelles homogènes et exploitable pour le calcul du panier.

La logique est davantage une standardisation par période mensuelle que de lissage artificiel : les séries sont regroupées à la fréquence centrale du calcul et les marchés sont réindexés pour obtenir une grille temporelle commune.

### 4.6 Construction du panier mensuel

Après agrégation des composantes par produit et par marché, le code calcule pour chaque marché le coût mensuel du panier selon la relation suivante :

$$
\text{Panier}_{m,t} = 60 \cdot P_{\text{mil},m,t} + 9 \cdot P_{\text{niébé},m,t} + 3.75 \cdot P_{\text{huile},m,t} + 1.0 \cdot P_{\text{sel},m,t}
$$

Le DataFrame final `basket_df` contient ainsi une série mensuelle du coût du panier pour chaque marché sélectionné. L’applicatif utilise ensuite cette série dans les tableaux, les graphiques et les rapports de synthèse.

### 4.7 Sorties produites

Le pipeline produit des sorties explicites :

- `outputs/tables/cout_mensuel_panier_survie.csv` : base mensuelle agrégée par marché ;
- `outputs/figures/cout_panier_survie_tchad.png` : figure de la trajectoire des coûts par marché ;
- `outputs/rapport_panier_survie.md` : rapport analytique synthétique.

Le fichier de sortie CSV présente une structure typique : colonne `reference_date`, puis les colonnes par marché (`N'Djaména`, `Abéché`, `Moundou`). Cette structure est explicitement visible dans les premières lignes de la base calculée.

### 4.8 Honnêteté sur la complétude des séries

Le projet applique une logique de standardisation et de continuité temporelle sur des séries mensuelles, sans injection de données synthétiques. La base est construite à partir d’observations du marché et de méthodes de réindexation temporelle. En l’état du code, la méthode reste fondée sur des séries observées, avec reconstitution de la grille mensuelle mais sans génération de valeurs artificielles non documentées.

---

## 5. Limites Économiques et Hypothèses Structurantes (Honnêteté Scientifique)

### 5.1 Panier alimentaire vs panier global

Le dispositif ne mesure pas l’ensemble du coût de vie d’un ménage. Il s’agit d’un Food MEB strict. Il couvre la dépense alimentaire incompressible nécessaire à un équilibre nutritionnel minimal, mais exclut les dépenses non alimentaires :

- eau potable ;
- combustible / bois de chauffe ;
- énergie ;
- hygiène ;
- soins ;
- éducation ;
- transport non lié directement à l’approvisionnement alimentaire.

Cette distinction est essentielle. Un panier alimentaire de survie ne saurait être assimilé à un panier de consommation complète ni à un minimum de vie socialement décent. Son interprétation correcte est d’ordre alimentaire et de protection de la survie physique.

### 5.2 Prix de détail vs prix bord-champ

Les données utilisées dans le projet correspondent au prix payé par le consommateur final sur les étals et marchés de vente, et donc à des prix de détail. Elles ne reflètent pas directement les prix reçus par les producteurs à la récolte, ni les prix de gros ou de bord-champ, qui peuvent naturellement être inférieurs aux prix observés sur les marchés urbains.

Cette distinction est méthodologiquement importante, car le coût du panier est un indicateur de pression sur les ménages consommateurs et non un indicateur de revenu des producteurs. La base n’est donc pas un indicateur de marge de production rurale, mais d’accès au marché urbain et de charge de consommation pour les ménages.

### 5.3 Périmètre spatial et limites de représentativité

Les séries sont construites sur trois marchés précis : Moundou, N’Djaména et Abéché. Elles ne reflètent pas directement l’ensemble des zones pastorales, transhumantes ou désertiques du Tchad, en particulier l’extrême Nord, ni les marchés périphériques non suivis dans la base. Le dispositif est donc robuste pour le suivi comparatif de marchés de référence, mais il ne remplace pas un dispositif de surveillance nationale complet et hiérarchisée.

### 5.4 Limite des marchés urbains et de carrefour

La base documentée du projet est structurée autour de marchés urbains et de points de carrefour commercial, plutôt que de zones rurales dispersées. Cette configuration a pour avantage de capter les coûts de consommation effective et d’accessibilité alimentaire, mais elle ne rend pas compte de la dynamique de production locale et des écarts de prix qui peuvent se produire dans les zones plus enclavées ou plus isolées.

---

## 6. Repères Macroéconomiques & Utilisations Opérationnelles

### 6.1 Comparaison au SMIG

Le tableau de bord compare le coût du panier au Salaire Minimum Interprofessionnel Garanti (SMIG) légal du Tchad, fixé à 60 000 FCFA. La mesure est interprétée comme un repère macroéconomique de pouvoir d’achat et de pression sur les dépenses incompressibles.

Dans le code de l’application, cette référence est utilisée pour calculer la part du SMIG absorbée par le panier mensuel, selon la logique :

$$
\text{Part du SMIG} = \frac{\text{Coût du panier}}{\text{SMIG}} \times 100
$$

Cette formulation permet d’évaluer la capacité d’un ménage moyen à couvrir ses besoins alimentaires essentiels avec un revenu minimum légal. Le calcul n’est pas un substitut au calcul du revenu réel, mais un point de référence d’accessibilité à un coût de survie.

### 6.2 Implications opérationnelles pour les acteurs humanitaires et décideurs

Le projet a une valeur opérationnelle forte pour les acteurs humanitaires, les agences de protection sociale et les décideurs :

- il identifie les marchés où la charge alimentaire minimale est la plus élevée ;
- il permet de comparer la pression sur les dépenses de survie au seuil de référence du SMIG ;
- il soutient l’argument selon lequel des transferts monétaires forfaitaires uniformes sont rarement efficaces dans un système où les coûts de consommation varient spatialement.

Les usages visés sont donc ceux d’un observatoire de prix capable d’orienter des décisions d’indexation territorialisée plutôt que des montants uniformes non différenciés. Cette interprétation est compatible avec les objectifs de comparaison et de soutien à la décision explicitement présents dans le code de l’interface.

### 6.3 Positionnement analytique

Le projet n’emploie pas de coefficients de choc fictifs, ni d’aides non documentées, ni de montants arbitraires de transfert. Les références utilisées sont des coûts de marché réels, observés et agrégés, comparés à un seuil institutionnel (SMIG). Cette approche augmente la reproductibilité analytique et la crédibilité de l’outil pour le pilotage décisionnel.

---

## 7. Traçabilité, Licence & Citation

### 7.1 Traçabilité du projet

Le projet est stocké dans le dépôt GitHub `Kadergueli-Labs / tchad-market-analysis` et mobilise :

- la base de données `freedatatd-markets-full.csv` ;
- le script `src/panier_survie.py` pour la génération du panier mensuel ;
- l’application `app.py` pour la visualisation, le benchmark SMIG et l’analyse comparative ;
- le répertoire `outputs/` pour les séries, figures et rapports structurés.

La traçabilité est donc descendue jusqu’à la donnée brute et au script d’agrégation, avec des sorties prêtes à l’usage pour le reporting analytique.

### 7.2 Licence

Le dépôt est publié sous licence Creative Commons Attribution 4.0 International (CC BY 4.0).

Cette licence autorise la réutilisation, la modification et la diffusion du travail, à condition d’attribuer correctement la source et de mentionner les modifications éventuelles.

### 7.3 Citation bibliographique recommandée

#### BibTeX

```bibtex
@misc{freedata_tchad_market_analysis,
  author = {{FreeData.td} and {Kadergueli-Labs}},
  title = {tchad-market-analysis},
  year = {2024},
  howpublished = {GitHub repository},
  url = {https://github.com/Kadergueli/tchad-market-analysis},
  note = {Licensed under CC BY 4.0}
}
```

#### Forme texte institutionnelle

FreeData.td and Kadergueli-Labs. *tchad-market-analysis*. GitHub repository, 2024. Licensed under CC BY 4.0. Available at: https://github.com/Kadergueli/tchad-market-analysis.

---

## 8. Conclusion méthodologique

Le projet établit un cadre d’analyse rigoureux, basé sur des prix de marché observés, sur une structure de panier alimentaire standardisée et sur un benchmark institutionnel explicite (SMIG). La méthode est scientifique dans sa logique de calcul, critique dans ses limites, et claire dans son objectif : mesurer la charge alimentaire minimale de survie sur les marchés suivis au Tchad, sans sur-interprétation et sans fabrication de données.

La crédibilité du dispositif repose sur trois principes fondamentaux :

1. des données de marché observées ;
2. une formulation de panier standardisée et explicitement documentée ;
3. une interprétation prudente, centrée sur la survie et le coût incompressible, sans substitution de la dépense non alimentaire ni des niveaux de vie complets.

C’est précisément cette transparence de construction qui permet d’interpréter les résultats comme des indicateurs de vulnérabilité alimentaire et non comme des projections complètes de la situation socio-économique des ménages.

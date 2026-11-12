# FashMatch — intégration du catalogue Kaggle

## Objectif
Préparer un catalogue public pour le POC de Data Engineering, **sans photographies de personnes ni données réelles d'utilisateurs**. La source est `Fashion Product Images (Small)` par Param Aggarwal, page Kaggle : https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small

**Statut : intégration préparée, non exécutée sur le CSV original.** Le dataset n'est pas redistribué dans ce ZIP ; son téléchargement reste à effectuer et sa provenance doit être vérifiée. Le script ne fabrique pas de données produits.

## Télécharger le fichier source
1. Ouvrir la page Kaggle et se connecter.
2. Télécharger le dataset, puis extraire uniquement `styles.csv` (ignorer les images).
3. Placer `styles.csv` dans `data/raw/`.

Option via l'API Kaggle, si configurée :

```bash
kaggle datasets download -d paramaggarwal/fashion-product-images-small -p downloads --unzip
```

Puis copier le fichier `styles.csv` obtenu dans `data/raw/`.

## Exécuter

```bash
python -m pip install -r requirements.txt
python src/prepare_catalogue.py
```

Option : `python src/prepare_catalogue.py --limit 1000` pour un premier test rapide.

Résultats :
- `data/processed/catalogue_fashmatch.csv` : catalogue nettoyé ;
- `data/processed/rapport_catalogue.json` : métriques de qualité et de distribution.

## Traitements appliqués
- Validation de la présence des dix colonnes d'origine ;
- sélection de 8 colonnes nécessaires et renommage ;
- suppression de `gender` (public commercial visé) et `year` (non nécessaire au scénario minimal) ;
- suppression des lignes sans identifiant, catégorie ou type de produit ;
- dédoublonnage par identifiant produit ;
- limitation aux catégories Apparel, Footwear, Accessories ;
- contrôle des valeurs manquantes et des distributions ;
- **aucune image téléchargée, aucune donnée client utilisée**.

## Limites et décisions à documenter
- Le CSV d'origine ne contient pas de prix ni de tailles : ne pas les inventer comme s'ils provenaient de Kaggle.
- `usage` (Casual/Formal/Sports...) n'est pas une taxonomie complète des styles.
- La page Kaggle affiche MIT ; la portée des droits sur les photos et les marques n'est pas démontrée par cette seule mention. La réutilisation des métadonnées est proposée pour un POC pédagogique, sous réserve de validation par l'équipe DPO.
- Le catalogue est historique, pas un inventaire commercial actuel.
- Les métriques réelles de qualité ne seront connues qu'après exécution sur `styles.csv`.
- Les profils synthétiques restent un **jeu séparé**, à relier ensuite par des préférences déclarées fictives ; ils ne sont pas des données anonymisées de personnes réelles.

## Collaboration DPO
Lire `docs/fiche_source_et_DPO.md` et `docs/dictionnaire_donnees.csv`. Les DPO valident finalité, champs conservés, droits d'utilisation et mesures de rétention sur les profils. Les politiques de conservation ne sont pas fixées par ce script.

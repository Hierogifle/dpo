# Fiche de source et note de validation DPO — FashMatch

## Provenance et licence
- Source : Param Aggarwal, **Fashion Product Images (Small)**, Kaggle.
- URL : https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small
- Licence **affichée sur Kaggle** : MIT (vérifiée lors de la préparation, 10 novembre 2026).
- Métadonnées : `styles.csv`, 10 champs, environ 44 000 produits ; comptages exacts à vérifier après téléchargement.
- Fréquence de mise à jour indiquée : jamais.
- Attention : une licence déclarée par l'uploader ne suffit pas à certifier les droits sur les photographies de produits, marques et éléments provenant de tiers.

## Objectif du traitement
Constituer un petit catalogue de vêtements et accessoires pour tester un pipeline ETL, la minimisation et la qualité des données. Aucun utilisateur réel ni photographie de personne n'est requis.

## Ce qui est retenu
Identifiant produit, catégorie, sous-catégorie, type, couleur, saison, usage, nom de produit et référence de source. `gender` et `year` sont exclus dans le scénario minimal.

## Explications simples
- **Minimisation** : ne pas importer des colonnes dont on n'a pas besoin.
- **Profil synthétique** : personne inventée de toutes pièces ; ce n'est pas un profil client anonymisé.
- **Pseudonymisation** : remplacer un identifiant permettant de retrouver une personne par un code ; contrairement à l'anonymisation, cela reste potentiellement réidentifiable.
- **Qualité** : mesurer les valeurs manquantes, les doublons et les catégories sous-représentées.

## Questions à valider ensemble
1. Autorisons-nous les métadonnées de ce catalogue pour la démonstration pédagogique, sans redistribution d'images ?
2. L'usage prévu est-il uniquement un test d'ETL ou également une recommandation simulée ?
3. Faut-il conserver `productDisplayName` ou seulement les catégories et couleurs ?
4. Souhaite-t-on exclure `gender` de façon permanente pour éviter un filtrage inutile des vêtements ?
5. Quels champs des profils synthétiques sont indispensables ? Quelle finalité justifie chacun ?
6. Quelle durée de conservation fictive tester et quelle règle de purge démontrer ? (À décider, pas de durée RGPD universelle.)
7. Quelle procédure de vérification des droits sur les photographies avant un éventuel usage ultérieur ?
8. Comment tracer l'origine et la version du dataset sans enregistrer de données personnelles ?

## Décisions provisoires
- Ne pas utiliser d'images du dataset dans ce POC.
- Ne pas intégrer de prix ou de tailles non présents dans la source.
- Ne pas inférer de caractéristiques sensibles à partir des vêtements.
- Ne pas présenter la licence MIT comme une garantie juridique complète sur les contenus de tiers.
- Ne pas prétendre que les traitements de pseudonymisation/purge sont réalisés par ce seul script de catalogue.

## Validation
Data 1 : ______  DPO 1 : ______  DPO 2 : ______  Date : ______

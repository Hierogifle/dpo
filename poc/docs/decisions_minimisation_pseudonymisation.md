# FashMatch POC — J2-02 / Décisions techniques et questions DPO

| Champ | Traitement dans le POC | Motif |
| --- | --- | --- |
| product_id, category, subcategory, article_type, color, season, usage, product_name | Conservé | Catalogue produit utile au POC, aucune donnée client |
| gender, year (catalogue Kaggle brut) | Exclu du catalogue préparé | Minimisation pédagogique du périmètre du POC |
| budget_max_eur, preferred_sizes | Supprimés des profils V2 | Aucun champ prix/taille correspondant dans le catalogue |
| preferred_categories, preferred_colors | Alignés avec les valeurs réelles Kaggle | Compatibilité des vocabulaires |
| preferred_usages | Remplace preferred_styles | Champ `usage` disponible (mais n'est PAS une taxonomie parfaite de styles) |
| first_name, last_name, email | Fictifs; zone privée | Démontrer le flux de pseudonymisation; aucune personne réelle |
| user_id | Remplacé par identifiant HMAC côté jeu exploitable | Relier techniquement sans exposer les identifiants initiaux |
| created_at, retention_until | Conservés | Démonstration de la purge J3; 90 jours hypothétiques |

Points à confirmer avec les DPO : durée réaliste par finalité pour une éventuelle V2 de production, base légale des traitements, politique de suppression des données annexes / sauvegardes, et périmètre des contrôles. L'identifiant pseudonymisé n'est pas une anonymisation au sens RGPD. Les dossiers `/data/private/` et `/data/raw/` ne doivent pas être rendus publics.

# Note pédagogique Data/IA → DPO — FashMatch, préparation des données

**But** : étudier un catalogue de vêtements public et des profils fictifs pour préparer un POC de traitement conforme, sans traiter de photos de personnes.

**Origine des informations** : produits de Kaggle « Fashion Product Images (Small) », profils créés localement par script à partir de choix aléatoires contrôlés. Les profils ne représentent aucun client.

**Pourquoi réduire les champs ?** La démonstration explore catégories, couleurs et usages. Le pipeline écarte l'année de référencement et le public commercial cible (`gender`) parce qu'ils ne sont pas nécessaires au périmètre choisi. Il ne s'agit pas d'affirmer que ces champs sont toujours interdits.

**Qualité** : certaines lignes du CSV brut sont incorrectes et sont rejetées par le parseur. Le rapport versionné ventile désormais les exclusions. Le catalogue final peut encore comporter des informations manquantes ; ce n'est pas synonyme de non-conformité, mais doit être pris en compte.

**Points de vigilance** : prix et tailles du catalogue non fournis ; catégories et styles des profils fictifs non directement compatibles avec les champs Kaggle. La durée de 90 jours est une hypothèse pédagogique.

**Questions à arbitrer en équipe** : finalité exacte du POC ; champs nécessaires ; politique de conservation et suppression pour une vraie V2 ; conditions de réutilisation du dataset ; traitement des photos (hors POC) ; règles d'acceptation des données et risques de couverture inégale des usages.

**Ne pas confondre** : une donnée synthétique inventée ne devient pas une donnée personnelle simplement parce qu'elle possède un `user_id` fictif. Une donnée réellement liée à quelqu'un resterait personnelle même pseudonymisée.

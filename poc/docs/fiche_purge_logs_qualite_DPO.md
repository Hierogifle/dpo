# FashMatch — Mesures de POC J3, à examiner avec les DPO

**Purge** : suppression des enregistrements fictifs dont `retention_until` est strictement antérieure à la date de référence, dans le jeu pseudonymisé, les identités de démonstration et la correspondance privée. Mode simulation par défaut. Les données de l'échéance sont fictives, les **90 jours restent à valider**.

**Traçabilité** : `traitements.jsonl` enregistre uniquement date UTC, nature de l'opération, statut et compteurs. Pas de noms, courriels, identifiants ou contenu des préférences. Les logs de traitement ne sont pas équivalents à des logs d'accès.

**Qualité** : contrôles automatisés des colonnes minimales, des champs non souhaités, des doublons, des catégories/couleurs/usages autorisés, des dates et de la mention `synthetic`. Rapport lisible par les deux équipes.

**Limites** : aucune donnée réelle, aucun selfie ou chat, pas de tiers externes, pas de sauvegarde gérée par le script, pas de garanties ACID multi-fichiers. Les sorties pseudonymisées ne sont pas anonymisées par principe. Des politiques de conservation propres aux finalités réelles seront requises.

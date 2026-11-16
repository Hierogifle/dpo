# FashMatch — Synthèse des métriques J4-02

## Résultats vérifiés à partir des rapports du POC

- **41 890** produits conservés ; **44 424** lignes source chargées (avant filtrage, hors lignes éventuellement mal formées rejetées à la lecture).
- **80** profils utilisateurs entièrement fictifs pseudonymisés.
- **0** anomalie détectée sur les profils par les contrôles disponibles ; **0** identifiant dupliqué.
- **32 187** articles d'usage Casual, soit **76.84 %** du catalogue.
- **83** cellules manquantes dans le catalogue préparé (ne pas confondre avec le nombre de lignes concernées).
- **94.3 %** de lignes source *chargées* retenues dans le catalogue ; ne pas utiliser comme taux brut d'import sans auditer les rejets CSV.
- Durée de conservation **90 jours**, fictive et paramétrable.

## Tests et purge

L'équipe a observé **5/5 tests réussis** et deux simulations : **0 profil concerné au 01/09/2026** ; **80 au 01/02/2027**. Ces valeurs sont des constats de la précédente exécution. Relancer la suite et les simulations pendant la préparation de la démo pour les reconfirmer.

## Ce que ces métriques ne démontrent pas

- Pas de preuve d'une qualité de recommandation, de l'absence de biais ou de l'efficacité d'un système IA.
- Pas de preuve de conformité RGPD en production : aucune donnée utilisateur réelle utilisée.
- La pseudonymisation n'est pas l'anonymisation. La table de correspondance et les identités fictives sont isolées dans `data/private/` et ne doivent pas être partagées.
- Les logs J3 sont ceux du pipeline, **pas** une traçabilité complète des accès et traitements de Stella, Cabine ou Pay3x.
- La purge réelle est vérifiée par tests isolés ; ne jamais exécuter `--apply` sur la copie principale pendant la soutenance.
- Les choix d'architecture V2 et durées réelles par finalité sont des arbitrages distincts relevant de L1/L4/L5.

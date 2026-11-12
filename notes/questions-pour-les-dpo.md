# FashMatch · Questions Data/IA pour les DPO

*12 novembre 2026 · Romuald*

Cette note ne tranche rien : elle liste les questions dont nous avons besoin des réponses pour avancer sur l'architecture V2 et le POC. Les qualifications juridiques restent les vôtres.

## Questions par module, pour la matrice L1

Pour chaque module, la question de fond est la même : garder, encadrer ou retirer ? Voici ce qui nous aiderait à dessiner la V2.

**Match · Recommandation**

- Quelle base légale retenez-vous pour la recommandation personnalisée ? Selon la réponse, faut-il un bouton d'opposition ou un retrait du consentement ?
- Quelle durée de conservation remplace les 5 ans actuels, pour l'historique de navigation et pour l'historique d'achats ?
- Le suivi de navigation passe-t-il par des traceurs qui demandent un bandeau de consentement ?

**Cabine · Essayage virtuel**

- Comment qualifiez-vous l'import de la photo d'une autre personne : traitement illicite, violation de données, autre ? La réponse change ce que nous devons prévoir techniquement.
- Faut-il conserver le selfie, l'image générée, ou ni l'un ni l'autre après la session ?
- L'entraînement des modèles sur les photos des clients peut-il continuer ? Si oui, à quelles conditions ?
- Quelles obligations de l'art. 50 de l'AI Act s'appliquent ici, et à qui : mention visible, marquage lisible par machine, ou les deux ?

**Stella · Styliste**

- Peut-on garder les conversations, et combien de temps ? Une anonymisation réelle d'un texte libre vous semble-t-elle démontrable ?
- Le fournisseur du modèle est-il sous-traitant seulement, ou devient-il responsable s'il entraîne ses modèles sur nos conversations ?

**Âge · Contrôle à l'inscription**

- L'estimation faciale reste-t-elle acceptable si la photo n'est pas conservée et qu'une méthode alternative est proposée ?
- Qui doit opérer le contrôle : FashMatch ou un tiers indépendant, comme le recommande la CNIL ?
- Le seuil de 15 ans est-il le bon, au regard de la majorité numérique ?

**Pay3x · Paiement fractionné**

- Le score Pay3x est-il un système d'IA au sens de l'AI Act ? S'il l'est, relève-t-il du haut risque (évaluation de la solvabilité) ?
- Quel âge minimum pour le paiement fractionné, et comment le vérifier ?
- Que doit contenir le refus pour respecter l'art. 22 : motif, intervention humaine, contestation ?

**Insight · Segmentation**

- Déduire religion, orientation sexuelle et origine à partir de photos relève-t-il de la catégorisation biométrique interdite par l'AI Act ? Si oui, le module disparaît de la V2.
- Une segmentation marketing sans photos ni données sensibles est-elle une alternative acceptable à proposer à la direction ?

## Questions transverses pour l'architecture V2

Ces réponses décident de boîtes et de flèches entières sur le schéma V2.

- **Localisation** : tout doit-il rester dans l'UE, ou des transferts hors UE sont-ils acceptables avec des garanties ? Cela concerne l'hébergeur et le fournisseur du modèle de Stella.
- **Contrats** : quels tiers ont besoin d'un contrat de sous-traitance (hébergeur, fournisseur du modèle, prestataire de paiement, outil marketing) ?
- **Durées** : pouvez-vous nous donner une durée par catégorie de données ? Nous la transformerons en purge automatique.
- **Supervision humaine** : sur quels modules une décision doit-elle pouvoir être revue par un humain, et dans quel délai ?
- **Information des personnes** : à quels moments du parcours l'utilisateur doit-il être informé (inscription, premier essayage, premier message à Stella, demande Pay3x) ?
- **AIPD** : quels modules en demandent une ? Le schéma des flux peut servir de base à la description des traitements.
- **Rôle de FashMatch** : fournisseur ou déployeur, pour chaque système d'IA ? Cela change les obligations que nous devons rendre visibles dans l'architecture.
- **La crise** : pour la personne dont l'image circule sur un forum, qu'attendez-vous techniquement de nous (retrouver l'image, supprimer les données, tracer qui l'a générée) ?

## Décisions attendues pour le POC

Aurélien a posé 8 questions dans `poc/docs/fiche_source_et_DPO.md`. Les trois premières bloquent la suite :

1. **Réutilisation du dataset Kaggle** : autorisez-vous ses métadonnées pour une démonstration pédagogique ? Et peut-on publier le fichier brut sur GitHub, ou faut-il seulement le script qui le télécharge ?
2. **Champs des profils synthétiques** : lesquels sont indispensables, et pour quelle finalité ? Nous proposons de retirer le budget et la taille, inutilisables sans prix ni tailles dans le catalogue.
3. **Durée de conservation à tester** : les 90 jours actuels sont une hypothèse. Quelle durée et quelle règle de purge voulez-vous voir démontrées ?

Une question de notre côté : pour démontrer la pseudonymisation, nous voulons ajouter aux profils des identifiants fictifs (nom, e-mail inventés). Cela vous semble-t-il une démonstration valable ?

## Ce que nous vous demandons de valider

- [ ] **L'architecture V1** (J1-01, `data-ia/architecture-v1.html`) : chaque fait est sourcé, chaque hypothèse est marquée en pointillés. Si une hypothèse est fausse, dites-le-nous, nous corrigerons le schéma et les tableaux ensemble.
- [ ] **Les données du POC** (J1-02) : le dictionnaire de données et les deux notes d'Aurélien dans `poc/docs/`.
- [ ] **La colonne « Source »** de nos futures mesures V2 : nous vous l'enverrons ligne par ligne dès que la matrice L1 sera décidée.

Pour la matrice L1 elle-même, nous proposons une séance commune : vous qualifiez, nous expliquons ce qui est faisable techniquement et ce que coûte chaque option.

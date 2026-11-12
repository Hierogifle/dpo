# FashMatch · Note de synthèse perso

*12 novembre 2026 · Romuald · usage personnel, ne pas diffuser*

## Où en est le projet

Au matin du 12 novembre, une tâche sur 20 est en attente de validation dans le planning (J1-02, le POC d'Aurélien) et aucune n'est terminée. La soutenance a lieu la semaine prochaine.

| Rôle | Qui | Tâche jour 1 | État réel |
| --- | --- | --- | --- |
| Data 1 | Moi | J1-01 · cartographier les 6 modules et les flux V1 | Fait (architecture V1), pas encore coché dans le planning |
| Data 2 | Aurélien | J1-02 · données du POC | Fait, en attente de validation |
| DPO 1 | Collègue DPO | J1-03 · traitements, finalités, problèmes RGPD, début L4 | En cours : 4 modules sur 6 dans le docx du drive |
| DPO 2 | Collègue DPO | J1-04 · textes, échéances, début L3 et L5 | Rien de visible sur le drive |
| Tous | — | J1-05 · matrice L1 garder / encadrer / retirer | Pas commencée |

Le dépôt GitHub `Hierogifle/dpo` a trois branches : `main` et `Aure` (même commit, le POC), et `romuald` (le POC, plus mon architecture, le sujet rangé dans `sujet/` et les notes dans `notes/`). Rien n'est encore fusionné.

## Mon travail : l'architecture V1

L'architecture V1 couvre J1-01 et la moitié V1 de J2-01. Elle est commitée dans `data-ia/architecture-v1.html`.

Elle contient le schéma (personnes, accès, API, 6 modules, 8 stockages, 4 tiers), le tableau des 27 flux, le pipeline V1 en 6 étapes par module, l'inventaire des données, les tiers, la couche transverse manquante et 12 hypothèses.

Ce qui est solide, car sourcé dans l'énoncé ou les decks :

- les 6 modules et ce qu'ils font ;
- photos en clair dans un bucket, hébergeur dont certains services sont hors UE ;
- accès internes non journalisés, pas d'audit d'accessibilité, pas de DPO ni de référent IA ;
- 5 ans de conservation pour Match (énoncé) et pour les photos (deck), réutilisation des photos pour l'entraînement (deck) ;
- les trois incidents de la crise.

Ce que je dois pouvoir défendre comme un choix de modélisation, et non comme un fait :

- l'API unique, la console interne, le découpage en 8 bases et leurs noms ;
- le fait que Pay3x soit une IA (l'énoncé dit seulement « score ») : à trancher par le DPO 2 dans L5 ;
- quelques formulations déduites : « âge déclaré non fiable », « image impossible à rappeler », Insight lit « toutes » les photos.

À faire sur ce livrable : ajouter une phrase en tête qui dit que le découpage technique est une modélisation de l'équipe, et le faire valider par les deux DPO (c'est la règle du planning).

## Le POC d'Aurélien

Le POC est sérieux et reproductible, mais un tiers ne peut pas encore le relancer. Il couvre le module Match (catalogue + préférences déclarées).

Vérifié en relançant ses scripts sur une copie :

- 44 446 produits Kaggle en entrée, 22 lignes mal formées rejetées, 2 534 produits hors cible exclus, **41 890 produits** en sortie ; chaque exclusion est comptée et contrôlée ;
- catalogue nettoyé et 80 profils régénérés **identiques octet pour octet** ; **3 tests sur 3** passent ;
- dictionnaire de données avec finalité et décision par champ, deux notes prudentes pour les DPO ;
- déséquilibre réel repéré : « Casual » = 77 % du catalogue, Party, Travel et Smart Casual sous 0,2 %.

Problèmes vérifiés :

| Problème | Effet |
| --- | --- |
| Noms de fichiers synthétiques incohérents entre script, dépôt et EDA | Marche sous Windows par hasard de casse, casse sous Linux ou en conteneur |
| `requirements.txt` limité à pandas, pas de conteneur | Un tiers ne peut pas l'exécuter, exigence de l'énoncé non tenue |
| README racine obsolète et mal placé | Dit « non exécuté » et « non redistribué », chemins faux |
| `.gitignore` sans effet sur `poc/data/raw` | Le CSV Kaggle brut est publié alors que sa redistribution n'est pas validée |
| Deux catalogues (Kaggle + 120 produits synthétiques en français) | Profils alignés sur le synthétique, pas sur Kaggle |
| Profils sans identifiant direct | Rien à pseudonymiser : la démo tomberait à plat |
| `budget_max_eur` et `preferred_sizes` inutilisables | À retirer pour montrer la minimisation |

Ce qui manque encore (il le sait) : pseudonymisation, purge automatique, journalisation, rapport de qualité sur les profils.

## Le document juridique des DPO

« Problèmes juridiques de chaque module » (drive, 11 nov.) traite 4 modules sur 6 : Pay3x et Insight sont vides. C'est leur travail, je ne le réécris pas ; ces remarques servent à orienter mes questions.

Bons réflexes : conservation de 5 ans excessive (art. 5), profilage (art. 4 et 21), transparence (art. 12 à 14), traceurs (art. 82 LIL), mention IA (art. 50 AI Act), fournisseur de Stella = sous-traitant (art. 28), art. 22 et contestation pour Âge, focus CNIL sur l'estimation de l'âge.

Points fragiles :

- Cabine : « violation de donnée personnelle » est le mauvais terme. Une violation (art. 4.12) est un incident de sécurité ; importer la photo d'un tiers est un traitement illicite.
- Stella : « anonymiser et plus aucun souci » est trop optimiste pour du texte libre, souvent seulement pseudonymisé.
- Âge : l'angle « discrimination » est faible ; le vrai sujet est la fiabilité (la fille de 14 ans est passée). Le seuil de 15 ans renvoie à la majorité numérique (art. 8 RGPD, art. 45 LIL).
- Une source citée comme « un site de veille juridique », sans nom : l'énoncé demande des sources évaluées.

Manques qui touchent mon architecture : Insight (art. 9 RGPD et catégorisation biométrique interdite par l'art. 5(1)(g) de l'AI Act, sans doute « retirer »), Pay3x (art. 22, mineurs, haut risque possible), transferts hors UE, sécurité (art. 32), entraînement sur les photos, base légale de chaque module.

## Risques pour la soutenance

Le plus gros risque est que la matrice L1 n'existe toujours pas : tout le reste (architecture V2, cahier des charges, POC) en dépend.

| Risque | Pourquoi | Parade |
| --- | --- | --- |
| L1 pas décidée | Je ne peux pas dessiner la V2 sans savoir ce qui est gardé ou retiré | Pousser une séance L1 commune dès que possible |
| POC non relançable par un tiers | Exigence explicite de l'énoncé | Fichier des dépendances, conteneur, README dans `poc/` |
| Pseudonymisation démontrée sur des profils sans identifiant | Le jury verra que la démo ne prouve rien | Ajouter des identifiants fictifs aux profils |
| Dataset Kaggle publié sans décision des DPO | Contradiction avec nos propres notes | Faire trancher la question 1 de la fiche source |
| Documents incohérents entre eux | Erreur listée par l'équipe pédagogique | Relecture croisée (J3-05) avec la matrice de traçabilité |
| Hypothèses présentées comme des faits | Un DPO ou le jury peut tomber dessus | Garder les pointillés et le mot « hypothèse » jusqu'au bout |
| Aurélien malade | Retard sur purge, logs, pseudonymisation | Prendre une partie si son absence dure |

## Mes prochaines actions

- [ ] Cet après-midi : présenter la data et l'IA aux DPO, puis notre travail, y compris la partie d'Aurélien
- [ ] Envoyer la note Data/IA à Aurélien et la note de questions aux DPO
- [ ] Cocher J1-01 « en attente de validation » dans le planning, avec le lien de l'architecture
- [ ] Ajouter en tête de l'architecture la phrase « découpage technique = modélisation de l'équipe »
- [ ] Obtenir la matrice L1 avec les DPO, puis dessiner l'architecture V2 (J2-01) sur le même gabarit
- [ ] Préparer le pipeline avant / après et la matrice de traçabilité (J3-01)

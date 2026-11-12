# FashMatch · Note Data/IA : retour sur le POC

*12 novembre 2026 · Romuald*

Aurélien, j'ai relu tout `poc/` et relancé tes scripts sur une copie : le travail est solide et reproductible. Quelques corrections sont nécessaires pour qu'un tiers puisse le relancer, comme l'exige l'énoncé.

## Ce qui est solide

- **Comptes justes et tracés** : 44 446 produits en entrée, 22 lignes mal formées rejetées, 2 534 hors cible, 41 890 en sortie. Le contrôle de cohérence des comptes est une très bonne idée.
- **Reproductible** : en relançant tes scripts, le catalogue et les 80 profils ressortent identiques octet pour octet. Les 3 tests passent.
- **Minimisation documentée** : le dictionnaire de données donne la finalité et la décision champ par champ. C'est exactement ce que les DPO attendent.
- **Notes DPO prudentes** : pseudonymisation ≠ anonymisation, licence MIT présentée sans sur-promesse, 90 jours présentés comme une hypothèse.
- **EDA utile** : « Casual » fait 77 % du catalogue, Party, Travel et Smart Casual moins de 0,2 %. C'est un déséquilibre à citer en soutenance.

## À corriger, par priorité

1. **Noms des fichiers synthétiques.** `generate_data.py` écrit `catalogue_DEMONSTRATION_SYNTHETIQUE.csv` et `profils_utilisateurs_SYNTHETIQUES.csv`, le dépôt contient `catalogue_synthetique.csv` et `profils_utilisateurs_synthetiques.csv`, et l'EDA cherche la version en majuscules. Sous Windows ça passe car la casse est ignorée ; sous Linux ou en conteneur, l'analyse des profils est sautée sans erreur. Un seul nom partout.
2. **Dépendances et environnement.** `requirements.txt` ne contient que pandas : il manque matplotlib, kagglehub et pytest. L'énoncé demande un POC exécutable par un tiers (README, dépendances, conteneur ou environnement reproductible) : un Dockerfile simple suffirait.
3. **README.** Celui à la racine décrit le POC mais dit « non exécuté » et « non redistribué », ce qui est faux aujourd'hui, et ses chemins `docs/...` pointent à côté. Je propose de le déplacer dans `poc/README.md` et de garder la racine pour l'organisation du dépôt.
4. **`.gitignore`.** La règle `data/raw/*` ne vise que la racine, pas `poc/data/raw/` : le CSV Kaggle brut est publié sur GitHub, alors que ta fiche demande justement aux DPO si on peut le redistribuer. Corriger la règle et retirer le fichier du suivi Git, en attendant leur réponse.
5. **Un seul catalogue.** Le catalogue synthétique de 120 produits (en français, prix et tailles inventés) et le catalogue Kaggle coexistent, et les profils sont alignés sur le synthétique. Je propose de garder Kaggle et d'aligner les catégories des profils dessus (c'est la tâche que tu avais notée).
6. **Profils.** Ils n'ont aucun identifiant direct, donc rien à pseudonymiser. Ajouter des identifiants fictifs (nom, e-mail factice) rendrait la démo parlante. Et retirer `budget_max_eur` et `preferred_sizes`, inutilisables sans prix ni tailles dans Kaggle : c'est une belle démo de minimisation.

## La suite : conformité du pipeline et répartition

Le POC doit démontrer les mesures du cahier des charges sur le module Match. Je propose cette répartition, à ajuster selon ton état de santé.

| Mesure à démontrer | Ce que le POC doit montrer | Qui | Planning |
| --- | --- | --- | --- |
| Minimisation | Champs inutiles retirés avant tout traitement, justifiés par le dictionnaire | Aurélien | J2-02 |
| Pseudonymisation | Identifiants fictifs remplacés par un jeton, table de correspondance séparée | Aurélien | J2-02 |
| Purge automatique | Suppression des profils dont `retention_until` est dépassé, avec trace | Aurélien | J3-02 |
| Journalisation | Un journal des traitements : qui, quoi, quand, combien de lignes | Aurélien | J3-02 |
| Rapport qualité | Complétude, doublons, cohérence et déséquilibres, aussi sur les profils | Aurélien | J3-02 |
| Lien avec l'architecture | Chaque mesure du POC reliée à une exigence du cahier des charges | Romuald | J3-01 |

De mon côté : architecture V2 (J2-01) dès que la matrice L1 est décidée, puis cahier des charges, schémas avant / après et matrice de traçabilité (J3-01). Si tu restes malade, je reprends la purge ou la journalisation.

## Mes questions pour toi

- [ ] Es-tu d'accord pour garder uniquement le catalogue Kaggle et abandonner le synthétique ?
- [ ] Tu préfères un Dockerfile ou un simple environnement virtuel documenté ?
- [ ] Je déplace le README dans `poc/`, ou tu le fais sur ta branche pour éviter un conflit ?
- [ ] Quelle durée de purge veux-tu tester ? Les 90 jours actuels sont à valider par les DPO.
- [ ] Pour la présentation aux DPO, y a-t-il un point de ton travail que tu tiens à ce que je mette en avant ?

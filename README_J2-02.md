# FashMatch — J2-02 : ingestion, nettoyage, minimisation, pseudonymisation

## Installation sans écraser le dépôt
Copier **le contenu** de `poc/` dans le dossier `poc/` du projet. Sauvegarder les fichiers en conflit et comparer les différences (`git diff`) avant remplacement : `src/generate_data.py` est volontairement révisé (suppression de la génération du catalogue synthétique). Ne pas remplacer `src/prepare_catalogue.py`, `src/analyse_catalogue.py`, ni les tests J1 : ils sont conservés.

- `poc/src/generate_data.py` : remplace l'ancienne génération de 120 produits fictifs par 80 profils fictifs, catégories/couleurs/usages issus du catalogue Kaggle réel.
- `poc/src/pseudonymize_profiles.py` : génère des pseudonymes HMAC à partir des identifiants et une table de correspondance séparée.
- `poc/.gitignore` : règles relatives à `poc/`. **Si le dépôt utilise un `.gitignore` à la racine, les règles doivent être préfixées de `poc/`.** Vérifier avec `git check-ignore -v poc/data/raw/styles.csv` depuis la racine.
- `poc/requirements.txt` : ajouter ces dépendances à celles existantes, sans supprimer les autres.

## Commandes depuis `poc/`
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/download_catalogue.py             # si le script J1 existe et si nécessaire
python src/prepare_catalogue.py
python src/generate_data.py
python src/pseudonymize_profiles.py
python src/analyse_catalogue.py
```
Sous Linux/macOS : `source .venv/bin/activate`.

**Nom unique compatible EDA :** `data/synthetic/profils_utilisateurs_SYNTHETIQUES.csv` (respecter la casse). Le catalogue Kaggle reste `data/processed/catalogue_fashmatch.csv`. Ne plus relancer l'ancien générateur de catalogue de démonstration : le nouveau ne crée plus `catalogue_DEMONSTRATION_SYNTHETIQUE.csv`. Supprimer l'ancien fichier du dépôt uniquement après revue Git.

## Séparation des données
- `data/private/profils_identifiants_SYNTHETIQUES.csv` : **identités fictives source**, non versionnées.
- `data/private/correspondance_profils.csv` : **table de correspondance**, non versionnée.
- `data/private/.pseudonym_key` : **secret HMAC** local, non versionné et non partagé.
- `data/synthetic/profils_utilisateurs_SYNTHETIQUES.csv` : profils **pseudonymisés**, entièrement fictifs; ne contiennent ni nom ni email.

La clé HMAC est générée aléatoirement à la première exécution; elle est conservée dans `data/private` pour garantir une pseudonymisation stable aux nouvelles exécutions. **Ne jamais commiter le dossier `data/private/`.** Révoquer et renouveler la clé si elle est divulguée.

## Décisions de minimisation
Suppression de `budget_max_eur` et `preferred_sizes` : le catalogue Kaggle ne possède pas de prix ni de tailles. `preferred_styles` devient `preferred_usages`, calqué sur les usages réellement présents dans le catalogue. Catégories et couleurs également échantillonnées depuis ce catalogue.

Le mécanisme HMAC et l'isolement de la table illustrent la pseudonymisation; ils ne garantissent pas une anonymisation. Une base légale, la sécurité, l'accès restreint et les durées de conservation pour de vrais utilisateurs seraient à définir avec les DPO.

**Durée de 90 jours :** valeur illustrative du POC, en attente d'un arbitrage formel des DPO; elle n'est pas présentée comme une exigence légale.

## Vérification Git
Depuis la racine du dépôt : `git status --short`, puis `git check-ignore -v poc/data/private/.pseudonym_key poc/data/raw/styles.csv`. Si un fichier brut a déjà été commité, ajouter `.gitignore` ne le retire PAS du suivi : `git rm --cached poc/data/raw/styles.csv` (sans effacer le fichier local), suivi d'un commit. Cela ne supprime pas les copies dans l'historique déjà publié : demander un arbitrage sur la redistribution et l'historique si nécessaire.

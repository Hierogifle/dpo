# Points ouverts de la V2 : ce que dit le droit, ce qu'on propose

Recherche du 14 novembre 2026, faite pour les huit points laissés ouverts dans l'architecture V2 (`data-ia/architecture-v2.html`).

Chaque point suit le même ordre :
- ce que disent les textes ;
- les options possibles ;
- notre proposition ;
- ce que ça change dans l'architecture.

Les sources sont listées en fin de note. Beaucoup viennent de cabinets d'avocats ou de sites spécialisés : elles sont marquées *(source secondaire)*, et les DPO vérifient le texte officiel (Légifrance, EUR-Lex) avant de s'en servir.

---

## Ce qui a changé depuis la V2 d'hier

1. **Le paiement en 3 fois devient du crédit à la consommation le 20 novembre 2026, dans six jours.**
   - Textes : directive (UE) 2023/2225, transposée par l'ordonnance n° 2025-880 du 3 septembre 2025.
   - Ce qui ne change pas : le choix de tout confier à un prêteur agréé est confirmé.
   - Ce qui s'ajoute : FashMatch a des obligations en tant que vendeur (point 4).
2. **L'article 50 de l'AI Act (transparence) s'applique depuis le 2 août 2026.**
   - Le Digital Omnibus (règlement (UE) 2026/1744) ne l'a pas reporté. Il a seulement repoussé les systèmes à haut risque de l'annexe III au 2 décembre 2027.
   - Le code de bonnes pratiques sur le marquage et l'étiquetage des contenus générés par IA est publié depuis le 10 juin 2026.
3. **Correction de mon côté : pour Stella, FashMatch n'est pas seulement déployeur.**
   - En intégrant un modèle Mistral dans un assistant mis en service sous son propre nom, FashMatch devient **fournisseur du système d'IA Stella**. Mistral reste fournisseur du modèle à usage général.
   - L'obligation d'annoncer qu'on parle à une IA (art. 50.1) pèse sur le fournisseur du système, donc sur nous.
   - La mesure prévue ne change pas. Le rôle à inscrire dans le L5, oui.
4. **Par défaut, Mistral conserve les requêtes envoyées à son API pendant 30 jours**, pour surveiller les abus. Avec l'API standard, la décision « aucune conservation » n'est donc pas tenue (point 6).

---

## 1. Les 15–17 ans dans Cabine

**Ce que disent les textes**
- **Consentement.** À partir de 15 ans, un mineur consent seul (RGPD art. 8 ; loi Informatique et Libertés art. 45). Rien n'interdit donc Cabine aux 15–17 ans.
- **Protection renforcée.** Le RGPD demande une protection particulière des enfants (considérant 38) et une information adaptée à leur âge (art. 12.1).
- **Hypertrucage.** Une image générée de soi-même ressemble à une personne existante : c'est un hypertrucage au sens de l'AI Act (art. 3.60). Il faut l'**étiqueter** (art. 50.4) en plus du **marquage lisible par machine** (art. 50.2).
- **Risque pénal.** Le risque existe si l'outil sert à fabriquer l'image de quelqu'un d'autre : Code pénal art. 226-8 et 226-8-1, modifiés par la loi SREN du 21 mai 2024, qui couvrent aussi les hypertrucages à caractère sexuel. Le test du vivant (seule la personne devant la caméra) répond à ce risque.
- **DSA.** L'article 28 du DSA ne vise que les plateformes en ligne, c'est-à-dire celles qui diffusent au public des contenus d'utilisateurs. FashMatch n'en est probablement pas une. Les lignes directrices de la Commission du 14 juillet 2025 restent la référence de bonnes pratiques pour les mineurs.

**Options**
- A. Cabine réservée aux 18 ans et plus.
- B. Cabine ouverte aux 15–17 ans en « mode protégé ».
- C. Cabine ouverte aux 15–17 ans avec accord parental. Juridiquement inutile dès 15 ans, et lourd à mettre en œuvre.

**Notre proposition : B**, avec A en repli si les DPO jugent le risque trop élevé. Le mode protégé comprend :
- un catalogue restreint, sans maillots de bain ni lingerie (les sous-vêtements sont déjà exclus pour tous) ;
- aucun export ni partage vers les réseaux sociaux : l'image reste affichée dans l'app, avec une mention visible « Générée par IA » ;
- une information rédigée pour un public de 15 ans (art. 12.1) ;
- les mêmes garanties que pour les adultes : aucune image conservée, test du vivant, journal de génération de 6 mois.

**Impact sur l'architecture.** Le tiers de confiance renvoie une tranche d'âge (« 15–17 » ou « 18+ ») au lieu d'un simple oui / non. La passerelle active le mode protégé selon cette tranche. Aucune date de naissance n'est stockée.

---

## 2. Contester l'estimation de l'âge

**Ce que disent les textes**
- **CEPD.** Sa déclaration 1/2025 du 11 février 2025 demande de proposer une autre méthode à ceux qui ne peuvent pas ou ne veulent pas utiliser la première. Il recommande les solutions où le service apprend seulement si la personne est au-dessus ou en dessous du seuil.
- **Lignes directrices DSA art. 28 (Commission, juillet 2025).**
  - Au moins deux méthodes doivent être proposées, avec un recours en cas d'erreur.
  - La simple déclaration de l'utilisateur ne suffit pas.
  - L'estimation doit venir d'un tiers indépendant ou d'un système audité.
- **AI Act.** L'estimation de l'âge par le visage est probablement une **catégorisation biométrique** (art. 3.40). Le déployeur doit alors en informer les personnes (art. 50.3, applicable depuis le 2 août 2026). *(Lecture d'une source spécialisée, à confirmer.)*
- **RGPD art. 9.** Le débat est ouvert : sans identification, ce n'est pas une donnée biométrique au sens strict.
  - La CNIL n'a pas tranché la question.
  - En juillet 2025, elle s'est opposée aux caméras qui estiment l'âge en continu dans les bureaux de tabac, qu'elle juge ni nécessaires ni proportionnées.
  - Par prudence, on applique les garanties de l'article 9.
- **RGPD art. 22.** Un refus d'accès fondé uniquement sur une estimation automatique ouvre trois droits : obtenir une intervention humaine, donner son point de vue et contester la décision.
- **Fiabilité.** L'estimation par le visage est la moins fiable autour du seuil, et notre seuil (15 ans) est bas.

**Notre proposition : trois méthodes au choix dès l'inscription, plus un recours humain**
1. **Preuve d'âge en double anonymat**, proposée en premier : France Identité ou l'application européenne de vérification de l'âge.
   - L'application européenne est testée en 2026 dans sept pays, dont la France.
   - La Commission demande qu'elle soit disponible dans chaque pays d'ici fin 2026. Des preuves « 15+ » et « 18+ » sont en test.
2. **Estimation par le visage chez le tiers**, sans conservation. Elle n'est acceptée que si l'âge estimé dépasse nettement le seuil. Sinon, on bascule vers la méthode 1 ou 3.
3. **Pièce d'identité contrôlée par le tiers**, puis supprimée. Seule la tranche d'âge revient à FashMatch.

**Recours.** Un formulaire de contestation déclenche une revue par le support. Le support ne voit jamais la photo : il propose une autre méthode et répond sous un délai à fixer avec les DPO (nous proposons 72 h).

**Information (art. 50.3 et art. 13).** Avant toute prise de vue, un écran explique :
- que l'âge est estimé par une IA ;
- que rien n'est conservé ;
- quelles autres méthodes existent.

**Impact sur l'architecture**
- Le tiers de confiance propose les trois méthodes.
- Une nouvelle exigence s'ajoute à la matrice : EX-21, « le client sait que son âge est estimé par une IA ».
- La source d'EX-14 est complétée par les lignes directrices DSA.

---

## 3. Le registre L4 (travail des DPO, liste de ce qui doit bouger)

- **Pay3x.**
  - À retirer : le scoring interne et le stockage du numéro de carte.
  - Le prêteur est **responsable de traitement distinct** : c'est ce que disent ses propres conditions générales (par exemple chez Oney).
  - FashMatch ne lui transmet que la commande.
- **Stella.** À indiquer :
  - finalité, base légale et absence de conservation ;
  - destinataire : le fournisseur du modèle, sous-traitant au sens de l'art. 28.
- **Nouveaux traitements à créer.**
  - Comptes clients.
  - Commandes et facturation : 10 ans, Code de commerce L123-22.
  - Communication commerciale : consentement, CPCE L34-5.
  - Preuves de consentement.
  - Journalisation de sécurité (art. 32).
  - Journal de génération Cabine : intérêt légitime, 6 mois.
  - Vérification de l'âge.
- **Pour chaque traitement** : les destinataires et l'absence de transfert hors UE. Cette information manque encore dans le registre.

---

## 4. Le prestataire de paiement fractionné

**Ce que disent les textes**
- **Changement de régime.** À partir du 20 novembre 2026, le paiement en 3 ou 4 fois devient un crédit à la consommation, **même sans frais**.
  - Les contrats conclus avant cette date restent sous l'ancien régime.
  - Seul le paiement différé accordé par le vendeur lui-même, sans tiers ni intérêts et soldé rapidement, reste exclu. *(source secondaire)*
- **Côté prêteur.**
  - Il doit évaluer la solvabilité de façon approfondie (directive art. 18 ; Code de la consommation L312-16), sans utiliser les données des réseaux sociaux.
  - Si l'évaluation est automatisée, le client a droit à une intervention humaine, à une explication et à un réexamen (directive art. 18.8).
  - S'y ajoute le RGPD art. 22, éclairé par deux arrêts de la CJUE : **SCHUFA** (C-634/21, 7 décembre 2023), qui assimile un score de crédit déterminant à une décision automatisée, et **Dun & Bradstreet Austria** (C-203/22, 27 février 2025), sur l'explication due au client.
- **AI Act.** L'évaluation de la solvabilité est un système à **haut risque** (annexe III, point 5.b). Les obligations sont reportées au 2 décembre 2027 et portées par le prêteur.
- **Côté vendeur (FashMatch)** *(sources secondaires, articles à vérifier sur Légifrance)* :
  - le crédit doit figurer dans le contrat de vente (Code de la consommation L312-45) ;
  - la publicité doit porter l'avertissement obligatoire, et les formules comme « accepté pour tous » sont interdites (L312-5 à L312-10) ;
  - FashMatch risque d'être qualifié d'**intermédiaire de crédit** (Code monétaire et financier L519-1) s'il choisit le prêteur, collecte les données du client et présente lui-même l'offre.

**Notre proposition**
- **Critères de choix du prêteur.**
  1. Agrément vérifié sur le registre REGAFI (ACPR).
  2. Parcours conforme à la nouvelle directive dès le 20 novembre, avec une revue humaine documentée.
  3. Données hébergées dans l'UE.
  4. FashMatch ne reçoit que « accepté / refusé » et l'état des échéances.
  5. Un contrat qui dit qui explique un refus et qui traite un réexamen.
  6. Les mentions de publicité fournies par le prêteur.
- **Alma, Oney et Floa** sont à comparer sur ces critères. Je n'ai pas vérifié leur statut exact : il faut le consulter sur REGAFI.
- **Côté FashMatch, un rôle minimal.**
  - Afficher l'option et rediriger vers la page du prêteur, sans collecter aucune donnée financière.
  - La présenter de façon neutre : jamais présélectionnée, jamais présentée comme « sans risque ».
  - Faire valider par un juriste le statut d'intermédiaire, ou son absence.
- **Rôle RGPD.** Le prêteur est un responsable de traitement distinct, pas un sous-traitant.
  - Il n'y a donc pas de contrat art. 28.
  - Il faut en revanche informer les clients et définir par écrit les données échangées.

**Impact sur l'architecture**
- Le bloc du prestataire est relabellisé « responsable distinct ».
- Une nouvelle exigence s'ajoute : EX-20, « l'offre de paiement fractionné respecte le droit du crédit ».

---

## 5. L'hébergeur souverain

**Ce que disent les textes**
- **Le RGPD n'impose pas d'hébergeur européen.** Le transfert vers les États-Unis reste légal grâce au Data Privacy Framework, validé par le Tribunal de l'UE le 3 septembre 2025 (affaire Latombe, T-553/23). Un pourvoi est en cours devant la CJUE.
- **Le risque du CLOUD Act.** Un hébergeur soumis au droit américain peut être contraint de livrer des données, même hébergées en Europe. C'est ce risque que le choix « souverain » écarte.
- **SecNumCloud (ANSSI).** C'est la qualification la plus exigeante, qui protège notamment des lois extraterritoriales. Elle **n'est pas obligatoire** pour une start-up de e-commerce.
  - Le catalogue compte environ 12 à 13 prestataires : OVHcloud, Outscale, Cloud Temple, Numspot, S3NS, Orange Business, entre autres.
  - Le nombre exact varie selon les sources : il faut consulter le catalogue officiel de l'ANSSI.

**Notre proposition : OVHcloud, en hébergement standard en France**
- On ne prend pas d'offre SecNumCloud : le coût et la complexité ne se justifient pas pour nos données, mais on garde la possibilité d'y passer plus tard.
- Pourquoi OVHcloud :
  - entreprise française, non soumise au CLOUD Act ;
  - serveurs à processeurs graphiques disponibles pour Cabine ;
  - un service de modèles (AI Endpoints) qui propose des modèles Mistral.
- Résultat : **un seul sous-traitant pour l'hébergement, Cabine et Stella**.
- Alternative équivalente : Scaleway, hébergé à Paris, non qualifié SecNumCloud d'après les listes consultées.
- À noter : une source indique que la qualification d'Outscale expire le 30 novembre 2026. C'est à vérifier avant de le retenir.

**Impact sur l'architecture.** Aucun changement de schéma. On remplace « hébergeur souverain » par « hébergeur européen non soumis aux lois extraterritoriales » si l'équipe ne prend pas d'offre SecNumCloud, pour ne pas surpromettre.

---

## 6. Le fournisseur du modèle de langage (Stella)

**Ce que disent les sources** *(sites spécialisés, à recouper avec le contrat de sous-traitance de Mistral)*
- **Conservation par défaut.** L'API Mistral conserve les requêtes 30 jours glissants, pour surveiller les abus.
- **Conservation zéro (« ZDR »).**
  - Elle s'obtient sur demande, et Mistral l'accorde au cas par cas.
  - Elle couvre les appels de conversation simples, mais pas les produits Agents, Conversations, fichiers ou traitements par lots.
- **Localisation.** Selon une source, le traitement dans l'UE n'est pas garanti par défaut.
- **Entraînement.** Les sources ne disent pas la même chose : il faut lire le contrat de sous-traitance de Mistral.
- **Les alternatives.**
  - Scaleway documente officiellement une conservation zéro par défaut pour ses API de modèles, hébergées à Paris.
  - OVHcloud indique que les données ne sont ni stockées ni partagées. Un comparatif signale toutefois que ce réglage serait à activer : à vérifier.
  - Les deux services proposent des modèles Mistral.

**Options**
- A. API Mistral, avec la conservation zéro obtenue par écrit et un traitement dans l'UE.
- B. Un modèle Mistral servi par notre hébergeur (OVHcloud AI Endpoints, ou Scaleway).
- C. Un modèle ouvert installé sur nos propres serveurs.

**Notre proposition : B.**
- Elle respecte « aucune conservation » par défaut, garde les données en France et ne nécessite pas de sous-traitant supplémentaire.
- On passe à **A** seulement si on a besoin des plus gros modèles, avec la conservation zéro écrite dans le contrat.
- **C** se garde pour 2027 (voir point 8).
- Dans tous les cas, on garde le **masquage des données identifiantes** avant l'envoi et le filtrage des entrées et des sorties.

**Impact sur l'architecture.** Le bloc « Fournisseur LLM UE » devient « Modèle Mistral servi par l'hébergeur, conservation zéro ».

---

## 7. Les rôles AI Act (à confronter au L5 d'Enzo)

| Système | Rôle de FashMatch | Obligations principales |
|---|---|---|
| Match | Fournisseur | Risque minimal. RGPD (consentement, exclusion des catégories sensibles). |
| Cabine | Fournisseur du système **et** déployeur | Marquage lisible par machine (art. 50.2), sans délai de grâce : le système est mis en service après le 2 août 2026. Étiquetage de l'hypertrucage (art. 50.4). Adhérer au code de bonnes pratiques du 10 juin 2026. Choisir un modèle dont la licence autorise l'usage commercial (par exemple FLUX.1 schnell, sous licence Apache 2.0 ; FLUX.1 dev, lui, n'autorise pas l'usage commercial). |
| Stella | Fournisseur du système **et** déployeur ; Mistral = fournisseur du modèle à usage général | Annoncer qu'il s'agit d'une IA (art. 50.1). Les obligations du modèle (art. 53) restent chez Mistral. |
| Âge | Déployeur (le tiers est fournisseur) | Informer les personnes (art. 50.3). Point à suivre : si l'âge est considéré comme une caractéristique protégée, la catégorisation pourrait relever du haut risque (annexe III, point 1.b), avec des obligations à partir du 2 décembre 2027. |
| Paiement fractionné | Hors périmètre pour FashMatch | Le prêteur porte le haut risque (annexe III, point 5.b), à partir du 2 décembre 2027. |
| Insight | Retiré | — |

---

## 8. L'option de Mélanie pour Stella (feuille de route 2027)

**Ce que disent les textes**
- **CNIL, fiche du 19 juin 2025.** Réutiliser les futures conversations des utilisateurs d'un agent conversationnel pour améliorer le modèle peut reposer sur l'intérêt légitime, à condition de garanties fortes :
  - un droit d'opposition préalable et discrétionnaire ;
  - une information claire ;
  - une pseudonymisation dès la collecte ;
  - l'exclusion des données sensibles.
- **CEPD, avis 28/2024 (décembre 2024).** Il va dans le même sens.

**Notre proposition.** L'option est **compatible avec la feuille de route 2027, pas avec la V2**. Elle suppose :
- un modèle qu'on peut réentraîner, donc l'option C du point 6 ;
- un historique visible et supprimable par le client ;
- une opposition en un clic ;
- un filtrage des données sensibles avant l'entraînement ;
- une analyse d'impact (AIPD) avant le lancement.

---

## Calendrier utile pour la soutenance

| Date | Ce qui s'applique |
|---|---|
| 2 août 2026 | Article 50 de l'AI Act (transparence) |
| 20 novembre 2026 | Paiement fractionné = crédit à la consommation |
| 2 décembre 2026 | Fin du délai de marquage pour les systèmes mis sur le marché avant le 2 août 2026 (ne nous concerne pas) |
| Fin 2026 | Application européenne de vérification de l'âge attendue dans chaque pays |
| 2 décembre 2027 | Obligations des systèmes à haut risque (annexe III) |

---

## Sources

**AI Act et Digital Omnibus**
- [ActuIA — obligations en vigueur et reports, Omnibus 2026/1744](https://www.actuia.com/en/news/ai-act-obligations-in-force-and-delays-under-omnibus-2026-1744/) *(source secondaire)*
- [Usercentrics — accord sur l'Omnibus, article 50](https://usercentrics.com/knowledge-hub/eu-ai-act-high-risk-delay-article-50-transparency-consent/) *(source secondaire)*
- [Village de la Justice — double conformité après l'Omnibus](https://www.village-justice.com/articles/guide-pratique-double-conformite-pour-les-entreprises-apres-digital-omnibus,57912.html) *(source secondaire)*
- [regulation-ai.eu — texte de l'article 50](https://www.regulation-ai.eu/en/articles/article-50/)
- [Legalithm — article 50 et hypertrucages](https://www.legalithm.com/en/blog/ai-act-transparency-obligations-article-50-deepfake-labeling) *(source secondaire)*
- [donneespersonnelles.fr — code de bonnes pratiques, article 50](https://www.donneespersonnelles.fr/transparence-ia-article-50-ai-act) *(source secondaire)*
- [Leto — marquage des contenus IA](https://www.leto.legal/guides/code-bonne-conduite-contenu-genere-ia) *(source secondaire)*
- [Xident — estimation de l'âge et catégorisation biométrique](https://xident.io/blog/ai-act-article-50-facial-age-estimation-biometric-categorisation-2026/) *(source secondaire, fournisseur du secteur)*

**Vérification de l'âge et mineurs**
- [CEPD — déclaration 1/2025 sur la vérification de l'âge](https://www.edpb.europa.eu/news/news/2025/edpb-adopts-statement-age-assurance-creates-task-force-ai-enforcement-and-gives_en)
- [William Fry — analyse de la déclaration du CEPD](https://www.williamfry.com/knowledge/navigating-age-assurance-another-layer-insights-from-the-edpb/) *(source secondaire)*
- [Freshfields — lignes directrices DSA art. 28](https://www.freshfields.com/en/our-thinking/blogs/technology-quotient/dsa-decoded-6-the-european-commission-finalises-guidelines-on-the-protection-of-102kv4s) *(source secondaire)*
- [Hogan Lovells — lignes directrices DSA art. 28](https://hlc.com/en/publications/the-longawaited-eu-guidelines-on-article-281-dsa-what-online-platforms-must-know) *(source secondaire)*
- [aivancity — la CNIL et l'estimation de l'âge dans les bureaux de tabac](https://www.aivancity.ai/blog/estimation-de-lage-par-ia-dans-les-bureaux-de-tabac-la-cnil-sy-oppose-fermement/) *(source secondaire)*
- [Clubic — application européenne de vérification de l'âge](https://www.clubic.com/actualite-609232-verification-d-age-l-app-europeenne-techniquement-prete-la-france-dans-les-sept-premiers-pays.html) *(source secondaire)*
- [Génération NT — France Identité et double anonymat](https://www.generation-nt.com/actualites/france-identite-verification-age-double-anonymat-donnees-personnelles-2070080) *(source secondaire)*
- [Schmitt Avocats — majorité numérique à 15 ans](https://www.schmitt-avocats.fr/les-nouveaux-pouvoirs-des-agents-de-la-cnil-et-la-majorite-numerique-a-15-ans/) *(source secondaire)*
- [CNIL — hypertrucages : se protéger et signaler](https://www.cnil.fr/fr/node/168145)
- [donneespersonnelles.fr — cadre juridique des deepfakes](https://donneespersonnelles.fr/deepfakes-cadre-juridique) *(source secondaire)*

**Crédit à la consommation**
- [Légifrance — ordonnance n° 2025-1154 (coordination)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000052982995)
- [EUR-Lex — directive (UE) 2023/2225](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32023L2225)
- [Kohen Avocats — obligations des commerçants au 20 novembre 2026](https://kohenavocats.fr/2026/08/19/paiement-fractionne-credit-consommation-20-novembre-2026-obligations-commercants/) *(source secondaire, signalée comme rédigée par IA)*
- [donneespersonnelles.fr — paiement fractionné au 20 novembre 2026](https://donneespersonnelles.fr/paiement-fractionne) *(source secondaire)*
- [Herald Avocats — BNPL et responsabilités des acteurs](https://www.herald-avocats.com/bnpl-et-paiement-fractionne-conformite-produit-et-responsabilites-des-acteurs-apres-la-transposition-de-la-ccd2/) *(source secondaire)*
- [wiki.private.law — directive et BNPL, article 18](https://wiki.private.law/en/ccd2-bnpl-eu) *(source secondaire)*
- [Oney — conditions générales du 3x / 4x](https://saprdoney.blob.core.windows.net/qlf/Repository/documents/paiementfractionne/CGV%203X%204X%20Oney.pdf)

**Hébergement et modèles**
- [Hunton — Tribunal de l'UE, Data Privacy Framework](https://www.hunton.com/privacy-and-information-security-law/eus-general-court-confirms-adequacy-of-eu-u-s-data-privacy-framework) *(source secondaire)*
- [Cloud Temple — fiche Data Privacy Framework et CLOUD Act](https://www.cloud-temple.com/wp-content/uploads/2025/12/Fiche-reglementaire-Data-Privacy-Framework-Cloud-Temple.pdf) *(source secondaire, prestataire du secteur)*
- [own2pwn — prestataires qualifiés SecNumCloud](https://own2pwn.fr/articles/appsec/secnumcloud) *(source secondaire)*
- [Usine Digitale — marché SecNumCloud](https://www.usine-digitale.fr/informatique/cloud/cloud-de-confiance-le-marche-des-offres-qualifiees-secnumcloud-selargit-pousse-par-les-contraintes-reglementaires.INOZUVHVONEL7IHPME6JHEGA6A.html) *(source secondaire)*
- [developersdigest — conservation des données chez Mistral](https://www.developersdigest.tech/models/data-retention/mistral) *(source secondaire)*
- [meetily — Mistral, conservation zéro et contrat de sous-traitance](https://meetily.ai/llm-privacy/mistral) *(source secondaire)*
- [Scaleway — confidentialité des API de modèles](https://www.scaleway.com/en/docs/generative-apis/reference-content/data-privacy/)
- [OVHcloud — AI Endpoints, capacités et limites](https://docs.ovhcloud.com/fr/guides/public-cloud/ai-machine-learning/ai-endpoints-capabilities)
- [Hugging Face — FLUX.1 schnell, licence](https://huggingface.co/black-forest-labs/FLUX.1-schnell/blob/main/README.md?code=true)

**Entraînement des modèles (2027)**
- [CNIL — recommandations sur l'intérêt légitime pour développer une IA](https://cnil.fr/fr/recommandations-developpement-ia-interet-legitime)
- [CNIL — avis du CEPD sur les modèles d'IA](https://cnil.fr/fr/node/166444)

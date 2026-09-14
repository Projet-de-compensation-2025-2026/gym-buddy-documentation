# Soutenance — déroulé de 18 minutes

Le [diaporama français](Gym-Buddies-defense.pptx) contient 12 diapositives et des notes orales. Prévoir 18 minutes, garder 2 minutes de marge, puis environ 30 minutes de questions conformément au sujet.

| Temps | Partie |
| --- | --- |
| 0:00–1:30 | Besoin, périmètre et modules évalués |
| 1:30–3:30 | Architecture et rôle des quatre dépôts |
| 3:30–9:30 | Démonstration : publication, séance, conversation avec image/audio |
| 9:30–11:00 | Authentification, confidentialité et personnel |
| 11:00–14:30 | Suggestions puis appariement hebdomadaire |
| 14:30–17:00 | Tests, migration et limites |
| 17:00–18:00 | Bilan |
| 18:00–20:00 | Marge pour la navigation ou un incident réseau |

## Préparer la démonstration

Utiliser deux profils de navigateur ou deux navigateurs distincts pour les membres A et D. Deux onglets du même profil partagent le cookie de renouvellement et ne constituent pas deux sessions indépendantes. Préparer le personnel dans un profil séparé. Garder les mots de passe hors du support et du partage d’écran.

Ouvrir le [site publié](https://projet-de-compensation-2025-2026.github.io/gym-buddy-ui/), les profils, la conversation image/audio et une séance de démonstration. Vérifier le son et la connexion avant de commencer. Les captures de [version 1.2.0](screenshots/release-1.2.0/README.md) constituent le secours si le réseau devient lent.

Montrer un parcours déjà vérifié : image publiée, candidature puis acceptation, place restante, message reçu et lecture audio. Pour une séance hebdomadaire, sélectionner explicitement la bonne occurrence. Les données de démonstration sont synthétiques ; ne pas réinitialiser les fixtures du serveur.

## Questions à préparer

- Pourquoi un monolithe modulaire et un contrat OpenAPI partagé ?
- Comment empêcher un tiers de lire un média privé ? Pourquoi un lien signé reste-t-il valable 60 secondes ?
- Comment éviter deux acceptations pour la dernière place ?
- Que représentent les termes du score ? Quel coût pour les accès aux données et le tri ?
- Pourquoi un appariement glouton, avec quelle garantie et quelles limites ?
- Pourquoi les séances hebdomadaires peuvent-elles changer d’heure locale en hiver ?
- Comment prouver que la version testée est celle qui est déployée ?

Les preuves et limites exactes figurent dans la [vérification de version](../80-Testing/06-Release-verification.md). Ne pas annoncer une absence absolue de bugs ou de vulnérabilités.

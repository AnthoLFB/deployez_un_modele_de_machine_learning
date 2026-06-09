# Maintenance et Mise à jour

La pérennité d'un modèle de Machine Learning en production repose sur une surveillance constante et des mises à jour régulières pour éviter la dérive du modèle (*model drift*).

## Protocole de Mise à jour Régulière

Il est recommandé d'appliquer le protocole suivant tous les mois ou après une modification importante de la structure des effectifs.

### 1. Collecte et Intégration des Données
Les nouvelles données de vérité terrain (employés ayant quitté ou étant restés dans l'entreprise après une période donnée) doivent être insérées dans la table `training_dataset` de la base de données.

### 2. Déclenchement du Ré-entraînement
Utilisez l'endpoint `/train` avec l'optimisation activée pour garantir la meilleure configuration possible :
```bash
curl -X POST "http://votre-api/train?force=true&optimize=true"
```

### 3. Validation de la Performance
- Consultez les logs de l'application pour vérifier le **Score F1** et le **Rappel** obtenus.
- Si le Score F1 est inférieur de plus de 10% par rapport au modèle précédent, analysez la qualité des nouvelles données.

## Archivage et Versionnage du "Cerveau"

Le système de gestion des modèles (`ModelManager`) assure la sécurité des opérations :
- **Rotation automatique** : Lors d'un ré-entraînement forcé, l'ancien modèle est automatiquement déplacé vers `storage/history/` avec un suffixe temporel (ex: `model_20260609_120000.joblib`).
- **Rollback** : Pour revenir à une version précédente, il suffit de renommer le fichier souhaité dans `storage/history/` et de le replacer à la racine du dossier modèle configuré.

## Monitoring et Santé du Système

### Surveillance des Interactions
L'API historise chaque prédiction. Cette base de données d'interactions est cruciale pour :
- **Vérifier la cohérence** : Est-ce que le modèle prédit un taux de départ anormalement élevé ?
- **Audit** : Pouvoir expliquer a posteriori une prédiction spécifique.

### Alerting et Maintenance préventive
- **Logs d'erreurs** : Surveillez les erreurs de type `400` (problèmes de format de données clients) et `500` (erreurs internes).
- **Santé de la DB** : L'endpoint `/health` permet de s'assurer que la connexion à la base de données est toujours active.

## Protocole de Sécurité
- Assurez-vous que le fichier `.env` est correctement configuré et non exposé publiquement.
- Limitez l'accès aux endpoints `/train` et `/dump-brain` via une couche de sécurité réseau (VPN, filtrage IP) ou une authentification si l'API est exposée sur le web.

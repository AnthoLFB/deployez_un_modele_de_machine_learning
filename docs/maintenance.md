# Maintenance et Mise à jour

La pérennité d'un modèle de Machine Learning dépend de sa maintenance régulière.

## Protocole de Ré-entraînement

Il est recommandé de ré-entraîner le modèle périodiquement (ex: tous les mois ou après chaque ajout significatif de données de vérité terrain).

### Étapes de mise à jour :
1.  **Collecte des données** : Charger les nouvelles données d'attrition réelle dans la table `training_dataset`.
2.  **Appel à l'API** : Envoyer une requête `POST /train?optimize=true&force=true`.
3.  **Vérification** : Analyser les scores de performance (F1-score) affichés dans les logs.
4.  **Tests de non-régression** : Vérifier que les prédictions sur un jeu de test de référence restent cohérentes.

## Archivage et Versionnage

Le `ModelManager` gère automatiquement l'archivage :
*   Le modèle actif est stocké à la racine sous le nom configuré dans `.env`.
*   Chaque ré-entraînement avec `force=true` déplace l'ancien modèle vers `storage/history/` avec un timestamp.
*   En cas de dégradation des performances du nouveau modèle, il est possible de restaurer manuellement un ancien fichier `.pkl`.

## Monitoring

L'API enregistre les logs d'interaction dans la table `interaction_logs`. 
*   **Surveillance des erreurs** : Vérifier régulièrement les logs pour détecter des erreurs 400 ou 500.
*   **Analyse de dérive** : Comparer périodiquement les distributions des entrées dans `inputs` par rapport aux données d'entraînement initiales.

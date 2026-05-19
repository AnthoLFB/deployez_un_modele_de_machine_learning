# Bienvenue sur la documentation du projet : Déployez un modele de machine learning

Cette documentation couvre l'utilisation, l'architecture et la maintenance de l'API de prédiction de l'attrition des employés.

## Aperçu du projet

Le projet est conçu pour fournir une interface simple et efficace afin de prédire si un employé risque de quitter l'entreprise. Il utilise un modèle de forêt aléatoire (Random Forest) entraîné sur des données historiques de ressources humaines.

### Composants principaux

* **FastAPI** : Framework web pour l'exposition des services.
* **RandomForest (Scikit-learn)** : Modèle de Machine Learning pour la classification.
* **SQLAlchemy** : ORM pour la gestion de la base de données et l'historisation des prédictions.
* **Docker/CI-CD** : Infrastructure pour le déploiement continu.

## Structure de la documentation

* [Documentation de l'API](api.md) : Détails sur les endpoints, requêtes et réponses.
* [Modèle Technique](model.md) : Analyse du modèle, performances et architecture.
* [Maintenance & Mise à jour](maintenance.md) : Protocoles de maintenance et ré-entraînement.

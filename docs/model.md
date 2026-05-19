# Documentation Technique du Modèle

Cette section détaille les choix techniques, l'architecture de la pipeline de Machine Learning et les performances attendues.

## Architecture du Modèle

Le modèle choisi est une **Forêt Aléatoire (Random Forest)** pour sa robustesse et sa capacité à gérer des données hétérogènes (numériques et catégorielles).

### Pipeline de Prétraitement
Pour garantir la cohérence des données entre l'entraînement et l'inférence, nous utilisons une `sklearn.pipeline.Pipeline` qui inclut :

1.  **Variables Numériques** : Imputation et standardisation via `StandardScaler`.
2.  **Variables Catégorielles** : Encodage via `OneHotEncoder` (gestion des nouvelles catégories via `handle_unknown='ignore'`).
3.  **Classifieur** : `RandomForestClassifier`.

### Choix Techniques
*   **GridSearchCV** : Utilisé pour optimiser les hyperparamètres (`n_estimators`, `max_depth`, `min_samples_split`).
*   **StratifiedKFold** : Validation croisée préservant l'équilibre des classes.
*   **Scoring** : Le score F1 est privilégié pour gérer le déséquilibre potentiel des classes dans les données d'attrition.

## Performances
Les performances varient selon les données d'entraînement fournies. Le système enregistre le meilleur score obtenu lors de l'entraînement optimisé dans les logs de la console.

### Suivi des prédictions
Toutes les prédictions et les données d'entrée sont stockées dans la base de données SQLite (table `inputs` et `predictions`), permettant une analyse a posteriori de la dérive du modèle (data drift).

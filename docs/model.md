# Documentation Technique du Modèle

Cette section détaille les choix techniques, l'architecture de la pipeline de Machine Learning et les performances du modèle de prédiction d'attrition.

## Algorithme : Random Forest

Le modèle choisi est un **Random Forest Classifier**. Ce choix est justifié par plusieurs facteurs :
- **Robustesse** : Moins sensible aux valeurs aberrantes que d'autres algorithmes.
- **Gestion des non-linéarités** : Capable de capturer des relations complexes entre les variables RH (ex: corrélation entre âge, salaire et ancienneté).
- **Hétérogénéité des données** : Naturelle gestion des variables numériques et catégorielles après prétraitement.
- **Interprétabilité** : Possibilité d'extraire l'importance des caractéristiques (feature importance) pour comprendre les leviers de rétention.

## Architecture de la Pipeline

Pour garantir la reproductibilité et éviter les fuites de données (data leakage), l'ensemble du processus est encapsulé dans une `sklearn.pipeline.Pipeline`.

### 1. Prétraitement Automatique (`ColumnTransformer`)
La pipeline identifie automatiquement les types de colonnes :

- **Variables Numériques** :
    - Imputation des valeurs manquantes par la **médiane** (`SimpleImputer`).
    - Standardisation (`StandardScaler`) pour mettre toutes les variables à la même échelle.
- **Variables Catégorielles** :
    - Conversion systématique en chaînes de caractères.
    - Imputation des valeurs manquantes par une valeur constante ("nan").
    - Encodage **OneHot** (`OneHotEncoder`) avec gestion des catégories inconnues lors de l'inférence (`handle_unknown='ignore'`).

### 2. Entraînement et Optimisation
- **Optimisation** : L'API permet d'activer `GridSearchCV` pour tester différentes combinaisons d'hyperparamètres (nombre d'arbres, profondeur maximale, poids des classes).
- **Validation Croisée** : Utilisation de `StratifiedKFold` (5 splits) pour s'assurer que chaque pli est représentatif de la distribution globale des départs.
- **Équilibrage** : Le paramètre `class_weight='balanced'` est utilisé par défaut pour compenser le fait que les départs sont généralement moins fréquents que les maintiens dans l'effectif.

## Métriques de Performance

Le succès du modèle est mesuré principalement par le **Score F1**, qui représente la moyenne harmonique de la précision et du rappel. 

| Métrique | Justification |
| :--- | :--- |
| **Précision** | Éviter de cibler inutilement des employés qui ne comptent pas partir (faux positifs). |
| **Rappel** | Identifier un maximum d'employés réellement à risque (faux négatifs). |
| **Score F1** | Équilibre optimal entre précision et rappel, crucial sur des jeux de données déséquilibrés. |

## Maintenance Technique
Le modèle est sauvegardé au format binaire (`.joblib`) dans le dossier `storage/model/`. Une historisation est effectuée à chaque nouvel entraînement réussi, permettant un rollback rapide en cas de dégradation des performances.

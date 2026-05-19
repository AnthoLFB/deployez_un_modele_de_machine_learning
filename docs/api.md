# Documentation de l'API

L'API est documentée automatiquement par Swagger. Vous pouvez y accéder à `/docs` lorsque le serveur est lancé.

## Points de terminaison (Endpoints)

### 1. Santé de l'API
`GET /health`

Vérifie si l'API est opérationnelle.

**Réponse :**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. Entraînement du modèle
`POST /train`

Déclenche l'entraînement du modèle sur les données disponibles dans la base de données.

**Paramètres de requête :**
* `force` (bool, défaut: `false`) : Force le ré-entraînement même si un modèle existe.
* `optimize` (bool, défaut: `false`) : Active la recherche d'hyperparamètres (GridSearch).

**Exemple de réponse :**
```json
{
  "status": "success",
  "message": "Modèle entraîné avec succès via pipeline."
}
```

### 3. Prédiction unitaire
`POST /predict`

Prédit l'attrition pour un employé unique.

**Corps de la requête (JSON) :**
```json
{
  "age": 30,
  "revenu_mensuel": 4500,
  "departement": "R&D",
  "poste": "Chercheur",
  "nb_experiences_precedentes": 2,
  "annees_experience_totale": 8,
  "annees_dans_entreprise": 3,
  "annees_poste_actuel": 2,
  "satisfaction_environnement": 3,
  "note_evaluation_precedente": 3.5,
  "niveau_hierarchique": 2,
  "satisfaction_travail": 4,
  "satisfaction_equipe": 3,
  "satisfaction_equilibre_pro_perso": 3,
  "nombre_evaluations": 1,
  "note_evaluation_actuelle": 3.8,
  "heures_supplementaires": false,
  "augmentation_salaire_precedente": 12.0,
  "nb_participations_pee": 1,
  "nb_formations_suivies": 2,
  "code_sondage": "A1",
  "niveau_education": "Master",
  "domaine_etude": "Sciences",
  "frequence_deplacement": "Rare",
  "annees_depuis_derniere_promotion": 1,
  "annees_avec_responsable_actuel": 2,
  "tranche_distance_domicile_travail": "5-10km"
}
```

**Réponse :**
```json
{
  "prediction": true
}
```

### 4. Prédiction par lot (CSV)
`POST /predict-csv`

Envoie un fichier CSV contenant plusieurs employés pour des prédictions en masse.

### 5. Archivage
`POST /dump-brain`

Archive manuellement le modèle actuel dans le dossier `storage/history/`.

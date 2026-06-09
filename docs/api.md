# Documentation de l'API

L'API est construite avec **FastAPI** et offre une interface REST pour interagir avec le modèle de Machine Learning. La documentation interactive est disponible à l'adresse `/docs` (Swagger UI) ou `/redoc` (ReDoc) sur l'instance déployée.

## Points de terminaison (Endpoints)

### Santé et Informations
- `GET /` : Affiche un message de bienvenue et les métadonnées de l'application.
- `GET /health` : Vérifie la disponibilité de l'API et de la base de données.

**Exemple de réponse (`/health`) :**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected"
}
```

### Gestion du Modèle
- `POST /train` : Lance l'entraînement du modèle sur les données présentes en base.
    - **Query Parameters**:
        - `force` (bool) : Ré-entraîne même si un modèle existe déjà.
        - `optimize` (bool) : Active la recherche par grille (**GridSearchCV**) pour optimiser les hyperparamètres.
    - **Body (Optionnel)** : Un objet JSON définissant la `param_grid` personnalisée.

- `POST /dump-brain` : Archive le modèle actuellement en production vers le dossier de stockage historique.

### Prédictions
- `POST /predict` : Effectue une prédiction unitaire.
    - **Payload** : Nécessite l'ensemble des caractéristiques de l'employé (voir schéma ci-dessous).
    - **Réponse** : Retourne la prédiction (0 ou 1) et la probabilité associée.

**Exemple de corps de requête (`/predict`) :**
```json
{
  "revenu_mensuel": 5000.0,
  "departement": "R&D",
  "poste": "Ingénieur",
  "nombre_experiences_precedentes": 2,
  "annee_experience_totale": 10,
  "annees_dans_l_entreprise": 5,
  "annees_dans_le_poste_actuel": 3,
  "age_rh": "35",
  "satisfaction_employee_environnement": 4,
  "note_evaluation_precedente": 3.5,
  "niveau_hierarchique_poste": 2,
  "satisfaction_employee_nature_travail": 4,
  "satisfaction_employee_equipe": 4,
  "satisfaction_employee_equilibre_pro_perso": 3,
  "note_evaluation_actuelle": 4.0,
  "heure_supplementaires": "Non",
  "augementation_salaire_precedente": "5%",
  "nombre_participation_pee": 1,
  "nb_formations_suivies": 2,
  "niveau_education": "Master",
  "domaine_etude": "Informatique",
  "frequence_deplacement": "Rare",
  "annees_depuis_la_derniere_promotion": 2,
  "annes_sous_responsable_actuel": 3,
  "tranche_distance_domicile_travail": "10-20km"
}
```

- `POST /predict-csv` : Prédiction par lot via un fichier CSV.
    - Le fichier doit contenir les colonnes correspondantes au schéma de prédiction.

### Historique
- `GET /show-list` : Liste les dernières prédictions effectuées et enregistrées en base de données.
    - **Query Parameters** : `limit` (nb de résultats), `offset` (pagination).

## Codes de statut HTTP
- `200 OK` : Succès de la requête.
- `400 Bad Request` : Données d'entrée invalides ou mal formées.
- `404 Not Found` : Modèle non trouvé (nécessite un entraînement).
- `409 Conflict` : Un modèle existe déjà (utiliser `force=true`).
- `500 Internal Server Error` : Erreur inattendue du serveur.

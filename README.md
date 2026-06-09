---
title: Déployez un modele de machine learning
emoji: 🎓
colorFrom: purple
colorTo: indigo
sdk: gradio
sdk_version: 6.14.0
python_version: '3.11'
app_file: main.py
pinned: false
license: mit
short_description: Projet OC
---

# Déployez un modèle de machine learning

CI/CD

Ce projet vise à fournir une solution complète de prédiction de l'attrition des employés (départ de l'entreprise) via une API REST robuste. Il intègre un modèle de Machine Learning (Random Forest) et une infrastructure moderne pour le déploiement.

## Fonctionnalités

- **API REST (FastAPI)** : Endpoints pour l'entraînement, la prédiction (unitaire et batch CSV) et la gestion du modèle.
- **Modèle de Machine Learning** : Pipeline Scikit-learn incluant prétraitement automatique et RandomForest.
- **Persistance** : Historisation des prédictions en base de données SQL.
- **CI/CD** : Automatisation des tests et du déploiement via GitHub Actions.
- **Documentation** : Documentation interactive Swagger et documentation statique MkDocs.

## Architecture

Le projet suit une architecture modulaire :
- `app/api` : Définition des routes FastAPI.
- `app/services` : Logique métier (entraînement, prédiction, gestion du modèle).
- `app/db` : Gestion de la base de données (SQLAlchemy).
- `app/schemas` : Modèles de données Pydantic.

## Installation et Configuration

### Prérequis
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommandé) ou `pip`

### Installation locale

1. **Cloner le repository** :
   ```bash
   git clone https://github.com/votre-repo/deployez_un_modele_de_machine_learning.git
   cd deployez_un_modele_de_machine_learning
   ```

2. **Installer les dépendances** :
   ```bash
   uv sync
   # ou
   pip install -r requirements.txt
   ```

3. **Configurer l'environnement** :
   Créez un fichier `configuration/.env` (si non existant) avec les variables nécessaires (voir `configuration/.env.example`).

4. **Lancer l'application** :
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 7860 --reload
   ```

## Utilisation de l'API

### Endpoints principaux

- `GET /` : Message de bienvenue.
- `GET /health` : État de santé de l'API.
- `POST /train` : Entraîne ou ré-entraîne le modèle (possibilité d'optimisation via GridSearchCV).
- `POST /predict` : Prédit le risque de départ pour un employé (données JSON).
- `POST /predict-csv` : Prédiction en masse à partir d'un fichier CSV.
- `GET /show-list` : Historique des prédictions.

### Exemple de prédiction unitaire
```bash
curl -X 'POST' \
  'http://localhost:7860/predict' \
  -H 'Content-Type: application/json' \
  -d '{
  "revenu_mensuel": 5000.0,
  "departement": "R&D",
  "poste": "Ingénieur",
  "age_rh": "35",
  "heure_supplementaires": "Non",
  ... (autres champs)
}'
```

## Déploiement

Le projet est conçu pour être déployé sur **Hugging Face Spaces** (ou toute plateforme supportant Docker/FastAPI).

- Les fichiers de configuration CI/CD se trouvent dans `.github/workflows/`.
- Le déploiement est automatique lors d'un push sur la branche `main`.

## Documentation supplémentaire

Une documentation détaillée est disponible dans le dossier `docs/` et peut être générée avec MkDocs :
```bash
mkdocs serve
```

- [Documentation technique du modèle](docs/model.md)
- [Protocole de maintenance](docs/maintenance.md)
- [Guide de l'API](docs/api.md)
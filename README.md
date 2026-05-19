<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Projet OC | Déployez un modele de machine learning</h3>

  <p align="center">
    Une API robuste de prédiction de l'attrition des employés basée sur le Machine Learning.
    <br />
    <a href="#about-the-project"><strong>Explorer la doc »</strong></a>
    <br />
    <br />
    <a href="#getting-started">Installation</a>
    ·
    <a href="#usage">Utilisation</a>
    ·
    <a href="#api-endpoints">API Endpoints</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table des matières</summary>
  <ol>
    <li>
      <a href="#about-the-project">À propos du projet</a>
      <ul>
        <li><a href="#built-with">Technologies utilisées</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Prise en main</a>
      <ul>
        <li><a href="#prerequisites">Prérequis</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Utilisation</a></li>
    <li><a href="#api-endpoints">Points de terminaison de l'API</a></li>
    <li><a href="#deployment">Déploiement</a></li>
    <li><a href="#license">Licence</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## À propos du projet

Ce projet propose une solution complète pour prédire si un employé est susceptible de quitter l'entreprise (attrition). Il comprend une API REST construite avec FastAPI, un modèle de Machine Learning RandomForest, et une persistance des données via SQLAlchemy.

Objectifs clés :
* Prédiction en temps réel via API.
* Entraînement et optimisation automatique du modèle (GridSearchCV).
* Archivage et versionnage des modèles entraînés.
* Journalisation complète des interactions et des données d'entrée.

### Technologies utilisées

* [![FastAPI][FastAPI-badge]][FastAPI-url]
* [![Python][Python-badge]][Python-url]
* [![Scikit-Learn][Sklearn-badge]][Sklearn-url]
* [![SQLAlchemy][SQLAlchemy-badge]][SQLAlchemy-url]
* [![Pandas][Pandas-badge]][Pandas-url]

<p align="right">(<a href="#readme-top">retour en haut</a>)</p>

<!-- GETTING STARTED -->
## Prise en main

Pour faire fonctionner l'API localement, suivez ces étapes.

### Prérequis

* Python 3.9+
* pip ou uv (recommandé)

### Installation

1. Clonez le dépôt
   ```sh
   git clone https://github.com/votre-username/deployez-un-modele-de-machine-learning.git
   ```
2. Installez les dépendances
   ```sh
   pip install -r requirements.txt
   ```
3. Configurez les variables d'environnement
   Copiez `.env.exemple` vers `.env` dans le dossier `configuration/` et ajustez les paramètres si nécessaire.
   ```sh
   cp configuration/.env.exemple configuration/.env
   ```
4. Lancez l'application
   ```sh
   python main.py
   ```

<p align="right">(<a href="#readme-top">retour en haut</a>)</p>

<!-- USAGE EXAMPLES -->
## Utilisation

Une fois l'API lancée, vous pouvez accéder à la documentation interactive Swagger à l'adresse suivante :
`http://localhost:8000/docs`

### Entraîner le modèle
```bash
curl -X POST "http://localhost:8000/train?optimize=true"
```

### Faire une prédiction
```bash
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{
  "age": 35,
  "revenu_mensuel": 5000,
  "departement": "Ventes",
  ...
}'
```

<p align="right">(<a href="#readme-top">retour en haut</a>)</p>

<!-- API ENDPOINTS -->
## Points de terminaison de l'API

| Méthode | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Message de bienvenue et infos API. |
| `GET` | `/health` | État de santé de l'API. |
| `POST` | `/train` | Entraîne le modèle sur les données de la DB. |
| `POST` | `/predict` | Effectue une prédiction unitaire. |
| `POST` | `/predict-csv` | Effectue des prédictions par lot via un fichier CSV. |
| `POST` | `/dump-brain` | Archive le modèle actuel. |
| `GET` | `/show-list` | Liste l'historique des prédictions. |

<p align="right">(<a href="#readme-top">retour en haut</a>)</p>

<!-- DEPLOYMENT -->
## Déploiement

Le projet intègre des workflows GitHub Actions pour le CI/CD :
* **CI** : Tests unitaires et linting à chaque push.
* **CD** : Déploiement automatique (configuré dans `.github/workflows/cd.yml`).

<p align="right">(<a href="#readme-top">retour en haut</a>)</p>

<!-- LICENSE -->
## Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

<p align="right">(<a href="#readme-top">retour en haut</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[FastAPI-badge]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[Python-badge]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[Sklearn-badge]: https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white
[Sklearn-url]: https://scikit-learn.org/
[SQLAlchemy-badge]: https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white
[SQLAlchemy-url]: https://www.sqlalchemy.org/
[Pandas-badge]: https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/
## Installation de la Base de Données

Un script d'automatisation est fourni pour créer les utilisateurs, les bases de données et les tables nécessaires.

### Prérequis
- PostgreSQL installé et en cours d'exécution.
- Python avec `psycopg2-binary` et `python-dotenv` (inclus dans `requirements.txt`).
- Le fichier `configuration/.env` doit être correctement renseigné.

### Utilisation
Pour initialiser ou mettre à jour la base de données, exécutez la commande suivante à la racine du projet :

```bash
python setup_db.py
```

**Note :** Par défaut, le script tente de se connecter à Postgres en utilisant les variables d'environnement `PGUSER` et `PGPASSWORD` (souvent `postgres`). Assurez-vous d'avoir les droits suffisants (rôle `SUPERUSER`) pour créer de nouveaux rôles et bases de données.

Si vous devez spécifier manuellement l'utilisateur administrateur pour le script :
- Sur Windows (PowerShell) :
  ```powershell
  $env:PGUSER="votre_admin"; $env:PGPASSWORD="votre_password"; python setup_db.py
  ```
- Sur Linux/macOS :
  ```bash
  PGUSER=votre_admin PGPASSWORD=votre_password python setup_db.py
  ```

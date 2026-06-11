# Configuration de l'environnement et de la Base de Données

Ce projet utilise un fichier `.env` pour gérer les variables d'environnement, notamment les identifiants de connexion à la base de données. Il est impératif de configurer ce fichier avant de lancer l'application.

## Utilisation du fichier `.env`

Un exemple est disponible dans le fichier `configuration/.env.example`. Vous devez le copier et le renommer en `configuration/.env` (ou à la racine du projet, selon la configuration du chargeur de variables) et remplir les champs nécessaires.

### Connexion à la Base de Données

Les variables suivantes sont requises pour établir la connexion à la base de données (PostgreSQL) :

* `POSTGRES_SA_NAME` : Nom d'utilisateur super-admin (pour la création des bases).
* `POSTGRES_SA_PWD` : Mot de passe du super-admin.
* `DB_PRODUCTION_HOST` / `DB_PRODUCTION_PORT` / `DB_PRODUCTION_NAME` / `DB_PRODUCTION_USER` / `DB_PRODUCTION_PWD` : Identifiants de connexion pour la base de données de production.
* `DB_STAGING_HOST` / `DB_STAGING_PORT` / `DB_STAGING_NAME` / `DB_STAGING_USER` / `DB_STAGING_PWD` : Identifiants de connexion pour la base de données de staging/développement.

**Attention : Ne jamais commiter le fichier `.env` réel contenant des secrets dans le repository Git.**

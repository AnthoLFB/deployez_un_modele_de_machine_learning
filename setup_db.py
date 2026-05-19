import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Charger les variables d'environnement depuis configuration/.env
dotenv_path = os.path.join('configuration', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print(f"Chargement du .env depuis {dotenv_path}")
else:
    print(f"Attention: {dotenv_path} non trouvé. Utilisation des variables d'environnement système.")

# Récupération des configurations
# On suppose que l'utilisateur qui exécute ce script a les droits nécessaires sur Postgres (souvent l'utilisateur 'postgres')
PG_HOST = os.getenv('DB_PRODUCTION_HOST', 'localhost')
PG_PORT = os.getenv('DB_PRODUCTION_PORT', '5432')
PG_USER = os.getenv('PGUSER', 'postgres')  # Utilisateur système pour la création initiale
PG_PWD = os.getenv('PGPASSWORD', '')

# Si PGUSER n'est pas défini, on essaie de demander à l'utilisateur ou d'utiliser 'postgres'
# Pour le bien de l'automatisation sans interaction, on va d'abord tenter avec 'postgres' sans mot de passe
# ou utiliser les variables d'environnement standards si elles existent.

# Utilisateurs et Bases du .env
SA_NAME = os.getenv('POSTGRES_SA_NAME')
SA_PWD = os.getenv('POSTGRES_SA_PWD')

DB_PROD_NAME = os.getenv('DB_PRODUCTION_NAME')
DB_PROD_USER = os.getenv('DB_PRODUCTION_USER')
DB_PROD_PWD = os.getenv('DB_PRODUCTION_PWD')

DB_STAGING_NAME = os.getenv('DB_STAGING_NAME')
DB_STAGING_USER = os.getenv('DB_STAGING_USER')
DB_STAGING_PWD = os.getenv('DB_STAGING_PWD')

def connect_db(dbname='postgres', user=PG_USER, password=PG_PWD, host=PG_HOST, port=PG_PORT):
    return psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

def create_role_if_not_exists(cursor, role_name, password, is_superuser=False):
    cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (role_name,))
    if not cursor.fetchone():
        print(f"Création du rôle {role_name}...")
        options = "SUPERUSER CREATEDB CREATEROLE" if is_superuser else ""
        query = f"CREATE ROLE {sql.Identifier(role_name).as_string(cursor)} WITH LOGIN PASSWORD %s {options}"
        cursor.execute(query, (password,))
    else:
        print(f"Le rôle {role_name} existe déjà.")

def create_db_if_not_exists(cursor, db_name, owner):
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
    if not cursor.fetchone():
        print(f"Création de la base de données {db_name}...")
        # CREATE DATABASE ne peut pas être exécuté dans une transaction ou avec des paramètres liés pour le nom
        cursor.execute(sql.SQL("CREATE DATABASE {} OWNER {}").format(
            sql.Identifier(db_name),
            sql.Identifier(owner)
        ))
    else:
        print(f"La base de données {db_name} existe déjà.")

def execute_sql_file(cursor, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
            if sql_content.strip():
                cursor.execute(sql_content)
                return True
    return False

def setup():
    print("--- Démarrage de la configuration de la base de données ---")
    
    # 1. Connexion initiale pour créer rôles et bases
    conn = connect_db()
    conn.autocommit = True
    cur = conn.cursor()

    try:
        # Création des rôles
        if SA_NAME: create_role_if_not_exists(cur, SA_NAME, SA_PWD, is_superuser=True)
        if DB_PROD_USER: create_role_if_not_exists(cur, DB_PROD_USER, DB_PROD_PWD)
        if DB_STAGING_USER: create_role_if_not_exists(cur, DB_STAGING_USER, DB_STAGING_PWD)

        # Création des bases
        if DB_PROD_NAME: create_db_if_not_exists(cur, DB_PROD_NAME, DB_PROD_USER)
        if DB_STAGING_NAME: create_db_if_not_exists(cur, DB_STAGING_NAME, DB_STAGING_USER)

    except Exception as e:
        print(f"Erreur lors de la création initiale : {e}")
        return
    finally:
        cur.close()
        conn.close()

    # 2. Création des tables et configuration des privilèges pour chaque base
    for db_name, db_user, priv_file in [
        (DB_PROD_NAME, DB_PROD_USER, 'ajout_privileges_production.txt'),
        (DB_STAGING_NAME, DB_STAGING_USER, 'ajout_privileges_staging.txt')
    ]:
        if not db_name: continue
        
        print(f"\nConfiguration de la base {db_name}...")
        try:
            # On se connecte en tant que superadmin pour être sûr d'avoir tous les droits
            conn = connect_db(dbname=db_name) 
            conn.autocommit = True
            cur = conn.cursor()

            # Création des tables
            table_files = ['inputs.txt', 'predictions.txt', 'interaction_logs.txt', 'training_dataset.txt']
            for tf in table_files:
                path = os.path.join('Requête SQL', 'tables', tf)
                print(f"  Exécution de {tf}...")
                # On enveloppe dans un TRY/EXCEPT pour gérer le cas où la table existe déjà
                try:
                    execute_sql_file(cur, path)
                except psycopg2.errors.DuplicateTable:
                    print(f"    La table définie dans {tf} existe déjà.")
                except Exception as e:
                    print(f"    Erreur dans {tf}: {e}")

            # Insertion des données (uniquement si training_dataset est vide)
            cur.execute("SELECT COUNT(*) FROM training_dataset")
            if cur.fetchone()[0] == 0:
                print("  Insertion des données initiales dans training_dataset...")
                execute_sql_file(cur, os.path.join('Requête SQL', 'tables', 'insertion_training_dataset.txt'))
            else:
                print("  La table training_dataset contient déjà des données.")

            # Privilèges
            priv_path = os.path.join('Requête SQL', 'databases', priv_file)
            print(f"  Configuration des privilèges depuis {priv_file}...")
            execute_sql_file(cur, priv_path)

            cur.close()
            conn.close()
            print(f"Base {db_name} configurée avec succès.")

        except Exception as e:
            print(f"Erreur lors de la configuration de {db_name} : {e}")

    # 3. Test de connexion SuperAdmin
    print("\n--- Test de vérification des accès SuperAdmin ---")
    try:
        sa_conn = connect_db(dbname=DB_PROD_NAME, user=SA_NAME, password=SA_PWD)
        print(f"Connexion réussie à {DB_PROD_NAME} avec l'utilisateur SuperAdmin {SA_NAME}")
        sa_conn.close()
        
        sa_conn_staging = connect_db(dbname=DB_STAGING_NAME, user=SA_NAME, password=SA_PWD)
        print(f"Connexion réussie à {DB_STAGING_NAME} avec l'utilisateur SuperAdmin {SA_NAME}")
        sa_conn_staging.close()
        
        print("Vérification des accès : OK")
    except Exception as e:
        print(f"Échec du test de connexion SuperAdmin : {e}")

if __name__ == "__main__":
    setup()

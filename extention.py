import oracledb # Ou votre connecteur Oracle/PostgreSQL
import random
from faker import Faker
from datetime import datetime

fake = Faker(['fr_FR'])

# --- CONFIGURATION ---
NB_TENRACS = 10 # Ajustez pour atteindre le million total cumulé
NB_REPAS = 10
NB_MACHINES = 10

def generate_data():
    # Listes de constantes pour la cohérence métier
    grades = [
        ('Affilié', 1), ('Sympathisant', 2), ('Adhérent', 3), 
        ('Chevalier', 4), ('Grand Chevalier', 5), ('Commandeur', 6), ('Grand\'Croix', 7)
    ]
    rangs = [('Novice', 1), ('Compagnon', 2)]
    titres = [('Philanthrope', 1), ('Protecteur', 2), ('Honorable', 3)]
    dignites = [('Maître', 1), ('Grand Chancelier', 2), ('Grand Maître', 3)]
    
    modeles = [('Traditionnel', 'Moderne'), ('Combiné 5-en-1', 'Contemporain'), ('Bas de gamme', 'Vintage')]
    types_entretien = [('Nettoyage Résistance', '6'), ('Vérification Électrique', '12'), ('Décapage', '3')]

    print("Début de la génération...")

    # 1. Tables de Référence (Petites)
    # On génère ici les Grades, Rangs, etc.
    
    # 2. Organismes et Territoires
    territoires = [(i, fake.region()) for i in range(1, 101)]
    organismes = [(fake.siret(), fake.company()) for _ in range(500)]
    adresses = [(i, fake.address().replace('\n', ' ')) for i in range(1, 5000)]

    # 3. Organisations (Ordre et Clubs)
    # idO 1 est l'Ordre, les autres sont des Clubs
    organisations = [(1, "L'Ordre Suprême du Tenrac", "Ordre", random.randint(1, 100))]
    for i in range(2, 201):
        organisations.append((i, f"Club Tenrac {fake.city()}", "Club", random.randint(1, 100)))

    # 4. Tenracs (Le gros volume)
    tenracs = []
    chevaliers_ids = [] # Utile pour les repas
    maitres_ids = []    # Utile pour l'entretien
    
    for i in range(1, NB_TENRACS + 1):
        grade = random.choice(grades)[0]
        dignite = random.choice(dignites)[0] if random.random() > 0.8 else None
        
        # Logique métier : code personnel RFID
        siret = random.choice(organismes)[0]
        idO = random.randint(1, 200)
        code_rfid = f"{fake.ean8()}-{idO}-{siret[:5]}"

        tenracs.append((
            i, fake.name(), fake.email(), fake.phone_number(), 
            fake.street_address(), code_rfid, dignite,
            random.choice(rangs)[0] if random.random() > 0.5 else None,
            grade,
            random.choice(titres)[0] if random.random() > 0.7 else None,
            siret, idO
        ))
        
        if grade in ['Chevalier', 'Grand Chevalier']:
            chevaliers_ids.append(i)
        if dignite == 'Maître':
            maitres_ids.append(i)

    # 5. Repas
    repas = []
    for i in range(1, NB_REPAS + 1):
        repas.append((
            f"R-{i}", f"Festin {fake.word()}", 
            fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),
            random.randint(1, 4999)
        ))

    # 6. Machines et Entretiens
    machines = [(i, f"Machine-{fake.word()}-{i}") for i in range(1, NB_MACHINES + 1)]
    
    historique_entretiens = []
    for _ in range(NB_MACHINES * 2):
        historique_entretiens.append((
            random.randint(1, NB_MACHINES),
            random.randint(1, 200),
            fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),
            random.choice(maitres_ids) if maitres_ids else 1
        ))

    print(f"Génération terminée : {NB_TENRACS} Tenracs créés.")
    
    # --- INSERTION OU EXPORT ---
    # Ici vous pouvez utiliser cursor.executemany() pour insérer dans votre DB
    # Ou écrire dans un fichier .sql
    with oracledb.connect(user="SYSTEM", password="02022007", host="127.0.0.1") as connection:
        drop_tables(connection)
        insert_tenrac(tenracs, connection)
        insert_territoire(territoires, connection)
        connection.commit()

def drop_tables(connection):

    intention = open("intention.sql", "r")
    intentionSQL = intention.read()
    intentionSQL = intentionSQL.split(";")

    with connection.cursor() as cursor:
            cursor.execute("drop table GRADE cascade constraints")
            cursor.execute("drop table RANG cascade constraints")
            cursor.execute("drop table TITRE cascade constraints")
            cursor.execute("drop table DIGNITE cascade constraints")
            cursor.execute("drop table ORGANISME_ASSOCIE cascade constraints")
            cursor.execute("drop table PLAT cascade constraints")
            cursor.execute("drop table INGREDIENT cascade constraints")
            cursor.execute("drop table SAUCE cascade constraints")
            cursor.execute("drop table MACHINE cascade constraints")
            cursor.execute("drop table TERRITOIRE cascade constraints")
            cursor.execute("drop table MODELE cascade constraints")
            cursor.execute("drop table ENTRETIEN cascade constraints")
            cursor.execute("drop table ADRESSE cascade constraints")
            cursor.execute("drop table REPAS cascade constraints")
            cursor.execute("drop table ORGANISATION cascade constraints")
            cursor.execute("drop table TENRAC cascade constraints")
            cursor.execute("drop table ORDRE_DES_TENRACS cascade constraints")
            cursor.execute("drop table CLUB_TENRAC cascade constraints")
            cursor.execute("drop table EST_CREATEUR cascade constraints")
            cursor.execute("drop table PARTICIPE cascade constraints")
            cursor.execute("drop table COMBINEIS cascade constraints")
            cursor.execute("drop table CONTIENT cascade constraints")
            cursor.execute("drop table EST_ASSOCIE cascade constraints")
            cursor.execute("drop table UTILISE cascade constraints")
            cursor.execute("drop table ASSOCIE cascade constraints")
            cursor.execute("drop table HISTORIQUE_ENTRETIEN cascade constraints")
            cursor.execute("drop table COMBINESP cascade constraints")
            cursor.execute("drop table COMBINEIP cascade constraints")
            cursor.execute("drop table ADRESSE_PARTENAIRE cascade constraints")
            for table in intentionSQL[0:len(intentionSQL)-1]:
                cursor.execute(table)
    print("Drop all tables succeed")

def insert_tenrac(data, connection):
    for tenrac in data:
        with connection.cursor() as cursor:
            cursor.execute("insert into TENRAC values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12)", 
                        (tenrac[0], tenrac[1], tenrac[2], tenrac[3], tenrac[4], tenrac[5], None, None, None,
                        None, None, None))
    print("Finished Tenrac")

def insert_territoire(data, connection):
    for territoire in data:
        with connection.cursor() as cursor:
            cursor.execute("insert into TERRITOIRE values (:1, :2)", 
                        (territoire[0], territoire[1]))
    print("Finished Territoire")

if __name__ == "__main__":
    generate_data()
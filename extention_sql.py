import random
from faker import Faker
from datetime import datetime
from time import time

fake = Faker(['fr_FR'])

HOST = "127.0.0.1"
PASSWORD = "02022007"

# --- CONFIGURATION ---
NB_TENRACS = 100_000 # Ajustez pour atteindre le million total cumulé
NB_REPAS = 10
NB_MACHINES = 10

def generate_data():
    # Listes de constantes pour la cohérence métier
    grades = [
        ('Affilié', 1), ('Sympathisant', 2), ('Adhérent', 3), 
        ('Chevalier', 4), ('Grand Chevalier', 5), ('Commandeur', 6), ('Grand Croix', 7)
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
    organisations = [(1, "L Ordre Supreme du Tenrac", "Ordre", random.randint(1, 100))]
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
            fake.street_address(),
            None,
            dignite,
            random.choice(rangs)[0] if random.random() > 0.5 else None,
            grade,
            random.choice(titres)[0] if random.random() > 0.3 else None,
            siret,
            random.choice(organisations)[0] if random.random() > 0.8 else None
        ))
        
        if grade in ['Chevalier', 'Grand Chevalier']:
            chevaliers_ids.append(i)
        if dignite == 'Maître':
            maitres_ids.append(i)

    # 5. Repas
    repas = []
    for i in range(1, NB_REPAS + 1):
        repas.append((
            i,
            f"R-{i}, Festin {fake.word().replace(',', '')}", 
            fake.date_time_between(start_date='-2y', end_date='now'),
            random.choice(adresses)[0]
        ))

    # 6. Machines et Entretiens
    machines = [(i, f"Machine-{fake.word()}-{i}") for i in range(1, NB_MACHINES + 1)]
    
    historique_entretiens = []
    for _ in range(NB_MACHINES * 2):
        historique_entretiens.append((
            random.choice(machines)[0],
            random.choice(organisations)[0],
            fake.date_time_between(start_date='-1y', end_date='now'),
            random.choice(maitres_ids) if maitres_ids else 1
        ))

    print(f"Génération terminée : {NB_TENRACS} Tenracs créés.")
    


    insert(territoires, "Territoire", "insert into Territoire values (:1, :2)")
    insert(organismes, "Organisme Associe", "insert into Organisme_associe values (:1, :2)")
    insert(adresses, "Adresse", "insert into Adresse values (:1, :2)")
    insert(organisations, "Organisation", "insert into Organisation values (:1, :2, :3, :4)")
    insert(dignites, "Dignite", "insert into Dignite values (:1, :2)")
    insert(rangs, "Rang", "insert into Rang values (:1, :2)")
    insert(grades, "Grade", "insert into Grade values (:1, :2)")
    insert(titres, "Titre", "insert into Titre values (:1, :2)")
    insert(tenracs, "Tenracs", "insert into Tenrac values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12)")
    insert(repas, "Repas", "insert into Repas values (:1, :2, :3, :4)")
    insert(machines,"Machine", "insert into Machine values (:1, :2)")
    insert(historique_entretiens, "Historique Entretien", "insert into Historique_Entretien values (:1, :2, :3, :4)")
    insert(modeles, "Modele", "insert into Modele values (:1, :2)")
    #insert(ingredients, connection, "Ingredient", "insert into Ingredient values (:1, :2)")
    #insert(sauces, connection, "Sauce", "insert into Sauce values (:1, :2)")
    #insert(plats, connection, "Plat", "insert into Plat values (:1, :2, :3)")
    #insert(est_associe, connection, "Est_Associe", "insert into Est_Associe values (:1, :2)")
    #insert(utilise, connection, "Utilise", "insert into Utilise values (:1, :2)")
    #insert(associe, connection, "Associe", "insert into Associe values (:1, :2)")
    #insert(est_createur, connection, "Est_Createur", "insert into Est_Createur values (:1, :2)")
    #insert(participe, connection, "Participe", "insert into Participe values (:1, :2)")
    #insert(combineis, connection, "CombineIS", "insert into CombineIS values (:1, :2)")
    #insert(combinesp, connection, "CombineSP", "insert into CombineSP values (:1, :2)")
    #insert(combineip, connection, "CombineIP", "insert into CombineIP values (:1, :2)")
    #insert(adresse_partenaire, connection, "Adresse_Partenaire", "insert into Adresse_Partenaire values (:1, :2)")

def insert(data, table, sql):
    insert = sql.split('(')[0]
    result = ""
    for element in data:
        result+=insert + '('
        for i in range(len(element)):
            if isinstance(element[i], str) or isinstance(element[i], datetime):
                result += "'"+ element[i].__str__() + "'"
            else:
                result += str(element[i])
            if i != len(element)-1:
                result+=", "
        result+=')\n'
    file = open("data/" + table + ".sql", "a+")
    file.write(result)
    print("Finished", table)

if __name__ == "__main__":
    NB_TENRACS = eval(input("Combien de Tenrac: "))
    a = time()
    generate_data()
    print("Generation made in", round(time()-a), "secondes")
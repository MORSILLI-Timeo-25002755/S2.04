import pandas as pd
import matplotlib.pyplot as plt

couleurs = plt.cm.Set3.colors

grades = pd.read_csv("csv/Grade.csv", header=None).rename(columns={0: "nom_grade"})
tenracs = pd.read_csv("csv/Tenracs.csv", header=None).rename(columns={8: "nom_grade"})

tenracs_grades = tenracs.merge(grades, on="nom_grade").groupby("nom_grade")

values = tenracs_grades.size() / len(tenracs)

plt.pie(values, 
        labels=grades["nom_grade"], 
        colors=couleurs,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.80,
        textprops={'fontsize': 11, 'weight': 'bold', 'color': '#333333'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 2})

plt.title("Répartition des Tenracs par Grade", fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.show()
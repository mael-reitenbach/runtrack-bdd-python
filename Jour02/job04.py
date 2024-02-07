import mariadb

plateforme_database = mariadb.connect(
    host="localhost",
    user="root",
    password="MaelRTB12!!"
)

cur = plateforme_database.cursor()
cur.execute("USE Laplateforme;")
cur.execute("SELECT nom, capacite FROM salle;")
liste_salles = []
for row in cur:
    liste_salles.append(row)
print(liste_salles)
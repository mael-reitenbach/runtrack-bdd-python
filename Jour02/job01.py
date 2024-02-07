import mariadb

plateforme_database = mariadb.connect(
    host="localhost",
    user="root",
    password="MaelRTB12!"
)

cur = plateforme_database.cursor()
cur.execute("USE Laplateforme;")
cur.execute("SELECT * FROM etudiant;")
for row in cur:
    print(row)
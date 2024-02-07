import mariadb

plateforme_database = mariadb.connect(
    host="localhost",
    user="root",
    password="MaelRTB12!"
)

cur = plateforme_database.cursor()
cur.execute("USE Laplateforme;")

cur.execute("SELECT AVG(superficie) FROM etage;")
print(f"La superficie de La Plateforme est de {int(cur.fetchone()[0])} m2")
import mariadb

plateforme_database = mariadb.connect(
    host="localhost",
    user="root",
    password="MaelRTB12!"
)

cur = plateforme_database.cursor()
cur.execute("USE Laplateforme;")

cur.execute("SELECT SUM(capacite) FROM salle;")
print(f"La capacité de toutes les salles est de : {(cur.fetchone()[0])}")
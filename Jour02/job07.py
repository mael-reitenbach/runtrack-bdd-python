import mariadb
import pandas

plateforme_database = mariadb.connect(
    host="localhost",
    user="root",
    password="MaelRTB12!"
)

cur = plateforme_database.cursor()
cur.execute("USE entreprise;")

class Database:
    def __init__(self):
        self.__host = "localhost"
        self.__user = "root"
        with open("password.txt", "r") as passwordtxt:
            self.__pw = passwordtxt.read()
            self.__database = "Entreprise"
        self.__connect()

    def __connect(self):
        self.database = mariadb.connect(
            host=self.__host,
            user=self.__user,
            password=self.__pw,
            autocommit=False,
            database=self.__database
        )
        return self.database

    def request(self, request, updates=False):
        database = self.__connect()
        cursor = database.cursor()
        cursor.execute(request)
        database.commit()
        if not updates:
            sel = cursor.fetchall()
            return sel
        cursor.close()
        database.close()


class Entreprise(Database):
    def __init__(self):
        super().__init__()

    def create_service(self, name):
        self.request(f"INSERT INTO service (nom) VALUES (\'{name}\')", updates=True)

    def get_services(self):
        result = self.request("SELECT * FROM service")
        organized = pandas.DataFrame(result, columns=["ID", "Name"])
        print(organized)

    def update_service(self, id, name):
        self.request(f"UPDATE service SET name = \'{name}\' WHERE id = {id}", updates=True)

    def remove_service(self, id):
        self.request(f"DELETE FROM employe WHERE id = {id}", updates=True)

    def create_employee(self, **kwargs):
        self.request(f"INSERT INTO employe (nom, prenom, salaire, id_service) VALUES (\'{kwargs['lastname']}\', \'{kwargs['name']}\', "
                     f"\'{kwargs['salary']}\', \'{kwargs['service_id']}\')", updates=True)

    def get_employees(self):
        result = self.request("SELECT * FROM employe")
        organized = pandas.DataFrame(result, columns=["ID", "Name", "Lastname", "Salary", "ID Service"])
        print(organized)

    def update_employee(self, id, **kwargs):
        values_to_update = ""
        for key, value in kwargs.items():
            values_to_update += f"{key} = \'{value}\', "
        values_to_update = values_to_update[:-2]
        self.request(f"UPDATE employe SET {values_to_update} WHERE id = {id}", updates=True)

    def remove_employee(self, id):
        self.request(f"DELETE FROM employe WHERE id = {id}", updates=True)


if __name__ == '__main__':
    entreprise = Entreprise()
    entreprise.create_employee(lastname="Luca", name="Dorso", salary=6603, service_id=3)
    entreprise.get_services()
    entreprise.get_employees()
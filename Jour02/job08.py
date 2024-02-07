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
            self.__database = "zoo"
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


class Zoo(Database):
    def __init__(self):
        super().__init__()

    def create_animal(self, name, born, race, cage, origin):
        #DATE in SQL is in the YYYY-MM-DD format
        if not self.check_full_cage(cage):
            self.request(f"INSERT INTO animaux (nom, race, date_naissance, pays_origine, cage_id) VALUES (\'{name}\', \'{race}\', \'{born}\', \'{origin}\', {cage})", updates=True)

    def get_animals(self):
        result = self.request("SELECT * FROM animaux")
        organized = pandas.DataFrame(result, columns=["ID", "Name", "Race", "Date of birth", "Country of origin", "In cage:"])
        print(organized)

    def update_animal(self, id, **kwargs):
        values_to_update = ""
        for key, value in kwargs.items():
            values_to_update += f"{key} = \'{value}\', "
        values_to_update = values_to_update[:-2]
        self.request(f"UPDATE animaux SET {values_to_update} WHERE id = {id}", updates=True)

    def remove_animal(self, id):
        self.request(f"DELETE FORM animaux WHERE id = {id}", updates=True)

    def create_cage(self, max_capacity, superficie):
        self.request(f'INSERT INTO cage (nb_animaux, superficie, max_capacite) VALUES (0, {max_capacity}, {superficie});', updates=True)

    def get_cages(self):
        result = self.request("SELECT * FROM cage")
        organized = pandas.DataFrame(result, columns=["ID", "Number of animals", "Max Capacity", "Superficie"])
        print(organized)

    def remove_cage(self, id):
        self.request(f"DELETE FROM cage WHERE id = {id}", updates=True)

    def check_full_cage(self, id):
        number = self.request(f"SELECT nb_animaux FROM cage WHERE id = {id}")[0][0]
        if number+1 > self.request(f"SELECT max_capacite FROM cage WHERE id = {id}")[0][0]:
            return True
        return False

    def update_cage_animals(self, id):
        if not self.check_full_cage(id):
            self.request(f"UPDATE cage SET nb_animaux = (SELECT COUNT(*) FROM animaux WHERE cage_id = {id}) WHERE id = {id}", updates=True)

    def total_surface(self):
        return self.request('SELECT SUM(superficie) FROM cage')[0][0]

    def join_animals_cages(self):
        return pandas.DataFrame(self.request('SELECT animaux.*, cage.max_capacite, cage.nb_animaux, cage.superficie FROM animaux INNER JOIN cage ON animaux.cage_id = cage.id'), columns=["ID", "Name", "Race", "DoB", "Country", "In cage:", "Max Cap.", "Nb Animals", "Surface"])


if __name__ == '__main__':
    pandas.set_option('display.max_columns', None)
    zoo = Zoo()
    running = True
    while running:
        zoo.get_cages()
        zoo.get_animals()
        request = int(input('1 - Add an animal\n2 - Remove an animal\n3 - Modify an animal\n4 - Caculate total cages surface\n'))
        if request == 1:
            cage_id = int(input("In which cage ?: "))
            if not zoo.check_full_cage(cage_id):
                zoo.create_animal(input("Name ?: "), input("Date of birth ? (YYYY-MM-DD): "), input("Race ?: "), cage_id, input("From which country ?: "))
            else:
                print("Cage is full already !")
            zoo.update_cage_animals(cage_id)
        elif request == 2:
            zoo.remove_animal(int(input("Which animal to remove ? (id): ")))
        elif request == 3:
            zoo.update_animal(int(input("Animal's ID: ")), nom=input("Animal's new name: "),
                                  race=input("Animal's race: "), date_naissance=input("Animal's date of birth: "),
                                  pays_origine=input("Animal's origin: "), cage_id=int(input("Animal's cage's id: ")))
        elif request == 4:
            print(f"Total surface in dam²: {zoo.total_surface()}")
        print("\n\n")
        print(zoo.join_animals_cages())
        running = False if input("Quit ? y/n").lower() == "y" else True
# importation du module necessaires
import sqlite3

class database:
    # https://docs.python.org/3/library/sqlite3.html
    def __init__(self, base):
        """
        méthode constructrice de la classe
        parametres:
                   base,une chaine de caracteres avec le chemin d'accès à la base de données
        """
        self.base = ""

    def test_connexion(self):
        """
        méthode permettant de savoir si la base de données peut-être connectées
        renvoie un booléen
        """
        try:
            conn = sqlite3.connect(self.base)
        except:
            return False

        conn.close()
        return True

    def connexion(self):
        """
        méthode permettant de se connecter à la base de donnée
        """
        self.con = sqlite3.connect(self.base)
        self.cur = self.con.cursor()

    def deconnexion(self):
        """
        méthode permettant de se deconnecter à la base de donnée
        """
        self.con.close()

    def execute(self,sql):
        """
        méthode permettant d'obtenir le résultat d'une requête sql
        parametres:
                   sql, une chaine de caracteres correspondant à une requete SQL
        renvoie le résultat de la requete dans la base
        """
        self.connexion()
        result = self.cur.execute(sql).fetchall()
        self.deconnexion()
        return result

    def contenue_table(self, table):
        return self.execute("SELECT * FROM " + table)

    def infotable(self, table):
        """
        méthode permettant de connaitre les informations d'une table
        parametres:
                   table, une chaine de caracteres contenant le nom de la table
        renvoie les informations de la table
        """
        return self.execute("DESCRIBE " + table)
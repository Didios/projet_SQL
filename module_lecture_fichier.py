import os
import os.path
import module_database as Database

def fichier_existe(path):
    """
    fonction permettant de connaitre l'existence d'un répertoire ou d'un fichier
    parametres:
               path, le chemin vers le répertoire souhaité sous forme de chaine de caracteres
    renvoie un booléen, True si le répertoire/fichier existe et False sinon
    """
    if "." in path and os.path.isfile(path):
        return True
    elif os.path.isdir(path):
        return True
    else:
        return False

def lire_fichier(file):
    """
    fonction qui lit un fichier choisit
    parametres:
               file, une chaine de caracteres contenant le chemin vers le fichier à lire
    renvoie une liste de chaine de caracteres, chaque élément est une ligne du fichier
    """
    if fichier_existe(file):
        f = open(file)
        f = [x.rstrip("\n") for x in f.readlines()]

        l = 0
        while l < len(f): # On enlève les sauts de ligne et les retours à la ligne
            if f[l] == "":
                f = f[:l] + f[l+1:]
            l += 1
        return f

def execute_sql_file(path, file, db):
    """
    fonction permettant d'exécuter une requete sql dans une base de données, ici, on lit le fichier puis on l'éxécute
    parametres:
               path, une chaine de caracteres contenant le chemin d'accès au fichier avec le fichier sql
               file, une chaine de caracteres contenant le nom du fichier à exécuter
               db, une chaine de caracteres avec le chemin entier vers la base de données dans laquelle exécuter la requete
    renvoie les résultats de la requetes sous forme de liste
    """
    base = Database.database(db)
    sql_liste = lire_fichier(path + "/" + file)
    sql = ""

    for i in range(len(sql_liste) -1):
        sql += sql_liste[i] + " "
    sql += sql_liste[-1]

    result = base.execute(sql)
    return result
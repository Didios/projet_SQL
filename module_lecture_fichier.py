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
        f = [x.rstrip("\n") for x in f.readlines()] # On enlève les sauts de ligne et les retours à la ligne

        l = 0
        while l < len(f): # On enlève les lignes vides
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
    sql_liste = lire_fichier(path + "/" + file)
    sql = ""

    for i in range(len(sql_liste)): # On établit la requête sql dans une seule ligne/chaine de caractères
        sql += sql_liste[i] + " "

    try: # Résolution du probleme "sqlite3.OperationalError: no such table:"
        base = Database.database(db)
        result = base.execute(sql)
    except:
        import sqlite3
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        result = cur.execute(sql).fetchall()
        conn.close()

    return result

    return result
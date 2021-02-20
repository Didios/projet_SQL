# importation des modules necessaire
import os
import os.path

# l'importation de ce module change selon l'utilisation du fichier (directe ou non)
try:
    import module_database as Database
except:
    from modules import module_database as Database

def fichier_existe(path):
    """
    fonction permettant de connaitre l'existence d'un répertoire ou d'un fichier
    parametres:
               path, le chemin vers le répertoire souhaité sous forme de chaine de caracteres
    renvoie un booléen, True si le répertoire/fichier existe et False sinon
    """
    if "." in path and os.path.isfile(path): # On dit que s'il y a un point dans le chemin, alors c'est un fichier que l'on recherche
        return True
    elif os.path.isdir(path): # sinon c'est un repertoire
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
    if fichier_existe(file): # on vérifie que le fichier existe
        with open(file) as f: # with permet de gerer l'ouverture et la fermeture automatique du fichier
            f = [x.rstrip("\n") for x in f.readlines()] # On enlève les sauts de ligne et les retours à la ligne, inutile puisque chaque ligne est un éléments du tableau

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
    sql_liste = lire_fichier(path + "/" + file) # on lit le fichier contenant le code SQL

    # On établit la requête sql dans une seule ligne/chaine de caractères
    sql = ""
    for i in range(len(sql_liste)):
        sql += sql_liste[i] + " "

    try: # Résolution du probleme "sqlite3.OperationalError: no such table:", si on y arrive pas avec le module dédié
        base = Database.database(db)
        result = base.execute(sql)
    except: # On l'effectue de manière directe
        import sqlite3
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        result = cur.execute(sql).fetchall()
        conn.close()

    return result
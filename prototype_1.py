import os.path
import module_affichage as show
import module_database as Database
import module_lecture_fichier as read

def stockage_question(path, file):
    """
    permet le stockage des questions, réponses et nom de fichier contenu dans un fichier
    parametres:
               path, une chaine de caracteres indiquant le chemin d'accès au dossier avec le fichier cible
               file, une chaine de caracteres avec le nom du fichier cible
    renvoie un dictionnaire avec toutes les informations des requetes
    """
    contenu = read.lire_fichier(path + "/" + file)
    requetes = {}

    i = 1
    while i < len(contenu):
        if contenu[i][0] == "#":
            question = contenu[i][1:]
            sql_file = contenu[i-1]

            numero = ""
            k = 0
            while question[k] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]: # on détermine le numero de la question
                numero += question[k]
                k += 1

            reponse = ""
            while i+2 < len(contenu) and contenu[i+2][0] != "#": # tant que l'on n'est pas juste avant la prochaine question, on est dans la réponse précédente
                reponse += contenu[i+1] + "\n"
                i += 1

        i+=1
        requetes[int(numero)] = [question, reponse, sql_file] # déterminer s'il faut la réponse écrite ou juste le fichier

    return requetes

def question_console():
    dictionnaire = stockage_question("requetes", "alire.md")

    for key, value in dictionnaire.items():
        print(value[0])

    choix = int(input("Quelle question choisit-tu ? "))

    if choix in dictionnaire.keys():

        if not Database.database("imdb.db").test_connexion(): # On vérifie que la base de données est disponible
            print("Connexion à la base de données impossible")
            return

        resultat = read.execute_sql_file("requetes", dictionnaire[choix][2], "imdb.db")

        # affichage de la réponse
        separation = "-" * len(dictionnaire[choix][0]) + "------------"
        print(dictionnaire[choix][0])
        print(separation)
        print(dictionnaire[choix][1])
        print(separation)
        show.afficher_table(resultat)

def test():
    """
    fonction permettant de tester l'intégralité des requêtes recensées dans alire.md
    renvoie une série de print qui indique le résultat du test pour chaque requête
    """
    dictionnaire = stockage_question("requetes", "alire.md")

    for choix in dictionnaire.keys():

        try:
            resultat = read.execute_sql_file("requetes", dictionnaire[choix][2], "imdb.db")
            print("requete", choix, ": réussi")
        except:
            print("requete", choix, ": echec")


if __name__ == "__main__":
    question_console()
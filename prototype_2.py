# importation des modules nécessaires
import os.path
from modules import module_affichage as show
from modules import module_database as Database
from modules import module_lecture_fichier as read
from modules import module_tkinter as tk

def stockage_question(path, file):
    """
    permet le stockage des questions, réponses et nom de fichier contenu dans un fichier
    parametres:
               path, une chaine de caracteres indiquant le chemin d'accès au dossier avec le fichier cible
               file, une chaine de caracteres avec le nom du fichier cible
    renvoie un dictionnaire avec toutes les informations des requetes
    """
    contenu = read.lire_fichier(path + "/" + file) # On lit le fichier contenant les informations necessaires
    requetes = {}

    i = 1
    while i < len(contenu): # Tant que l'on n'as pas vus l'intégralité des lignes du fichier
        if contenu[i][0] == "#": # si la ligne choisit est une question
            question = contenu[i][1:] # On choisit cette ligne comme étant une question
            sql_file = contenu[i-1] # On choisit la ligne précédente comme étant le fichier répondant à cette question ( ici les .sql)

            # On détermine le numero de la question
            numero = ""
            k = 0
            while question[k] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]: # on détermine le numero de la question
                numero += question[k]
                k += 1

            # On détermine la réponse à la question
            reponse = ""
            while i+2 < len(contenu) and contenu[i+2][0] != "#": # tant que l'on n'est pas juste avant la prochaine question, on est dans la réponse précédente
                reponse += contenu[i+1] + "\n"
                i += 1

        i+=1
        requetes[int(numero)] = [question, reponse, sql_file] # On ajoute les informations prises dans le dictionnaire de stockage

    return requetes

def question_semi_console():
    """
    fonction permettant de selectionner une question puis d'en afficher la réponse dans une fenetre tkinter
    affiche les questions, demande à l'utilisateur de choisir l'index d'une question, affiche une réponse dans une fenetre tkinter
    """
    dictionnaire = stockage_question("requetes", "alire.md") # On stocke toutes les informations contenu dans le fichier alire.md

    # On affiche l'intégralité des questions enregistrées
    for key, value in dictionnaire.items():
        print(value[0])

    choix = int(input("Quelle question choisit-tu ? ")) # On demande l'index de la question choisit par l'utilisateur

    if choix in dictionnaire.keys(): # On s'assure que la question existe

        if not Database.database("imdb.db").test_connexion(): # On vérifie que la base de données est disponible
            print("Connexion à la base de données impossible")
        else:
            resultat = read.execute_sql_file("requetes", dictionnaire[choix][2], "imdb.db") # On charge le résultat de la requête qui répond à la question

            texte_entier = dictionnaire[choix][1] + "\n" + "-" * len(dictionnaire[choix][0]) + "\n\n" + show.afficher_table(resultat) # On rédige le texte à afficher dans la fenêtre dans une unique ligne/chaine de caracteres

            tk.affichage_texte_tkinter(dictionnaire[choix][0], texte_entier, len(dictionnaire[choix][0])) # affichage de la réponse dans une fenetre tkinter
    else:
        print("Index de question inexistant")
        question_console()


def test():
    """
    fonction permettant de tester l'intégralité des requêtes recensées dans alire.md
    renvoie une série de print qui indique le résultat du test pour chaque requête
    """
    dictionnaire = stockage_question("requetes", "alire.md")

    for choix in dictionnaire.keys(): # Pour chaque éléments enregistrés dans le dictionnaire

        try: # On teste si on peut en effectuer la requete
            resultat = read.execute_sql_file("requetes", dictionnaire[choix][2], "imdb.db")
            print("requete", choix, ": réussi")
        except:
            print("requete", choix, ": echec")


if __name__ == "__main__":
    question_semi_console()
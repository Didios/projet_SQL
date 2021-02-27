# importation des modules necessaires
import os.path
from modules import module_database as Database
from modules import module_lecture_fichier as read
from modules import module_tkinter as tk
import tkinter as Tk

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

def question():
    """
    fonction permettant l'exécution de la fenetre tkinter qui est la base du projet
    renvoie une fenetre tkinter contenant les question, la selection de la question entrène l'affichage de la réponse dans une autre fenetre tkinter
    """
    dictionnaire = stockage_question("requetes", "alire.md") # On stocke toutes les informations contenu dans le fichier alire.md

    taille_max = len_maximum([i[0] for i in dictionnaire.values()]) # On détermine la longueur maximum des questions afin d'ajuster la fenetre

    root = tk.affichage_question_tkinter("Questions :", dictionnaire, taille_max) # On lance l'affichage des questions dans une fenetre tkinter

    # On crée un Menu pour l'aide et les crédits
    barremenu = Tk.Menu(root)

    barremenu_cascade = Tk.Menu(barremenu, tearoff=0)

    # On ajoute les deux sous-menus : aide et credits
    barremenu_cascade.add_command(label="Aide", underline=0, command = aide) # la fonction aide sert à mettre des parametres en dérivation, puisque directement, cela ne fonctionne pas
    barremenu_cascade.add_command(label="Crédits", underline=0, command = credit) # la fonction credit sert à mettre des parametres en dérivation, puisque directement, cela ne fonctionne pas

    barremenu.add_cascade(label="A propos", underline=0, menu=barremenu_cascade)

    # On affiche la fenetre et le menu
    root.config(menu=barremenu)
    root.mainloop()

def len_maximum(tab):
    """
    fonction parmettant de connaître la longueur maximale des éléments d'un tableau
    parametres:
               tab, une liste d'éléments
    renvoi un entier étant la longueur maximale des elements du tableau
    """
    maxi = 0

    for elmt in tab: # On parcours le tableau
        if len(str(elmt)) > maxi: # on choicit la plus grande longueur d'élément
            maxi = len(str(elmt))

    return maxi

def affichage_texte_tkinter(document):
    """
    fonction permettant d'afficher un document texte dans une fenetre tkinter, les sauts de ligne ne sont pas pris en compte
    parametres:
               document, une chaine de caracteres avec le chemin d'acces au document texte
    renvoie une fenêtre tkinter avec le contenu de document
    """
    contenu = read.lire_fichier(document) # On lit le document

    # On transforme la liste de ligne en chaine de caracteres
    contenu_str = ""
    for ligne in contenu:
        contenu_str += ligne + "\n"

    # On parametres une fenetre tkinter
    root = Tk.Tk()
    root.title("Aide")

    # On y ajoute contenu_str dans une zone de texte
    zone_texte = Tk.Text(root, width = 70)
    zone_texte.insert("insert", contenu_str)

    # On affiche le tout
    zone_texte.pack()
    root.mainloop()

def aide():
    """
    fonction permettant d'effectuer l'affichage de l'aide
    renvoie une fenetre tkinter avec l'aide
    """
    affichage_texte_tkinter("README.md")

def credit():
    """
    fonction permettant d'effectuer l'affichage des crédits
    renvoie une fenetre tkinter avec les crédits
    """
    affichage_texte_tkinter("credits.md")

def test():
    """
    fonction permettant de tester l'intégralité des requêtes recensées dans alire.md
    renvoie une série de print qui indique le résultat du test pour chaque requête
    """
    tout_juste = True
    liste_echec = []

    dictionnaire = stockage_question("requetes", "alire.md")

    for choix in dictionnaire.keys(): # Pour chaque éléments enregistrés dans le dictionnaire

        try: # On teste si on peut en effectuer la requete
            resultat = read.execute_sql_file("requetes", dictionnaire[choix][2], "imdb.db")
        except:
            tout_juste = False
            liste_echec += [choix]

    if tout_juste == True:
        print("Tous les tests ont été passé avec succès")
    else:
        print("Liste des tests ayant échoué : ", liste_echec)

if __name__ == "__main__":
    question()
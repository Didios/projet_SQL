#!"C:\Winpython\python-3.8.5.amd64\python.exe"

# programme réalisé par Didier Mathias en classe de Terminale B

# importation des modules necessaires
import os.path
from modules import module_database as Database
from modules import module_lecture_fichier as read
from modules import module_html as pprint

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
            sql_file = contenu[i-1][:-1] # On choisit la ligne précédente comme étant le fichier répondant à cette question ( ici les .sql)

            numero = read.devine_numero(question)[0] # On détermine le numero de la question, le [0] est là car la fonction renvoie une liste, le premier numero touvé est donc celui de la question

            # On détermine la réponse à la question
            reponse = ""
            while i+2 < len(contenu) and contenu[i+2][0] != "#": # tant que l'on n'est pas juste avant la prochaine question, on est dans la réponse précédente
                reponse += contenu[i+1] + "\n" # on ajoute donc la ligne à la réponse de la requete
                i += 1

            requetes[int(numero)] = [question, reponse, sql_file] # On ajoute les informations prises dans le dictionnaire de stockage

        i+=1

    return requetes

def Lancement(base, requetes, config):
    """
    fonction permettant le lancement du programme dans sa globalité
    parametres:
        base, une chaine de caracteres contenant le chemin d'accès vers une base de données ( celle permettant de répondre aux questions )
        requetes, une chaine de caracteres avec le chemin d'accès aux dossier contenant les requetes et le fichier de configuration
        config, une chaine de caracteres avec le nom du fichier de configuration (voir énoncé)
    """
    # On crée les fichiers html pour l'aide et les crédits
    credit()
    aide()

    pprint.debuthtml("Questions :")

    # On place un menu permettant l'accès aux pages html précédemment crée
    print('<menu type="toolbar">')
    print('<menu label="A propos">')
    print('<button onclick="window.open(%s)"> %s </button>' % ("'data/credits.html'", "Crédits"))
    print('<button onclick="window.open(%s)"> %s </button>' % ("'data/aide.html'", "Aide"))
    print("</menu>")
    print("<menu>")

    question(requetes, config, base)

    pprint.finhtml()

def question(requetes, config, base):
    """
    fonction permettant d'afficher les questions dans une fenetre tkinter
    parametres:
        requetes, une chaine de caracteres avec le chemin d'accès aux requetes et au fichier de configuration
        config, une chaine de caracteres indiquant le nom du fichier de configuration
        base, une chaine de caracteres contenant le chemin d'accès vers la base de données
    affiche les questions dans le fenetre tkinter, la selection de la question entraine l'affichage de la réponse dans une autre fenetre tkinter
    """
    dictionnaire = stockage_question(requetes, config) # On stocke toutes les informations contenu dans le fichier de configuration

    pprint.affichage_question_html(dictionnaire, base) # On affiche les boutons dans la page

    pprint.affichage_question_html(dictionnaire, base, True) # On crée les fichiers html auquel sont rattachés les boutons


def caracteres(texte):
    """
    fonction permettant d'obtenir une liste de tous les caracteres distinct présent dans une chaine de caracteres
    parametres:
        texte, une chaine de caracteres
    renvoie une liste de caracteres
    """
    lettres = []

    for caractere in texte:
        if caractere not in lettres:
            lettres += [caractere]

    return lettres

def len_maximum(tab):
    """
    fonction parmettant de connaître la longueur maximale des éléments d'un tableau
    parametres:
        tab, une liste d'éléments
    renvoi un entier étant la longueur maximale des elements du tableau
    """
    maxi = 0

    for elmt in tab: # On parcours le tableau
        if len(str(elmt)) > maxi: # on choisit la plus grande longueur d'élément
            maxi = len(str(elmt))

    return maxi

def aide():
    """
    fonction permettant d'actualiser/crée un fichier html contenant l'aide
    """
    if read.fichier_existe("data/aide.html"):
        read.suppr_fichier("data/aide.html", False)

    texte = "<html><head>\nAide\n</head><body><p>\n"

    # on met le contenu du fichier README.md dans la page
    contenu = read.lire_fichier("README.md", True)
    for i in contenu:
        texte += "</br>\n"
        texte += i + "\n"


    texte += "</p></body></html>"

    read.add_fichier("data", "aide.html", texte)

def credit():
    """
    fonction permettant d'actualiser/crée un fichier html contenant les crédits
    """
    if read.fichier_existe("data/credits.html"):
        read.suppr_fichier("data/credits.html", False)

    texte = "<html><head>\nCrédits\n</head><body><p>\n"

    # on met le contenu du fichier README.md dans la page
    contenu = read.lire_fichier("credits.md", True)
    for i in contenu:
        texte += "</br>\n"
        texte += i + "\n"

    texte += "</p></body></html>"

    read.add_fichier("data", "credits.html", texte)

def test():
    """
    fonction permettant de tester l'intégralité des requêtes recensées dans alire.md
    renvoie un print indiquant les résultats des tests
    """
    liste_echec = []

    dictionnaire = stockage_question("requetes", "alire.md")

    for choix in dictionnaire.keys(): # Pour chaque éléments enregistrés dans le dictionnaire
        try: # On teste si on peut en effectuer la requete
            resultat = read.execute_sql_file("requetes", dictionnaire[choix][2], "imdb.db")
        except: # sinon cela signifie que tous n'est pas juste et on ajoute le numero de la requetes dans les echec
            liste_echec += [choix]

    if liste_echec == []:
        print("Tous les tests ont été passé avec succès")
    else:
        print("Liste des tests ayant échoué : ", liste_echec)

if __name__ == "__main__":
    Lancement("imdb.db", "requetes", "alire.md")
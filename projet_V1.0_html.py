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

def Lancement(base, requetes, config):
    """
    fonction permettant le lancement du programme dans sa globalité
    parametres:
        base, une chaine de caracteres contenant le chemin d'accès vers une base de données ( celle permettant de répondre aux questions )
        requetes, une chaine de caracteres avec le chemin d'accès aux dossier contenant les requetes et le fichier de configuration
        config, une chaine de caracteres avec le nom du fichier de configuration (voir énoncé)
    """
    def add(event = None):
        """
        sous-fonction permettant l'exécution de la fonction ajouter car les commandes associé à tkinter ne peuvent pas contenir d'argument
        """
        dictionnaire = stockage_question(requetes, config) # On stocke toutes les informations contenu dans le fichier de configuration
        ajouter(dictionnaire, requetes, config, base)

    def suppr(event = None):
        """
        sous-fonction permettant l'exécution de la fonction supprimer car les commandes associé à tkinter ne peuvent pas contenir d'argument
        """
        dictionnaire = stockage_question("requetes", "alire.md") # On stocke toutes les informations contenu dans le fichier de configuration
        supprimer(dictionnaire, "requetes", "alire.md", base)

    credit()
    aide()

    pprint.debuthtml("Questions :")

    print('<menu type="toolbar">')
    print('<menu label="A propos">')
    print('<button onclick="window.open(%s)"> %s </button>' % ("'data/credits.html'", "Crédits"))
    print('<button onclick="window.open(%s)"> %s </button>' % ("'data/aide.html'", "Aide"))
    print("</menu>")
    print("<menu>")

    # menu avec bouton :                            permanents
    #    aide
    #    credits
    #    ajout
    #    suppression

    question(requetes, config, base)

    # raccourci clavier
"""
    # ajout de raccourci clavier
    root.bind("<Control-KeyPress-a>", add)
    root.bind("<Control-KeyPress-s>", suppr)
"""

def question(requetes, config, base, dictionnaire = None):
    """
    fonction permettant d'afficher les questions dans une fenetre tkinter
    parametres:
        root, une fenetre tkinter dans laquelle on affiche les questions
        requetes, une chaine de caracteres avec le chemin d'accès aux requetes et au fichier de configuration
        config, une chaine de caracteres indiquant le nom du fichier de configuration
        base, une chaine de caracteres contenant le chemin d'accès vers la base de données
        dictionnaire, optionnel, un dictionnaire indiquant les informations des requetes comme suit : {indice de la question : [question, reponse, fichier sql associé], ... }
    affiche les questions dans le fenetre tkinter, la selection de la question entraine l'affichage de la réponse dans une autre fenetre tkinter
    """

    if dictionnaire is None:
        dictionnaire = stockage_question(requetes, config) # On stocke toutes les informations contenu dans le fichier de configuration

    pprint.affichage_question_html(dictionnaire, base)

    pprint.finhtml()

    pprint.affichage_question_html(dictionnaire, base, True)

# c'est une sorte de div qui s'ajoute quand on clique sur le bouton
def ajouter(root, dico, requetes, config, base):
    """
    fonction permettant d'ajouter une requête via une #############################################
    parametres:
        root, une fenetre tkinter
        dico, un dictionnaire du type : {indice de la question : [question, reponse, fichier sql associé], ... }
        requetes, une chaine de caracteres avec le chemin d'accès vers le fichier contenant les requetes
        config, une chaine de caracteres avec le nom du fichier de configuration des requetes
        base, une chaine de caracteres avec le chemin d'accès vers la base de données
    """
    # on affiche le div qui contient des champs à remplir
    # ou on mets des boites de dialogue en route qui receuille les informations

    # ensemble des tooltips de champs et des verification de champs
    def numero_verifier(event):
        """
        sous-fonction qui permet de vérifier que le champs pour l'indice est correcte
        """
        pass

    def question_verifier(event):
        """
        sous-fonction qui permet de vérifier que le champs pour la question est correcte
        """
        pass

    def requete_verifier(event):
        """
        sous-fonction qui permet de vérifier que le champs pour la requete est correcte
        """
        pass

    def incrementation():
        """
        sous-fonction permettant le remplissage automatique du champs 'indice de la requete'
        """
        indice = [t for t in dico.keys()]
        i_max = max(indice)

    def validation():
        """
        sous-fonction permettant de faire la validation des conditions et d'ajouter la requête au fichier
        """
        pass

    def temp():
        """
        sous-fonction qui permet de gérer un fichier temporaire qui contiendrat les informations en cours d'enregistrement
        cette sous-fonction est une boucle
        """
        pass

    # affichage pour la demande de l'indice
    # affichage en cas d'erreur d'indice

    # affichage pour la demande de la question
    # affichage en cas d'abcence de question

    # affichage pour la demande de la requête
    # affichage en cas de problemes avec la requete

    # affichage d'un bouton de validation et de retour

    # on vérifie si une requete n'été pas déjà en cours, si oui, on la charge, sinon, on crée le fichier temp.txt
    if read.fichier_existe(requetes + "/temp.txt"):
        temporaire = read.lire_fichier(requetes + "/temp.txt", True)

    else:
        read.add_fichier(requetes, "temp.txt")

    # on met un raccourci clavier pour retourner au questions
    temp()

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

# c'est une sorte de div qui s'ajoute quand on clique sur le bouton
def supprimer(root, dico, requetes, config, base):
    """
    fonction permettant d'ajouter une requête via une fenetre tkinter
    parametres:
        root, une fenetre tkinter
        dico, un dictionnaire du type : {indice de la question : [question, reponse, fichier sql associé], ... }
        requetes, une chaine de caracteres avec le chemin d'accès vers le fichier contenant les requetes
        config, une chaine de caracteres avec le nom du fichier de configuration des requetes
        base, une chaine de caracteres avec le chemin d'accès vers la base de données
    """
    questions_supprimer = []

    def cases_cochees():
        """
        sous-fonction permettant de connaître les cases qui ont été coché
        (questions_supprimer est une liste de variables, donc les valeurs changent sans intervention dans le programme)
        renvoi une liste des index des cases sélectionner
        """
        numeros_cases = []

        for i in range(0,0): # nombre de questions possibles
            pass
            # On regarde si la case à été coché
                # on ajoute l'index de la question

        return numeros_cases

    def validation():
        """
        sous-fonction permettant de :
            connaître les cases cochées
            retirer les requetes associée aux cases cochées
        """
        suppr = cases_cochees()

        if messagebox.askyesno("Validation", "Est-tu sûr de vouloir supprimer (pour toujours) les questions :" + str(suppr)):
            alire =[0] + read.lire_fichier("requetes/alire.md", True) # l'ajout de la premiere valeur permet d'être en accrod sur le décompte avec la fonction read.suppr_lignes

            i_lignes = [] # on va stocker ici la liste des lignes à supprimer du document alire.md

            for n_question in suppr: # on parcours chaque questions sélectionner

                # on avance le compteur l des indices tant qu'on n'est pas sur la bonne question
                l = 1
                while alire[l][:len(n_question)] != n_question:
                    l += 1

                # on supprime le fichier sql associé qui se trouve une ligne au dessus
                read.suppr_fichier("requetes/" + alire[l-1], False)
                i_lignes += [l-1]

                # la détection se fait par la précence de # donc on enleve manuellement le premier
                i_lignes += [l]
                l += 1

                # on ajoute les indices tant qu'on n'as pas fini de parcourir les lignes de la question
                while l < len(alire) and len(alire[l]) > 0 and alire[l][0] != "#":
                    i_lignes += [l]
                    l += 1

            read.suppr_lignes("requetes/alire.md", *i_lignes) # une fois tous les indices de lignes récoltées, on supprime les lignes

            retour() # on retourne au menu

    def retour():
        """
        sous-fonction permettant de revenir au menu principal
        elle fait redémarrer le programme
        """
        pass

    # ajout d'un racourci clavier pour retourner au question

    # on affiche les requetes possibles
    ligne = 0
    for number, lien in dico.items(): # on parcours le dictionnaire qui contient toutes les questions
        valeur = Tk.IntVar()
        check = Tk.Checkbutton(frame, text = dico[number][0], variable = valeur) # mettre une variable permet de ne pas faire une fonction pour chaque cases pour voir si elle est coché ou non lors de la suppression
        ligne += 1
        # les questions à un chiffre on un 0 devant elles (req1.sql => #01), ils faut donc les différencier afin d'éviter les erreurs
        if number < 10:
            questions_supprimer.append([valeur, "#0" + str(number)])
        else:
            questions_supprimer.append([valeur, "#" + str(number)])
        check.grid(row = ligne, column = 0, sticky="w")

    # affichage d'un bouton de validation et de retour


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
    fonction permettant d'effectuer l'affichage de l'aide
    renvoie
    """
    if read.fichier_existe("data/aide.html"):
        read.suppr_fichier("data/aide.html", False)

    texte = "<html><head>\nAide\n</head><body><p>\n"

    aide_contenu = read.lire_fichier("README.md", True)
    for i in aide_contenu:
        texte += "</br>\n"
        texte += i + "\n"


    texte += "</p></body></html>"

    read.add_fichier("data", "aide.html", texte)

def credit():
    """
    fonction permettant d'effectuer l'affichage des crédits
    renvoie
    """
    if read.fichier_existe("data/credits.html"):
        read.suppr_fichier("data/credits.html", False)

    texte = "<html><head>\nCrédits\n</head><body><p>\n"

    aide_contenu = read.lire_fichier("credits.md", True)
    for i in aide_contenu:
        texte += "</br>\n"
        texte += i + "\n"

    texte += "</p></body></html>"

    read.add_fichier("data", "credits.html", texte)

def test():
    """
    fonction permettant de tester l'intégralité des requêtes recensées dans alire.md
    renvoie un print indiquant les résultats des tests
    """
    tout_juste = True
    liste_echec = []

    dictionnaire = stockage_question("requetes", "alire.md")

    for choix in dictionnaire.keys(): # Pour chaque éléments enregistrés dans le dictionnaire

        try: # On teste si on peut en effectuer la requete
            resultat = read.execute_sql_file("requetes", dictionnaire[choix][2], "imdb.db")
        except: # sinon cela signifie que tous n'est pas juste et on ajoute le numero de la requetes dans les echec
            tout_juste = False
            liste_echec += [choix]

    if tout_juste == True:
        print("Tous les tests ont été passé avec succès")
    else:
        print("Liste des tests ayant échoué : ", liste_echec)

if __name__ == "__main__":
    Lancement("imdb.db", "requetes", "alire.md")
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
    def add():
        ajouter(root, dictionnaire)

    def suppr():
        pass

    dictionnaire = stockage_question("requetes", "alire.md") # On stocke toutes les informations contenu dans le fichier alire.md

    taille_max = len_maximum([i[0] for i in dictionnaire.values()]) # On détermine la longueur maximum des questions afin d'ajuster la fenetre

    root = tk.affichage_question_tkinter("Questions :", dictionnaire, taille_max) # On lance l'affichage des questions dans une fenetre tkinter

    # On crée un Menu pour l'aide et les crédits
    barremenu = Tk.Menu(root)

    barre_aide = Tk.Menu(barremenu, tearoff=0)
    barre_modification = Tk.Menu(barremenu, tearoff=0)

    # On ajoute les deux sous-menus : aide et credits
    barre_aide.add_command(label="Aide", underline=0, command = aide) # la fonction aide sert à mettre des parametres en dérivation, puisque directement, cela ne fonctionne pas
    barre_aide.add_command(label="Crédits", underline=0, command = credit) # la fonction credit sert à mettre des parametres en dérivation, puisque directement, cela ne fonctionne pas

    # on ajoute les sous menus ajout et suppression
    barre_modification.add_command(label="Ajout", underline=0, command = add)
    barre_modification.add_command(label="Suppression", underline=0, command = suppr)

    barremenu.add_cascade(label="A propos", underline=0, menu=barre_aide)
    barremenu.add_cascade(label="Modification", underline=0, menu=barre_modification)

    # On affiche la fenetre et le menu
    root.config(menu=barremenu)
    root.mainloop()

def ajouter(root, dico):
    tk.clean(root, "Menu")
    root.title("")
    renseignement = [False, False, False]

    # ensemble des tooltips de champs et des verification de champs
    def numero_verifier(event):
        try:
            int(numero.get("current linestart", "current lineend"))
            renseignement[0] = True
            # on enleve le message en rouge
            n_texte.set("")
        except:
            renseignement[0] = False
            # on met le message en rouge
            n_texte.set("L'indice de la requetes doit être un entier")

    def question_verifier(event):
        texte = question_sql.get("current linestart", "current lineend")
        lettres = []

        for caractere in texte:
            if caractere not in lettres:
                lettres += [caractere]

        if texte == "" or ( len(lettres) == 1 and lettres[0] == " "):
            renseignement[1] = False
            # on met le message en rouge
            q_texte.set("La requete doit posséder une question/sujet/énoncé")
        else:
            renseignement[1] = True
            # on enleve le message en rouge
            q_texte.set("")

    def requete_verifier(event):
        texte = requete.get("1.0", "end")
        lettres = []
        for caractere in texte:
            if caractere not in lettres:
                lettres += [caractere]

        data = Database.database("imdb.db")
        if data.execute(texte) == None:
            renseignement[2] = False
            # on met le message en rouge
            r_texte.set("La requete n'est pas valide, veuillez corriger")
        elif len(lettres) < 3 and (" " in lettres or "\n" in lettres):
            renseignement[2] = False
            # on met le message en rouge
            r_texte.set("Veuillez écrire une requête")
        else:
            renseignement[2] = True
            # on enleve le message en rouge
            r_texte.set("")


    def incrementation():
        """
        fonction permettant le remplissage automatique du champs indice de la requetes
        """
        indice = [t for t in dico.keys()]
        i_max = max(indice)

        numero.delete("1.0", "end")
        numero.insert("insert", str(i_max + 1))

    def validation():
        from tkinter import messagebox

        numero_verifier("valider")
        question_verifier("valider")
        requete_verifier("valider")

        if renseignement[0] == False: # l'indice indiquer ne contient autre chose que des chiffres ou est vide
            messagebox.showerror("Indice", "Seules les chiffres sont autorisées pour les indices. Aucun espace, aucune lettres ou caractère spécial n'est autorisé")

        elif renseignement[1] == False: # la question est inexistante
            messagebox.showerror("Question", "Un énoncé, un sujet ou une question doit être fourni pour toutes requête ajouté")

        elif renseignement[2] == False: # la requete n'est pas bonne
            messagebox.showerror("Requête SQL", "La requête SQL n'est pas fonctionelle, veuillez corriger votre requete")

        else:
            index = str(numero.get("current linestart", "current lineend"))

            texte_requete = requete.get("1.0", "end")
            question_sujet = "#" + index + "." + question_sql.get("1.0", "end")
            sql_file = "req" + index + ".sql"

            # si tous est bon :
            with open("requetes/" + sql_file, "x") as fichier: # on cree un fichier .sql pour ajouter la requete
                fichier.write(texte_requete)

            with open("requetes/alire.md", "a") as alire: # on ajoute les données de la requete dans alire.md
                alire.write("\n \n" + sql_file + "\n" + question_sujet + texte_requete)

            root.destroy()
            question() # on retourne sur l'écran principal
            # faire en sorte de ne pas fermer la fenetre = changement de question -> initialisation + base

    def retour():
        root.destroy()
        question() # on retourne sur l'écran principal


    Tk.Label(root, text = "Indice de la question :").grid(row = 0, column = 0, sticky = "w")
    Tk.Button(root, text = "Incrémentation automatique", command = incrementation).grid(row = 0, column = 1, sticky = "e")
    numero =  Tk.Text(root, height = 1, width = 100)
    numero.bind("<Enter>", numero_verifier)
    numero.bind("<Leave>", numero_verifier)
    numero.grid(row = 1, column = 0, columnspan = 2)

    n_texte = Tk.StringVar()
    erreur_numero =  Tk.Label(root, text = "", fg = "red", textvariable = n_texte)
    erreur_numero.grid(row = 2, column = 0, sticky = "w")

    Tk.Label(root, text = "Question posée : ").grid(row = 3, column = 0, sticky = "w")
    question_sql = Tk.Text(root, height = 1, width = 100)
    question_sql.bind("<Enter>", question_verifier)
    question_sql.bind("<Leave>", question_verifier)
    question_sql.grid(row = 4, column = 0, columnspan = 2)

    q_texte = Tk.StringVar()
    erreur_question = Tk.Label(root, text = "", fg = "red", textvariable = q_texte)
    erreur_question.grid(row = 5, column = 0, sticky = "w")

    Tk.Label(root, text = "Requete SQL :").grid(row = 6, column = 0, sticky = "w")
    requete = Tk.Text(root, height = 10, width = 100)
    requete.bind("<Enter>", requete_verifier)
    requete.bind("<Leave>", requete_verifier)
    requete.grid(row = 7, column = 0, columnspan = 2)

    r_texte = Tk.StringVar()
    erreur_requete = Tk.Label(root, text = "", fg = "red", textvariable = r_texte)
    erreur_requete.grid(row = 8, column = 0, sticky = "w")

    Tk.Button(root, text = "valider", command = validation, width = 20, height = 5).grid(row = 9, column = 0, sticky = "w")
    Tk.Button(root, text = "retour", command = retour, width = 20, height = 5).grid(row = 9, column = 1, sticky = "e")

def supprimer():
    pass

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
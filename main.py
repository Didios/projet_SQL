# importation des modules necessaires
import os.path
from modules import module_database as Database
from modules import module_lecture_fichier as read
from modules import module_tkinter as tk
import tkinter as Tk
from tkinter import messagebox

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
        ajouter(root, dictionnaire, requetes, config, base)

    def suppr(event = None):
        """
        sous-fonction permettant l'exécution de la fonction supprimer car les commandes associé à tkinter ne peuvent pas contenir d'argument
        """
        dictionnaire = stockage_question(requetes, config) # On stocke toutes les informations contenu dans le fichier de configuration
        supprimer(root, dictionnaire, requetes, config, base)

    root = Tk.Tk()
    root.title("Projet SQL")

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

    # On place les sous-menus crée dans le Menu barremenu
    barremenu.add_cascade(label="A propos", underline=0, menu=barre_aide)
    barremenu.add_cascade(label="Modification", underline=0, menu=barre_modification)

    root.config(menu=barremenu) # On place le menu dans la fenetre

    question(root, requetes, config, base)

    # ajout de raccourci clavier
    root.bind("<Control-KeyPress-a>", add)
    root.bind("<Control-KeyPress-s>", suppr)

    root.mainloop()

def question(root, requetes, config, base, dictionnaire = None):
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
    tk.clean(root, "Menu")

    if dictionnaire is None:
        dictionnaire = stockage_question(requetes, config) # On stocke toutes les informations contenu dans le fichier de configuration

    taille_max = len_maximum([i[0] for i in dictionnaire.values()]) # On détermine la longueur maximum des questions afin d'ajuster la fenetre

    root, liste = tk.affichage_question_tkinter("Questions :", dictionnaire, taille_max, base, root) # On lance l'affichage des questions dans une fenetre tkinter

    # on ajoute une barre de défilement afin de faciliter l'accès aux questions
    scroll = Tk.Scrollbar(root,orient="vertical")
    scroll.pack(side="right", fill="y")
    scroll.config(command=liste.yview)

def ajouter(root, dico, requetes, config, base):
    """
    fonction permettant d'ajouter une requête via une fenetre tkinter
    parametres:
        root, une fenetre tkinter
        dico, un dictionnaire du type : {indice de la question : [question, reponse, fichier sql associé], ... }
        requetes, une chaine de caracteres avec le chemin d'accès vers le fichier contenant les requetes
        config, une chaine de caracteres avec le nom du fichier de configuration des requetes
        base, une chaine de caracteres avec le chemin d'accès vers la base de données
    """
    # on enlève ce qui se trouve sur la fenetre
    tk.clean(root, "Menu")
    root.title("Ajout de requête")
    renseignement = [False, False, False]

    # ensemble des tooltips de champs et des verification de champs
    def numero_verifier(event):
        """
        sous-fonction qui permet de vérifier que le champs pour l'indice est correcte
        """
        try: # on tente d'obtenir un entier avec le contenu du champs
            nbr = int(numero.get("current linestart", "current lineend"))
            if nbr in dico.keys():
                renseignement[0] = False
                n_texte.set("L'indice indiqué existe déjà")
            else:
                renseignement[0] = True
                if nbr < 10: # on fait en sorte de toujours écrire les nombres avec 2 chiffres minimum : 1 -> 01
                    numero.delete("current linestart", "current lineend")
                    numero.insert("current linestart", "0"+ str(nbr))
                n_texte.set("")
        except: # si ca ne marche pas, les conditions ne sont pas remplis : erreur
            renseignement[0] = False
            n_texte.set("L'indice de la requetes doit être un entier")

    def question_verifier(event):
        """
        sous-fonction qui permet de vérifier que le champs pour la question est correcte
        """
        texte = question_sql.get("current linestart", "current lineend") # on prend la question du premier au dernier caracteres de la ligne

        lettres = caracteres(texte) # on liste les caracteres du champs pour voir si il y a quelque chose d'écrit (autre que des espaces)

        if texte == "" or ( len(lettres) == 1 and lettres[0] == " "): # On regarde si le champs n'est pas vide
            renseignement[1] = False
            q_texte.set("La requete doit posséder une question/sujet/énoncé")
        else:
            renseignement[1] = True
            q_texte.set("")

    def requete_verifier(event):
        """
        sous-fonction qui permet de vérifier que le champs pour la requete est correcte
        """
        texte = requete.get("1.0", "end") # on prend la requete du premier caracteres jusqu'au dernier
        lettres = caracteres(texte)

        data = Database.database(base) # on met en route la base de données pour tester

        if data.execute(texte) == None: # si on obtient None, la requete ne s'est pas exécuté est donc elle est fausse
            renseignement[2] = False
            r_texte.set("La requete n'est pas valide, veuillez corriger")
        elif len(lettres) < 3 and (" " in lettres or "\n" in lettres): # si la requete ne contient que des espaces, elle peut s'éxécuter, ce cas est donc détaillé
            renseignement[2] = False
            r_texte.set("Veuillez écrire une requête")
        else:
            renseignement[2] = True
            r_texte.set("")


    def incrementation():
        """
        sous-fonction permettant le remplissage automatique du champs 'indice de la requete'
        """
        indice = [t for t in dico.keys()]
        i_max = max(indice)

        numero.delete("1.0", "end")
        numero.insert("insert", str(i_max + 1))

    def validation():
        """
        sous-fonction permettant de faire la validation des conditions et d'ajouter la requête au fichier
        """
        # on effectue une vérification pour chaque champs
        numero_verifier("valider")
        question_verifier("valider")
        requete_verifier("valider")

        # on affiche une erreur si une condition n'est pas remplie
        if renseignement[0] == False: # l'indice indiquer ne contient autre chose que des chiffres ou est vide
            messagebox.showerror("Indice", "Seules les chiffres sont autorisées pour les indices. Aucun espace, aucune lettres ou caractère spécial n'est autorisé")

        elif renseignement[1] == False: # la question est inexistante
            messagebox.showerror("Question", "Un énoncé, un sujet ou une question doit être fourni pour toutes requête ajouté")

        elif renseignement[2] == False: # la requete n'est pas bonne
            messagebox.showerror("Requête SQL", "La requête SQL n'est pas fonctionelle, veuillez corriger votre requete")

        else:
            read.suppr_fichier(requetes + "\temp.txt", False)

            index = numero.get("current linestart", "current lineend")

            texte_requete = requete.get("1.0", "end")
            question_sujet = "#" + index + "." + question_sql.get("1.0", "end")
            sql_file = "req" + str(int(index)) + ".sql" # le str(int permet de transformer les nombre du type 01 en 1

            read.add_fichier(requetes, sql_file, texte_requete) # on cree un fichier .sql en écriture pour ajouter la requete

            read.add_ligne(requete, config, "\n \n" + sql_file + "\n" + question_sujet + texte_requete) # on ajoute les données de la requete dans le fichier de configuration

            retour() # on retourne sur l'écran principal

    def retour(event = ""):
        """
        sous-fonction permettant de revenir au menu principal
        """
        question(root, requetes, config, base)

    def temp():
        """
        sous-fonction qui permet de gérer un fichier temporaire qui contiendrat les informations en cours d'enregistrement
        cette sous-fonction est une boucle
        """
        try: # on essaye d'enregistrer les informations
            read.remplacer_ligne(requetes, "temp.txt", 1, numero.get("current linestart", "current lineend"))
            read.remplacer_ligne(requetes, "temp.txt", 2, question_sql.get("current linestart", "current lineend"))

            # on efface toutes les autres lignes pour mettre la requete
            temporaire = read.lire_fichier(requetes + "/temp.txt", True)
            read.suppr_lignes(requetes + "/temp.txt", * [i for i in range(3, len(temporaire) +1)])

            read.remplacer_ligne(requetes, "temp.txt", 3, requete.get("1.0", "end")) # on ajoute la requete en cours au fichier

            root.after(100, temp) # On répète la fonction toutes les 0.1s
        except: # si on ne peut pas, cela signifie qu'il n'y a plus de fentre et donc la fonction s'arrête
            pass

    # affichage pour la demande de l'indice
    Tk.Label(root, text = "Indice de la question :").grid(row = 0, column = 0, sticky = "w")
    Tk.Button(root, text = "Incrémentation automatique", command = incrementation).grid(row = 0, column = 1, sticky = "e")
    numero =  Tk.Text(root, height = 1, width = 100)
    numero.bind("<Leave>", numero_verifier)
    numero.grid(row = 1, column = 0, columnspan = 2)

    # affichage en cas d'erreur d'indice
    n_texte = Tk.StringVar()
    erreur_numero =  Tk.Label(root, text = "", fg = "red", textvariable = n_texte)
    erreur_numero.grid(row = 2, column = 0, sticky = "w")

    # affichage pour la demande de la question
    Tk.Label(root, text = "Question posée : ").grid(row = 3, column = 0, sticky = "w")
    question_sql = Tk.Text(root, height = 1, width = 100)
    question_sql.bind("<Leave>", question_verifier)
    question_sql.grid(row = 4, column = 0, columnspan = 2)

    # affichage en cas d'abcence de question
    q_texte = Tk.StringVar()
    erreur_question = Tk.Label(root, text = "", fg = "red", textvariable = q_texte)
    erreur_question.grid(row = 5, column = 0, sticky = "w")

    # affichage pour la demande de la requête
    Tk.Label(root, text = "Requete SQL :").grid(row = 6, column = 0, sticky = "w")
    requete = Tk.Text(root, height = 10, width = 100)
    requete.bind("<Leave>", requete_verifier)
    requete.grid(row = 7, column = 0, columnspan = 2)

    # affichage en cas de problemes avec la requete
    r_texte = Tk.StringVar()
    erreur_requete = Tk.Label(root, text = "", fg = "red", textvariable = r_texte)
    erreur_requete.grid(row = 8, column = 0, sticky = "w")

    # affichage d'un bouton de validation et de retour
    Tk.Button(root, text = "valider", command = validation, width = 20, height = 5).grid(row = 9, column = 0, sticky = "w")
    Tk.Button(root, text = "retour", command = retour, width = 20, height = 5).grid(row = 9, column = 1, sticky = "e")


    # on vérifie si une requete n'été pas déjà en cours, si oui, on la charge, sinon, on crée le fichier temp.txt
    if read.fichier_existe(requetes + "/temp.txt"):
        temporaire = read.lire_fichier(requetes + "/temp.txt", True)

        numero.insert("current linestart", temporaire[0])
        question_sql.insert("current linestart", temporaire[1])

        req = ""
        for ligne in temporaire[2:]:
            req += ligne + "\n"

        requete.insert("1.0", req)

        numero_verifier("")
        question_verifier("")
        requete_verifier("")
    else:
        read.add_fichier(requetes, "temp.txt")

    root.bind("<Escape>", retour)
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
    # on nettoie la fenêtre et on change son nom
    tk.clean(root, "Menu")
    root.title("Suppression de requêtes")
    questions_supprimer = []

    def cases_cochees():
        """
        sous-fonction permettant de connaître les cases qui ont été coché
        (questions_supprimer est une liste de variables, donc les valeurs changent sans intervention dans le programme)
        renvoi une liste des index des cases sélectionner
        """
        numeros_cases = []

        for i in range(0,len(questions_supprimer)):
            if questions_supprimer[i][0].get() == 1: # On regarde si la case à été coché
                numeros_cases.append(questions_supprimer[i][1]) # on ajoute l'index de la question

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

                # on ajoute les indices tant qu'on n'as pas fini la question
                while l < len(alire) and len(alire[l]) > 0 and alire[l][0] != "#":
                    i_lignes += [l]
                    l += 1

            read.suppr_lignes("requetes/alire.md", *i_lignes) # une fois tous les indices de lignes récoltées, on supprime les lignes

            retour() # on retourne au menu

    def retour(event = ""):
        """
        sous-fonction permettant de revenir au menu principal
        elle fait redémarrer le programme
        """
        question(root, requetes, config, base)

    root.bind("<Escape>", retour)

    # d'ici à la barre, on installe une scrollbar pour pouvoir afficher toutes les questions (cela évite les fenêtres trop grandes)
    ff = Tk.Frame(root)
    ff.grid(row=0, column=0, columnspan=2)

    H = len(dico.values()) * 25
    W = str( len_maximum([t[0] for t in dico.values()]) //5) + "c"

    canvas = Tk.Canvas(ff, width=W, scrollregion =(0, 0, 10, H))
    canvas.pack(side="left")

    frame = Tk.Frame(canvas)
    frame.pack()

    vbar = Tk.Scrollbar(ff,orient="vertical")
    vbar.pack(side="right", fill="y")
    vbar.config(command=canvas.yview)
    canvas['yscrollcommand']=vbar.set
    canvas.create_window((0,0),window=frame,width=W, height=H, anchor='nw')
    ############################################################################

    # on ajoute les requêtes
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
    Tk.Button(root, text = "valider", command = validation, width = 20, height = 5).grid(row = 1, column = 0, sticky = "w")
    Tk.Button(root, text = "retour", command = retour, width = 20, height = 5).grid(row = 1, column = 1, sticky = "e")


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
    renvoie une fenetre tkinter avec l'aide
    """
    texte_liste = read.lire_fichier("README.md", True)
    texte = ""
    for t in texte_liste:
        texte += t + "\n"
    tk.affichage_texte_tkinter("aide", texte, len_maximum(texte_liste) +2)

def credit():
    """
    fonction permettant d'effectuer l'affichage des crédits
    renvoie une fenetre tkinter avec les crédits
    """
    texte_liste = read.lire_fichier("credits.md", True)
    texte = ""
    for t in texte_liste:
        texte += t + "\n"
    tk.affichage_texte_tkinter("credits", texte, len_maximum(texte_liste) +2)

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
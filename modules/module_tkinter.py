# On importe les modules necessaires
from tkinter import Tk, Text, Listbox, Scrollbar

# l'importation de ces modules dépend de la façon dans est exécuté le fichier
try:
    import module_affichage as show
    import module_lecture_fichier as read
    import module_tri as tris
except:
    from modules import module_affichage as show
    from modules import module_lecture_fichier as read
    from modules import module_tri as tris

def affichage_texte_tkinter(titre, texte, taille = 100):
    """
    fonction permettant d'afficher un texte choisit dans une fenetre tkinter
    parametres:
               titre, une chaine de caracteres donnant le titre de la fenetre
               texte, une chaine de caracteres étant le texte à afficher
               taille, optionnel, un entier qui est le nombre maximal de caracteres sur une ligne
    affiche une fenetre tkinter
    """
    # On défini une fenetre tkinter root ainsi que son titre
    root = Tk()
    root.title(titre)

    # On définit affiche qui servira à mettre le texte dans la fenetre ainsi que scroll qui permettrat de faire défiler affiche si sa taille est trop petite
    affiche = Text(root, width = taille + 10)
    scroll = Scrollbar(root, orient="vertical", command=affiche.yview)
    affiche.config(yscrollcommand=scroll.set)

    # On ajoute dans la zone de texte le texte que l'on doit afficher
    affiche.insert("insert", texte)

    # On affiche la fenetre ainsi que les éléments qu'elle contient
    scroll.pack(side="right", fill="y")
    affiche.pack(side="left")
    affiche.configure(state='disabled') # comme on veut juste afficher du texte, on désactive la zone de texte afin que l'utilisateur ne puisse pas la modifier
    root.mainloop()

def affichage_question_tkinter(titre, stockage, taille, base, root = None):
    """
    fonction permettant d'afficher une série de questions ainsi que de gerer les réponses contenue dans un dictionnaire, le tout dans une fenetre tkinter
    parametres:
               titre, une chaine de caracteres donnant le titre de la fenetre
               stockage, un dictionnaire construit comme tel : {entier : [question, reponse, fichier contenant la réponse], ...}
               taille, un entier qui est le nombre maximal de caracteres sur une ligne
               base, une chaine de caracteres avec le chemin d'accès vers la base de données
               root, optionnel, une fenêtre tkinter dans laquelle on doit afficher les questions
    renvoi une fenetre tkinter avec l'intégralité des questions recensées sous forme d'une liste de choix clickable ainsi que l'objet ListBox crée
    """

    def selection(event):
        """
        sous-fonction permettant d'afficher la réponse à la question selectionner
        parametres:
                   event, un évenement
        affiche une fenetre tkinter avec la reponse à la question choisit
        """
        indice = questions.curselection()[0] # on détermine l'indice de la question choisit
        question = questions.get(indice)
        numero = read.devine_numero(question)[0] # on détermine le numero de la question

        texte_entier = stockage[numero][0] + "\n\n" + stockage[numero][1] + "\n" + "-" * len(question) + "\n\n" + show.afficher_table(read.execute_sql_file("requetes", stockage[numero][2], base)) # On définit le texte à afficher dans la nouvelle fenetre en une seule ligne/chaine de caracteres
        affichage_texte_tkinter("Question " + str(numero) + " :", texte_entier, max([len(t) for t in texte_entier.split("\n")])) # On affiche la réponse dans une nouvelle fenetre tkinter

    # On définit une fenetre ainsi que son titre
    if root is None:
        root = Tk()

    root.title(titre)

    root.bind("<Double-Button-1>", selection) # On définit l'événement "double clic gauche" comme exécuteur de la fonction selection

    questions = Listbox(root, width = taille, height = 15) # On definit une liste qui contiendrat toutes les questions

    # On ajoute chaque questions stockées dans la liste dans l'ordre croissant
    ordre_questions = [t for t in stockage.keys()]
    ordre_questions = tris.tri_fusion(ordre_questions)

    i = 0
    while i < len(ordre_questions):
        questions.insert("end", stockage[ordre_questions[i]][0])
        i += 1

    # On affiche la fenetre tkinter et ce qu'elle contient
    questions.pack(side = "left")
    return root, questions

def clean(root, *elmt):
    """
    fonction permettant de vider une fenetre tkinter en excluant certains element
    parametres:
        root, le fenetre tkinter a 'nettoyer'
        elmt, les éléments de la fenetre que l'on ne doit pas enlever, fonctionne par type (tous les Canvas, ...)
    renvoi la fenetre vidé
    """
    for c in root.winfo_children():
        if c.winfo_class() not in elmt:
            c.destroy()
    return root

if __name__ == "__main__":
    affichage_texte_tkinter("test", "Bonjour\nCa va ?", 7)
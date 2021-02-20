# On importe les modules necessaires
from tkinter import Tk, Text, Listbox, Scrollbar

# l'importation de ces modules dépend de la façon dans est exécuté le fichier
try:
    import module_affichage as show
    import module_lecture_fichier as read
except:
    from modules import module_affichage as show
    from modules import module_lecture_fichier as read

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
    root.mainloop()

def affichage_question_tkinter(titre, stockage, taille):
    """
    fonction permettant d'afficher une série de questions ainsi que de gerer les réponses contenue dans un dictionnaire, le tout dans une fenetre tkinter
    parametres:
               titre, une chaine de caracteres donnant le titre de la fenetre
               stockage, un dictionnaire construit comme tel : {entier : [question, reponse, fichier contenant la réponse], ...}
               taille, un entier qui est le nombre maximal de caracteres sur une ligne
    affiche une fenetre tkinter avec l'intégralité des questions recensées
    """

    def selection(event):
        """
        sous-fonction permettant d'afficher la réponse à la question selectionner
        parametres:
                   event, un évenement
        affiche une fenetre tkinter avec la reponse à la question choisit
        """
        choix = questions.curselection()[0] +1 # on détermine le numéro de la question choisit
        texte_entier = stockage[choix][1] + "\n" + "-" * len(questions.get(choix-1)) + "\n\n" + show.afficher_table(read.execute_sql_file("requetes", stockage[choix][2], "imdb.db")) # On définit le texte à afficher dans la nouvelle fenetre en une seule ligne/chaine de caracteres
        affichage_texte_tkinter(stockage[choix][0], texte_entier, len(questions.get(choix-1))) # On affiche la réponse dans une nouvelle fenetre tkinter

    # On définit une nouvelle fenetre ainsi que son titre
    root = Tk()
    root.title(titre)

    root.bind("<Double-Button-1>", selection) # On définit l'événement "double clic gauche" comme exécuteur de la fonction selection

    questions = Listbox(root, width = taille, height = 15) # On definit une liste qui contiendrat toutes les question

    # On ajoute chaque questions stockées dans la liste
    for numero, question in stockage.items():
        questions.insert(numero, question[0])

    # On affiche la fenetre tkinter et ce qu'elle contient
    questions.pack()
    root.mainloop()

if __name__ == "__main__":
    affichage_texte_tkinter("test", "Bonjour\nCa va ?", 7)
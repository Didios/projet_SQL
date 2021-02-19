from tkinter import Tk, Text, Button, Scrollbar

def affichage_texte_tkinter(titre, texte, taille):
    """
    fonction permettant d'afficher un texte choisit dans une fenetre tkinter
    parametres:
               titre, une chaine de caracteres donnant le titre de la fenetre
               texte, une chaine de caracteres étant le texte à afficher
               taille, un entier qui est le nombre maximal de cracteres sur une ligne
    affiche une fenetre tkinter
    """
    root = Tk()
    root.title(titre)

    affiche = Text(root, width = taille + 10)
    scroll = Scrollbar(root, orient="vertical", command=affiche.yview)
    affiche.config(yscrollcommand=scroll.set)
    affiche.insert("insert", texte)

    scroll.pack(side="right", fill="y")
    affiche.pack(side="left")
    root.mainloop()

def affichage_question_tkinter(titre, stockage, taille):
    root = Tk()
    root.title(titre)

    for numero, question in stockage.items():
        print(numero)
        Button(root, text = question[0]).grid(column = 0, row = numero)

    root.mainloop()

########################################################################
#	imports
########################################################################
import tkinter
import os

def affichage(texte, titre = "Requêtes tables"):
	"""
	Affiche un texte (résultat d'une requête)
	dans une fenêtre tkinter
	Auteurs: M CHOUCHI
	Arguments:
		texte: str du texte à afficher
		titre: str du titre de la fenêtre
	Renvoi:
		rien
	"""
	root = tkinter.Tk()
	root.title(str(titre))
	RWidth=root.winfo_screenwidth() - 100
	RHeight=root.winfo_screenheight() - 100
	root.geometry("%dx%d+50+0"%(RWidth, RHeight))
	text=tkinter.Text(root, wrap = 'none')
	scroll_x=tkinter.Scrollbar(text.master, orient='horizontal', command = text.xview)
	scroll_x.config(command = text.xview)
	text.configure(xscrollcommand = scroll_x.set)
	scroll_x.pack(side = 'bottom', fill = 'x', anchor = 'w')
	scroll_y = tkinter.Scrollbar(text.master)
	scroll_y.config(command = text.yview)
	text.configure(yscrollcommand = scroll_y.set)
	scroll_y.pack(side = tkinter.RIGHT, fill = 'y')
	text.insert("1.0", texte)
	text.pack(side = tkinter.LEFT, expand = True, fill = tkinter.BOTH)
	root.mainloop()


if __name__ == "__main__":
    affichage_texte_tkinter("test", "Bonjour\nCa va ?", 7)
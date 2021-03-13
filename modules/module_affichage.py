#!"C:\Winpython\python-3.8.5.amd64\python.exe"

def taille_colonne(tableau):
    """
    fonction qui renvoie la taille minimale que doit avoir chaque colonne du tableau à afficher
    parametres:
               tableau, une liste de liste python
    renvoie une liste de valeur
    """
    longueur_colonne = [0] * len(tableau[0])

    for ligne in tableau:

        for column in range(len(ligne)):

            if len(str(ligne[column])) > longueur_colonne[column]:
                longueur_colonne[column] = len(str(ligne[column]))

    for i in range(len(longueur_colonne)):
        longueur_colonne[i] += 1

    return longueur_colonne

def separation(dimension):
    """
    fonction qui renvoie la representation d'un trait entre deux lignes d'un tableau
    parametres:
               dimension, une liste de valeur
    renvoie une chaine de caracteres correspondant à un ligne de séparation de l'affichage du tableau
    """
    ligne_separation = "+"

    for column in dimension:
        ligne_separation += "-" * column
        ligne_separation += "+"

    return ligne_separation

def afficher_ligne(ligne, dimension):
    """
    fonction qui permet d'obtenir l'affichage d'une ligne de tableau avec des dimensions données
    parametres:
               ligne, une liste
               dimension, une liste
    renvoie une chaine de caracteres contenant l'affichage de la ligne au format ascii
    """
    chaine = "|"

    for column in range(len(ligne)):
        chaine += str(ligne[column])
        chaine += " " * (dimension[column] - len(str(ligne[column])))
        chaine += "|"

    return chaine

def afficher_table(table, debut = 0, fin = None):
    """
    fonction qui permet d'obtenir l'affichage d'un tableau (réprésentant un tableau sql, avec la possibilité de choisir un intervalle de ligne à afficher
    parametres:
               table, une table sqlite3
               debut (optionnel), un nombre entier
               fin (optionnel), un nombre entier
    renvoie une chaine de caracteres contenant l'affichage de la partie du tableau souhaiter, par défaut son entièreté
    """
    if fin == None or fin > len(table):
        fin = len(table)
    if debut != 0:
        debut -= 1
    if debut < 1:
        debut = 0

    # On sélectionne les lignes du tableau que l'on va devoir afficher, pour éviter les tailles de colonne incohérentes
    table_afficher = []
    for ligne in range(debut, fin):
        table_afficher += [table[ligne]]

    dimension_colonne = taille_colonne(table_afficher)
    separation_ligne = separation(dimension_colonne)

    # On affiche les lignes choisis
    affichage_finale = separation_ligne + "\n"
    for ligne in table_afficher:
        affichage_finale += afficher_ligne(ligne, dimension_colonne) + "\n"
        affichage_finale += separation_ligne + "\n"
    return affichage_finale

def projection_table(table, *args):
    """
    fonction permettent de faire une projection sur un tableau sql
    parametres:
               table, une liste représentant un tableau sql
               args, une liste d'entier
    renvoie une liste avec les colonne selectionner
    """
    return [[ligne[column] for column in args] for ligne in tableau]

def produit_cartesien(table1, table2):
    """
    fonction permettant de faire le produit cartesien de 2 tables sql
    parametres:
               table1, une liste représentant un tableau sql
               table2, une liste représentant un tableau sql
    renvoie une liste
    """
    tableau = []
    for ligne1 in table1:
        for ligne2 in table2:
            tableau += [ligne1 + ligne2]
    return tableau


if __name__ == "__main__":
    import sqlite3
    conn = sqlite3.connect('imdb.db')
    c = conn.cursor()
    c.execute("SELECT * FROM title_basics")
    resultat = c.fetchall()
    print(afficher_table(resultat))
    conn.close()
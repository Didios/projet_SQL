# l'importation de ces modules dépend de la façon dans est exécuté le fichier
try:
    import module_affichage as show
    import module_lecture_fichier as read
    import module_tri as tris
except:
    from modules import module_affichage as show
    from modules import module_lecture_fichier as read
    from modules import module_tri as tris


def debuthtml(titre = ""):
    """
    fonction permettant de gérer le début d'un affichage dans une page web
    parametres:
        titre, optionnel, une chaine de caracteres qui définit le nom de la page web
    renvoi une chaine de caracteres avec le texte necessaire
    """
    print("Content-type: text/html")
    print("\n")
    print("<html><head>")
    print("\n" + titre + "\n")
    print("</head><body>")

def finhtml():
    """
    fonction permettant de gérer la fin d'un affichage dans une page web
    """
    print("</body></html>")

def tableau_html(tableau, debut = True, fin = True):
    """
    fonction permettant d'afficher un tableau dans une page web
    parametres:
        tableau, une liste dont chaque élément est une lsite avec avec le contenu d'une ligne du tableau
        debut, optionnel, un booléen indiquant si la page web doit être débuté, par défaut True
        fin, optionnel, un booléen indiquant si la page web doit être terminer, par défaut True
    renvoie une chaine de caracters avec l'impression necessaire
    """

    if debut:
        debuthtml()

    print("<style> table, th, td {border: 1px solid black;  padding: 5px; border-collapse: collapse;} </style> ")

    table = "<table>\n"

    for ligne in tableau:
        table += "<tr>\n"
        for colonne in ligne:
            table += "<td>" + str(colonne) + "</td>\n"
        table += "</tr>\n"
    table +="</table>\n"

    print(table)

    if fin:
        finhtml()


def texte_html(texte, debut = True, fin = True):
    """
    fonction permettant d'afficher un texte dans une page web
    parametres:
        texte, une chaine de caracteres à afficher
        debut, optionnel, un booléen indiquant si la page web doit être débuté, par défaut True
        fin, optionnel, un booléen indiquant si la page web doit être terminer, par défaut True
    renvoie une chaine de caracteres avec l'impression necessaires
    """
    if debut:
        debuthtml()

    print("<div style=\"width: 100%; font-size: 25px; font-weight: bold; text-align: center;\">")
    print(texte)
    print("</div>\n")

    if fin:
        finhtml()

def affichage_question_html(stockage, base):
    """
    fonction permettant d'afficher une série de questions ainsi que de gerer les réponses contenue dans un dictionnaire, le tout dans une fenetre tkinter
    parametres:
               stockage, un dictionnaire construit comme tel : {entier : [question, reponse, fichier contenant la réponse], ...}
               base, une chaine de caracteres avec le chemin d'accès vers la base de données
    renvoi une chaine de caracteres avec l'impression necessaires
    """

    # On ajoute chaque questions stockées dans la liste dans l'ordre croissant et on les tris par orde croissant
    ordre_questions = [t for t in stockage.keys()]
    ordre_questions = tris.tri_fusion(ordre_questions)

    for fichier in read.lister_fichier("modules/data"):
        read.suppr_fichier("modules/data/" + fichier, False)


    print("<br>")

    i = 10
    while i < len(ordre_questions):
        numero = ordre_questions[i]
        question = stockage[numero][0]

        def new_page():

            page = "<html><head>\n%s\n</head><body>" % question
            page += "\n<br><br>\n"

            requete = stockage[numero][1].split("\n")
            for ligne in requete:
                page += ligne
                page += "<br>"

            page += "-" * len(question) + "\n<br><br>\n"

            tableau_page = read.execute_sql_file("requetes", stockage[numero][2], base)
            page += "<style> table, th, td {border: 1px solid black;  padding: 5px; border-collapse: collapse;} </style>\n"

            table = "<table>\n"
            for ligne in tableau_page:
                table += "<tr>\n"
                for colonne in ligne:
                    table += "<td>" + str(colonne) + "</td>\n"
                table += "</tr>\n"
            table +="</table>\n"

            page += table
            page += "</body></html>"

            nom_page = str(ordre_questions[i]) + ".html"

            read.add_fichier("modules/data", nom_page, page)
            return "modules/data/" + nom_page

        lieu = new_page()
        # probleme à partir de numero = 9

        print('<a href="%s" target="_blank" title="%s">' % (lieu, lieu))
        print(question)
        print("</a>\n")
        print("<br>")

        i += 1
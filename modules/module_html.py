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
    renvoi une fenetre tkinter avec l'intégralité des questions recensées sous forme d'une liste de choix clickable ainsi que l'objet ListBox crée
    """

    def selection(question):
        """
        sous-fonction permettant d'afficher la réponse à la question selectionner
        parametres:
                   question, une chiane de cracteres avec la question cliquer
        affiche une fenetre tkinter avec la reponse à la question choisit
        """
        debuthtml()
        print("<p>" + question + "</p>")
        finhtml()
        numero = read.devine_numero(question)[0] # on détermine le numero de la question
        """
        texte_entier = stockage[numero][0] + "\n\n" + stockage[numero][1] + "\n" + "-" * len(question) + "\n\n" + show.afficher_table(read.execute_sql_file("requetes", stockage[numero][2], base)) # On définit le texte à afficher dans la nouvelle fenetre en une seule ligne/chaine de caracteres
        texte_html("Question " + str(numero) + " :\n", texte_entier)
        """
    # On ajoute chaque questions stockées dans la liste dans l'ordre croissant
    ordre_questions = [t for t in stockage.keys()]
    ordre_questions = tris.tri_fusion(ordre_questions)

    def test(bidule):
        debuthtml()
        print("<p>" + test + "</p>")
        finhtml()


    print("<select name='questions' size=" + str(len(stockage)) + ">\n") # On definit une liste qui contiendrat toutes les questions

    i = 0
    while i < len(ordre_questions):
        print('<option ondblclick="' + "print('bonjour, tu as double cliquer')" + '" value=' + "'" + str(i) + "'>")#'selection('" + stockage[ordre_questions[i]][0] + "')' value='" + str(i) + "'>")
        print(stockage[ordre_questions[i]][0])
        print("</option>\n")
        i += 1
    print("</select>")
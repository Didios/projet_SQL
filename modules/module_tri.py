#!"C:\Winpython\python-3.8.5.amd64\python.exe"

# module contenant différentes méthode de tris
# fait par Didier Mathias

def tri_bulles(T):
    """
    fonction permettant de trier un tableau de valeur avec le tri a bulles
    parametres:
        T un tableau de valeur a trier
    Renvoie le tableau trier
    """
    assert type(T) == list, "On ne trie que des tableaux/listes" #On verifie que T est une liste
    n = len(T)
    for i in range(n-1,0,-1):
        for j in range(i):
            if T[j] > T[j+1]:
                temp = T[j]
                T[j] = T[j+1]
                T[j+1] = temp
    return T # petite question, vous donneZ la complexité ? https://interstices.info/les-algorithmes-de-tri/

def tri_bulles_V2(T):
    """
    fonction permettant de trier un tableau de valeur avec le tri a bulles
    parametres:
        T un tableau de valeur a trier
    Renvoie le tableau de valeur trier
    """
    assert type(T) == list, "On ne trie que des tableaux/listes" #On verifie que T est une liste
    n = len(T)
    for i in range(n-1):
        t = n-i
        for j in range(t-1):
            if T[j] > T[j+1]:
                temp = T[j]
                T[j] = T[j+1]
                T[j+1] = temp
    return T

def tri_selection(T):
    """
    fonction permettant de trier un tableau de valeur avec le tri par selection
    parametres:
        T un tableau de valeur a trier
    Renvoie le tableau de valeur trier
    """
    def indice_min(T, dbt, fn):
        """
        sous-fonction permettant de trouver l'indice de la valeur minimale dans un tableau avec un intervalle donné
        a savoir que les deux valeurs délimitant l'intervalle sont comprises
        parametres:
            T un tableau de valeur
            dbt un entier indiquant le début de l'intervalle
            fn un entier indiquant la fin de l'intervalle
        Renvoie l'indice de la valeur minimum de l'intervalle
        """
        indice = dbt
        for i in range(dbt, fn):
            if T[i] < T[indice]:
                indice = i
        return indice

    assert type(T) == list, "On ne trie que des tableaux/listes" #On verifie que T est une liste
    for n in range(len(T) -1):
        mini = indice_min(T, n, len(T))
        temp = T[mini]
        T[mini] = T[n]
        T[n] = temp
    return T



def tri_insertion(T):
    """
    fonction permettant de trier un tableau de valeur avec le tri par insertion
    parametres:
        T un tableau de valeur a trier
    Renvoie le tableau de valeur trier
    """
    assert type(T) == list, "On ne trie que des tableaux/listes" #On verifie que T est une liste
    for i in range(1, len(T)):
        j = i - 1
        while j >= 0 and T[j] > T[j+1]:
            T[j], T[j+1] = T[j+1], T[j]
            j -= 1
    return T

def tri_fusion(T):
    """
    fonction permettant de trier un tableau de valeur avec le tri fusion
    parametres:
        T un tableau de valeur a trier
    Renvoie le tableau de valeur trier
    """
    def fusion(T1, T2):
        """
        sous-fonction permettant de fusionner 2 tableaux trier en un tableau trier
        parametres:
            T1 un tableau de valeur trié
            T2 un tableau de valeur trié
        Renvoie un tableau de valeur trié contenant T1 et T2
        """
        T = []
        while len(T1) != 0 and len(T2) != 0:
            if T1[0] < T2[0]:
                T += [T1[0]]
                T1 = T1[1:]
            else:
                T += [T2[0]]
                T2 = T2[1:]
        if len(T1) == 0:
            T += T2
        else:
            T += T1
        return T

    assert type(T) == list, "On ne trie que des tableaux/listes" #On verifie que T est une liste
    if len(T) < 2:
        return T
    else:
        m = len(T)//2
        T1 = tri_fusion(T[:m])
        T2 = tri_fusion(T[m:])
        T = fusion(T1, T2)
        return T

'''
Dans le tri rapide :

Pseudo-code
Voici le pseudo-code du tri rapide :

triRapide (début, fin) :
   Si le tableau a un seul élément
      Arrêter
   Sinon
      Choisir le pivot = ?
      Réorganiser le tableau selon notre pivot
      triRapide(début, pivot - 1)
      triRapide(pivot + 1, fin)

Le choix du pivot est essentiel.
Si, on regarde le pire des cas, on se rend compte du problème que pause cet algorithme. Si le tableau à trier est organisé de telle manière que, à chaque itération,
une des deux parties ne contient qu'un seul élement, alors sa complexité est polynomiale. Que l'on choisisse un pivot au milieu,
à la fin ou au début de la partie à traiter ne change rien : il existera toujours un cas pour lequel ce tri est particulièrement inefficace.

'''
def tri_rapide(T):
    """
    fonction permettant de trier un tableau de valeur avec le tri rapide
    parametres:
        T un tableau de valeur a trier
    Renvoie le tableau de valeur trier
    """
    assert type(T) == list, "On ne trie que des tableaux/listes" #On verifie que T est une liste
    if len(T) < 2:
        return T
    else:
        pivot = T[0]
        T_pivot = [pivot]
        while len(T) > 0:
            if T[0] < pivot:
                T_pivot = [T[0]] + T_pivot
            else:
                T_pivot = T_pivot + [T[0]]
            T = T[1:]
        pivot_indice = T_pivot.index(pivot)
        T1 = tri_rapide(T_pivot[:pivot_indice])
        T2 = tri_rapide(T_pivot[pivot_indice +1:])
        return T1 + T2



def test():
    """
    fonction de test des différents tris avec des test basiques
    """
    assert tri_bulles([9,8,7,6,5,4,3,2,1]) == [1,2,3,4,5,6,7,8,9], "Faux"
    assert tri_bulles([]) == [], "Faux"
    assert tri_bulles_V2([9,8,7,6,5,4,3,2,1]) == [1,2,3,4,5,6,7,8,9], "Faux"
    assert tri_bulles_V2([]) == [], "Faux"
    assert tri_bulles([3,6,7,54,1359,3,47,62,3]) == tri_bulles_V2([3,6,7,54,1359,3,47,62,3]), "Faux"

    assert tri_selection([9,8,7,6,5,4,3,2,1]) == [1,2,3,4,5,6,7,8,9], "Faux"
    assert tri_selection([]) == [], "Faux"

    assert tri_insertion([9,8,7,6,5,4,3,2,1]) == [1,2,3,4,5,6,7,8,9], "Faux"
    assert tri_insertion([]) == [], "Faux"

    assert tri_fusion([9,8,7,6,5,4,3,2,1]) == [1,2,3,4,5,6,7,8,9], "Faux"
    assert tri_fusion([]) == [], "Faux"

    assert tri_rapide([9,8,7,6,5,4,3,2,1]) == [1,2,3,4,5,6,7,8,9], "Faux"
    assert tri_rapide([]) == [], "Faux"

    print("Fonctionnel")


def test_aleatoire(longueur = False):
    """
    fonction de test des differents tri de manière aléatoire, que se soit le nombre de valeur ou les valeurs elle même
    parametres:
        longueur un parametres facultatif permettant de déterminer le nombre de valeur du tableau
    """
    from random import randint
    T = []

    if longueur == False:
        longueur = randint(0, 100) #Attention, le nombre maximum de récursion autorisé peut-être atteint
    else:
        assert type(longueur) == int, "la longueur du tableau doit être un nombre entier"
        assert longueur > -1, "la longueur d'un tableau doit être positive"

    print("Nombre de valeur : ",longueur)

    for i in range(longueur):
        T += [randint(-10000,10000)]

    T_bulles = T
    T_selection = T
    T_insertion = T
    T_fusion = T
    T_rapide = T

    T_bulles = tri_bulles(T_bulles)
    T_selection = tri_selection(T_selection)
    T_insertion = tri_insertion(T_insertion)
    T_fusion = tri_fusion(T_fusion)
    T_rapide = tri_rapide(T_rapide)

    assert T_bulles == T_selection, "Faux"
    assert T_bulles == T_insertion, "Faux"
    assert T_bulles == T_fusion, "Faux"
    assert T_bulles == T_rapide, "Faux"
    assert T_selection == T_insertion, "Faux"
    assert T_selection == T_fusion, "Faux"
    assert T_selection == T_rapide, "Faux"
    assert T_insertion == T_fusion, "Faux"
    assert T_insertion == T_rapide, "Faux"
    assert T_fusion == T_rapide, "Faux"

    print("Fonctionnel")
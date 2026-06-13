
import json # Cette importation nous permet d'utiliser les fonctionnalités liées au format JSON
import turtle # importation permettant d'utiliser le mode "Turtle"
from tkinter import * # ceci nous permet d'utiliser Tkinter



def lire_fichier(chemin_du_fichier):
    ''' Création d'une fonction qui lit le fichier personal.json et qui retourne les données de ce fichier'''
    with open(chemin_du_fichier, 'r', encoding='utf-8') as file: # ouverture du fichier avec l'option lecture avec la
        # codification "utf-8"
        personnes = json.load(file)  # assignation à la variable "personne" les données du fichier "personal.json
    return personnes


def construire_mapping(personnes):
    '''Création d'une fonction qui renvoie un dictionnaire avec comme clé les parents et leurs enfants sont les valeurs associées'''


    lire_fichier('personal.json')
    d = {} # création d'un dictionnaire vide

    for personnages in personnes: # Pour chaque personnage dans le dictionnaire "personnes" créé lors de l'étape précédente
        d[personnages['nom']] = personnages['enfants'] # on ajoute au dictionnaire vide, les parents comme clé et leurs enfants
        # comme valeurs
    return d


def tree(name, mapping, gen, family={}, depth={}):
    '''Création d'une fonction renvoyant un tuple qui, pour une personne donnée, donne le nombre total de descendants et
    la profondeur de l'arbre'''
    if name not in mapping or mapping[name] == []: # si le nom donné en paramètre n'est pas un parent ou si le parent
        # n'a pas d'enfants, elle ne continue pas le code
        pass

    else:

        for i in (mapping[name]): # pour chaque enfant du parent mis en paramètre, nous allons rajouter à l'ensemble
            # "family" le nom de l'enfant et nous allons rajouter à l'ensemble "génération" la génération de l'enfant
            family.add(i)
            depth.add(gen)
            tree(i, mapping, gen + 1, family, depth) # nous allons refaire la même fonction sauf que le nom de l'enfant
            # sera mis en paramètre et la génération sera augmentée de 1
            res = len(family), len(depth)
    return len(family), len(depth) # nous retournons le tuple, avec la premiere valeur nombre de descendants
                                   # et la 2éme valeur la génération


def all(d):
    '''Fonction créant une liste avec toutes les personnes présentes dans l'arbre généalogique '''

    ens = set()
    for i in d: # pour chaque parent dans le dictionnaire d
        for j in d[i]: # pour chaque enfant de chaque parent du dictionnaire d, nous ajoutons l'enfant dans l'ensemble vide
            ens.add(j)
        ens.add(i) # nous rajoutons également le parent dans l'ensemble vide
    return list(ens) # nous retournons la liste


def NEW_JSON_STRUCTURE(ens):
    ''' Cette fonction crée la Liste N_J_S qui contient des dictionnaires avec le nom de chaque
    # personne, le nombre de descendants et la génération, et crée également un fichier json. Cette fonction prend en
    paramètre la liste ens, créée lors de l'étape précédente.'''

    N_J_S = [dict()] * len(ens)  # création de liste ayant comme longueur len(ens) contenant des dictionnaires vides

    for name in ens: # pour chaque personne trouvée dans la liste précédente
        total_descendants, générations = tree(name, d, 1, set(), set()) # la fonction tree nous renvoie un tuple
        # composé du nombre total de descendants et du nombre de générations, nous allons donc assigner à la variable
        # ""total_descendants" le nombre total de descendants et à la variable génération la génération du personnage
        N_J_S[ens.index(name)] = {"name": name, "total_descendants": total_descendants, "generations": générations}

    with open('json_new_file.json', 'w', encoding='utf-8') as n_file:  # création du nouveau fichier json
        json.dump(N_J_S, n_file, indent=3)

    return N_J_S


def section_sort(N_J_S,paramètre):
    '''# Cette fonction triera la liste de personnes que nous avons créée lors de l'étape précédente'''
    n = len(N_J_S) # Nous assignons à la variable n la longueur de la liste N_J_S, c'est-à-dire le nombre de personnages
    # dans l'arbre.
    for i in range(n - 1): # nous allons parcourir la liste pour chaque entier situé entre 0 et n - 1 non compris
        max = i # nous assignons à la variable max la valeur de i
        for j in range(i + 1, n) : # pour chaque i , nous allons parcourir la liste par des éléments plus grands que i
            # et strictement plus petit que n
            if N_J_S[max][paramètre] < N_J_S[j][paramètre]: # si N_J_S[j][paramètre] est plus grand  que le max, j devient le max
                max = j
            elif N_J_S[max][paramètre] == N_J_S[j][paramètre]: # s'il y a égalité de valeurs
                if N_J_S[max]["name"] > N_J_S[j]["name"]: # sachant qu'il y a égalité, nous allons considérer l'ordre alphabétique
                    max = j # sachant que N_J_S[max]["name"] est plus grand que N_J_S[j]["name"], le maximum devient j

        if max != i: # si le maximum "final" est différent du maximum initial, nous allons permuter les valeurs
            N_J_S[i], N_J_S[max] = N_J_S[max], N_J_S[i] # permutation des valeurs


def etape_4(d_w, star):
    ''' Création d'une fonction qui va créer un dictionnaire trié avec des tuples comportant le nom de
     la personne et la génération. d_w est le dictionnaire trié contenant le nom, le nombre total de descendants et la
    génération et "star" est le dictionnaire associant chaque parent et ses enfants '''

    slov_i = {} # création d'un dictionnaire vide

    p = d_w[0]['generations'] # assignation à la valeur p la valeur de la génération maximale
    for i in d_w: # nous allons parcourir chaque élément du dictionnaire
        slov_i[i['name']] = i['generations']  # dictionnaire trié contenant le nom de la personne comme clé et sa
        # génération comme valeur

    for parent in slov_i.keys(): # pour chaque parent du dictionnaire slov_i
        if parent in star.keys():  # si la personne est un parent
            maxx = slov_i[parent] - 1 # nous assignons à la valeur maxx la génération du parent - 1
            f = True   # on suppose que la génération de ce parent est la plus grande
            # si la personne a des enfants, on regarde ses enfants, et cherche le maximum parmi
            # la generation du (parent - 1) et de ses enfants
            for children in star[parent]: # nous allons parcourir chaque enfant si les parents ont des enfants
                if slov_i[children] > maxx: # nous cherchons le maximum entre la génération de l'enfant et la génération
                                            # du parent diminué de 1
                    maxx = slov_i[children]  # maxx devient la génération du plus vieil enfant
                    f = False
            if f == False : # si la génération de l'enfant est plus grande que celle de ses parents
                slov_i[parent] = maxx + 1 # la génération du parent est celle de son enfant augmenté de 1
                for children in star[parent]:  #la génération de chaque enfant est la génération maximale entre eux
                    slov_i[children] = maxx
            else:  # si la génération de l'enfant est plus petite que celle de son parent -1
                for children in star[parent]:#  la génération de chaque enfant de ce parent sera celle de son parent diminué de 1
                    slov_i[children] = maxx

    for i in slov_i.keys(): # Nous allons inverser l'étage de chaque personne pour que la répresentation soit plus simple
        slov_i[i] = p - slov_i[i]  # pour inverser les étages, nous allons soustraire la génération actuelle
                                   # de la génération maximale


    slov_f = sorted(slov_i.items(), key=lambda x: x[1])  # Nous allons trier par étage ( du maximum au minimum)

    return slov_f # nous retournons slov_f, une liste qui contient les tuples(personne, son étage).
                  #Cette liste est triée de l'etage 0 jsuqu'au dernier étage





def matrixx(maxx, slov_f):
    '''création d'une fonction qui crée une matrice et qui prend pour paramètre la valeur maximale
    trouvée lors de l'étape précédente et slov_f'''
    matrix = [''] * (maxx + 1) # création d'une matrice ayant pour longueur la valeur maxx + 1
    for i in range(maxx + 1) : # pour chaque valeur de i situé entre 0 et la valeur maxx + 1 non comprise
        matrix[i] = [name for name, number in slov_f if number == i] # les personnes ayant la même génération seront situés
        # sur la même ligne
    return matrix # nous retournons la matrice


def command1():
    '''Fonction qui dessine un arbre'''
    turtle.speed(200)
    turtle.clear() # afin que les images ne s'interposent pas
    turtle.ht() # afin de cacher la tortue

    x0 = -200  # nous définissons les coordonnées et les pas selon x et selon y de départ
    y0 = 200
    pasx = 70
    pasy = 50
    y = y0
    turtle.penup() # relève le stylo de la tortue
    # affichage de tous les noms selon son étage
    for i in range(slov_f[-1][1] + 1):  # boucle selon les étages
        x = x0
        turtle.goto(x, y)   #turtle arrive sur la position initiale de chaque nom tout à gauche et se déplace vers la droite
        for j in range(len(matrix[i])):  # affichage des noms qui correspondent au même étage à la même ligne
            turtle.write(matrix[i][j], move=True) # écriture des personnages
            x = x + pasx  # décalage horizontal entre les noms
            turtle.goto(x, y)

        y -= pasy  # passage à l'étage suivant(en bas)

    # affichage des segments - liens
    for parent in d.keys():  # pour chaque parent présent dans le dictionnaire d
        # on cherche le parent dans la matrice et fixons sa position - le point de depart de turtle(x1, y1)
        for i in range(len(matrix)): # pour chaque valeur comprise entre 0 et la longueur de la matrice, à savoir 5 nom compris
            for j in range(len(matrix[i])): # pour un i donné, considérer chaque j entre 0 et la longueur de la matrix[i] non compris
                if parent == matrix[i][j]: # si le parent est égal à matrix[i][j]
                    x1 = x0 + pasx * j + 5
                    y1 = y0 - pasy * i - 2

        # pour ce parent, nous regardons ses enfants dans le dict.values()
        for child in d[parent]:
            # pour chaque enfant, nous cherchons sa position dans la matrice et la fixons - le final du lien(x2, y2)
            for i1 in range(len(matrix)): # pour chaque valeur comprise entre 0 et la longueur de la matrice, à savoir 5 non compris
                for j1 in range(len(matrix[i1])): #  pour un i donné, considérer chaque j entre 0 et la longueur de la matrix[i] non compris
                    if child == matrix[i1][j1]: # si l'enfant est égal à matrix[i1][j1]
                        x2 = x0 + pasx * j1 + 5
                        y2 = y0 - pasy * i1 + 15
                        turtle.goto(x1, y1)  # affichage du segment du (x1, y1) jusqu'à (x2, y2)
                        turtle.pendown() # nous abaissons le stylo de la tortue
                        turtle.goto(x2, y2)
                        turtle.penup() # nous relevons le stylo

    turtle.done()


def commande2():
    ''' Fonction responsable de l'affichage des phrases triées en fonction du nombre de descendants'''
    turtle.speed(200)
    turtle.clear() # afin que les images ne s'interposent pas
    turtle.ht() # afin de cacher la tortue
    a = -200  # coordonnée initiale de y là où sera imprimée la phrase
    b = 400
    #(a,b) correspondent aux coordonnées (x,y) sur le plan oordoné
    section_sort(N_J_S, "total_descendants") # on trie la liste N_J_S, et puis on imprime dans l'ordre demandé,
    # en fonction du tri qui a été fait
    for i in N_J_S: # on imprime chaque phrase
        turtle.penup()
        turtle.goto(a, b)
        turtle.pendown()
        turtle.write(str(i["name"]) + " a " + str(i['total_descendants']) + " descendants " + " sur " + str(
            i["generations"]) + " generations ")
        b -= 40 #passage en bas

def commande3():
    ''' Fonction responsable de l'affichage des phrases triées en fonction du nombre de générations, la même chose que la
    fonction commande2, mais qui affiche selon le nombre de générations '''
    turtle.speed(200)
    turtle.clear() # afin que les images ne s'interposent pas
    turtle.ht() # afin de cacher la tortue

    section_sort(N_J_S, "generations") # Nous trions la liste N_J_S par générations
    a = -200 # coordonnée initiale de y là où sera imprimée la phrase
    b = 400
    for i in N_J_S: # on imprime chaque phrase
        turtle.penup()
        turtle.goto(a,b)
        turtle.pendown()
        turtle.write(str(i["name"]) + " a " + str(i['total_descendants']) + " descendants " + " sur " + str(i["generations"]) + " generations ")
        b -= 40



# ***************************************************************************************************************************************************************************
# MAIN PROGRAM#MAIN PROGRAM#MAIN PROGRAM#MAIN PROGRAM#MAIN PROGRAM#MAIN PROGRAM#MAIN PROGRAM#MAIN PROGRAM#MAIN PROGRAM#MAIN PROGRAM#MAIN PROGRAM#
# ***************************************************************************************************************************************************************************
if __name__ == '__main__':

    d = construire_mapping(lire_fichier("personal.json"))  # dictionary with a parent associated to a list with his children

    ens = all(d)  # liste  avec toutes les personnes présentes dans JSON DEAFAULT FILE

    N_J_S = NEW_JSON_STRUCTURE(ens) #cette fonction crée la Liste N_J_S qui contient des dictionnaires avec le nom de chaque
    # personne, le nombre de descendants et la génération(ETAPE 2)

    section_sort(N_J_S,'generations')  ### Snous trions la liste N_J_S, nous pouvons également mettre
    # "total_descendants" si nous voulons le tri par descendance

    slov_f = etape_4(N_J_S,d)  ### ETAPE 4, assignation à la variable slov_f la liste finale triée de l'étape 4, avec les
    # personnes et leur échelle

    maxx = slov_f[-1][1]  # l'étage maximal parmi slov_f

    matrix = matrixx(maxx, slov_f)  # matrice finale qui contiens tout les noms avec leur index correspondant au leur étage dans l'arbre


    #on lie le module turtle et tkinter, puur que la tortue puisse dessiner dans la fenêtre turtle
    canvas = turtle.Screen().getcanvas()


    #création de 3 boutons avec leur fonction respectives
    button_1 = Button(canvas.master, text="arbre", command=command1)
    button_2 = Button(canvas.master, text="Tri par descendant", command=commande2)
    button_3 = Button(canvas.master, text="Tri par génération", command=commande3)

    # nous plaçons les boutons sur certaines coordonnées
    button_1.place(x=440, y=750, width=120, height=80)
    button_2.place(x=730, y=750, width=120, height=80)
    button_3.place(x=1000, y=750, width=120, height=80)


    turtle.mainloop()

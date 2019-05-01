
# coding=utf-8
import pygame
import os
import traceback
from random import randrange as randr
from pygame.locals import *

pygame.init()

def exceptonormal():
    """fonction exécutée dans move
    celle-ci permet de convertir les chiffre multiples de 2+1 en multiples de 2
    une fois toutes les case déplacées"""
    for i in range(5):
        for k in range(5):
            if tab[i][k] in exceptions:
                tab[i][k] = tab[i][k] - 1
    return


def move(deway):
    """fonction qui effectue le déplacement et la combinaisons des cases dans le sens demandé
    on utilise deux boucles for avec d'autres boucles imbriquées,on vérifie la variable deway
    afin de choisir les bonne varible et la bonne boucle, elle renvoie la variable mouvement 
    qui indicque si au moins une case à été déplacer"""
    mouvement = 0 # on initialise la variable qui informe si une case a bougée 
    if deway == "down" or deway =="right":
        a1 = 3 # valeur utilisée dans les boucles for qui suivent
        a2 = -1 # elle varie en fonction de la manière dont on veut parcourir 
        # le tableau
        a3 = -1 
        b = 1
    else:
        a1 = 1
        a2 = 5
        a3 = 1
        b = -1
    if deway == "down" or deway == "up":
        for passage in range(4): #tableau de 5*5 donc 5 passage
            for i in range(a1,a2,a3): # minimum, maximum, pas
                for k in range(5):
                    if tab[i + b][k] == tab[i][k] and tab[i][k] not in exceptions and tab[i][k] != 0:
                        tab[i + b][k] = 2 * tab[i][k] + 1
                        # on fais fois deux pour combiner les cases, puis on rajoute 1 afin de ne pas
                        # fusionne deux fois une case lors d'un passage
                        tab[i][k] = 0
                        mouvement = 1 #un mouvement a été effectué, mouvement est donc vrai
                    if tab[i + b][k] == 0 and tab[i][k] !=0:
                        tab[i + b][k] = tab[i][k]
                        tab[i][k] = 0
                        mouvement = 1
        exceptonormal()  #on retire les 1 ajoutés précedemment
        return mouvement
    else:
        for passage in range(4):
            for k in range(a1,a2,a3):
                for i in range(5):
                    if tab[i][k + b] == tab[i][k] and tab[i][k] not in exceptions and tab[i][k] != 0:
                        tab[i][k + b] = 2 * tab[i][k] + 1  # on fait fois deux pour combiner les cases
                        tab[i][k] = 0
                        mouvement = 1
                    if tab[i][k + b] == 0 and tab[i][k] !=0:
                        tab[i][k + b] = tab[i][k]
                        tab[i][k] = 0
                        mouvement =1
        exceptonormal()
        return mouvement


def images_load():
    """Charge les images et les stocke dans un dictionnaire qu'elle renvoie"""
    image_dict_temp = {}  # Dictionnaire vide qui contiendra les images
    for filename in os.listdir("pictures"):  # Parcours tous les fichiers du dossier "pictures"
        if filename.endswith(".png"):  # si le fichier est un .png, entre dans la boucle
            path = os.path.join("pictures", filename) # Récupère le chemain d'accès au fichier et le stocke dans path
            key = filename[:-4]  # Créée une clé pour accéder à l'élément dans le dictionnaire en prenant le nom du
            # fichier et en enlevant l'extension (-4 caractères)
            image_dict_temp[key] = pygame.image.load(path).convert_alpha() # on stocke l'image donnée dans le dictionnaire
    return image_dict_temp

def vic_def(mouvement):
    """Cette fonction va récuperer la varible mouvement qui informe si un mouvement de case a été effectué,
    si aucun mouvement à été effectué et que le tableau est plein dans ce cas c'est la défaite
    si lorsque qu'on compte les cases du tableau on détecte un 2048, c'est la victoire. """
    number_cases = 0 #on initialise la variable qui compte les cases pleines
    for x in range(5): #on parcours le tableau afin de comter le nombre de cases
        for y in range(5):
            if tab[x][y] != 0:
                number_cases = number_cases + 1
	    if tab[x][y] == 2048: #si un 2048 est présent victoire
		return 1 #on retourne donc 1
    if number_cases == 25 and mouvement == 0: #si aucun mouvement n'a été effectué et que le tableau est plein
	return 2 #on renvoie 2
    return 0 #sinon 0

def random_case():
    """Place une case (2 ou 4 au hazard avec 2 ayant une probabilité de 0.75 et 4 de 0.25) dans TAB à une position aléatoire"""
    number = randr(0, 4)  # Choisit un nombre au hasard afin de déterminer si un 2 ou un 4 apparait
    number_x, number_y = randr(0, 5), randr(0, 5)  # Choisit les coordonnées dans le tableau au hasard
    if tab[number_x][number_y] == 0:  # Vérifie si la case est vide
        if number == 0:  # if et elif servent ici à déterminer 2 ou 4 à partir de la valeur aléatoire
            number = 4
        else:
            number = 2
    else:
        random_case()
        return
    tab[number_x][number_y] = number  # Entre la valeur déterminée au hasard dans une case vide
    return # Condition pour continuer = Ne pas perdre


def affichage():
    """Fonction qui lis le tableau(tab) ,afin d'associer a chaque nombre son image 
    correspondante et l'affiche, de plus elle gère le score"""
    score = 0 #on initialise le score
    fenetre.blit(image_dict.get("interface"), (0, 0))  # Affiche la grille de jeu
    for x in range(0, 5):  # boucle qui parcours le tableau
        for y in range(0, 5):
            score = score + tab[x][y] # le socre équivaut à la somme de toutes les cases
            if tab[x][y] != 0:
                dispcoord = coords(x, y)  # Stocke dans la variable dispcoord l'equivalent en coordonnées dans le plan à partir des coordonnées dans le tableau
                key = "case" + str(tab[x][y])  # "Créée" le nom de l'objet à afficher
                fenetre.blit(image_dict.get(key), dispcoord)  # Affiche l'objet
    print(score)
    font = pygame.font.Font('comic.ttf', 40) #on définit la police et la taille
    text_score = font.render(str(score), True, (0, 0, 0)) #crée un l'objet text_score qui contient le score sous forme d'image
    fenetre.blit(text_score, (762, 77)) #on affiche le score
    pygame.display.flip()  # Rafraichit l'écran
    return 



def coords(y, x):
    """Associe les coordonnées dans le plan à partir des coordonnées du tableau"""
    return  (461+71*x, 181+71*y) # 461 et 181 sont les coordonnées de la première case, le delta entre les coordonnées
    # pour la case suivante est de 71, on ajoute donc x et y fois 71 afin d'avoir les coordonnées de la case souhaitée


try:
    ResX = 1280  # Resolution écran horizontale
    ResY = 720  # Resolution écran verticale
    pygame.font.init()
    exceptions = [1, 3, 5, 9, 17, 33, 65, 129, 257, 513, 1025, 2049]
    # liste qui contient les exceptions pour les mouvements
    cons = [0] * 5  # Création du tableau contenant les cases
    tab = [0] * 5
    for i in range(5):
        tab[i] = list(cons)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "50, 50"
    fenetre = pygame.display.set_mode((ResX, ResY))
    continuer = 1
    pygame.key.set_repeat(400, 30)
    image_dict = images_load()  # Fonction qui charge toutes les images
    #elle est utilisée dans la fonction random_case
    affichage()
    for g in range(5): # debug
        print(tab[g])  # debug
    while continuer: # boucle while principale
        for event in pygame.event.get(): 
            if event.type == QUIT:
                continuer = 0
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                   mouvement = move("down") #on demande de tenter de déplacer les case vers le bas, si au moins une case bouge mouvement = 1
                elif event.key == K_UP:
                   mouvement = move("up")
                elif event.key == K_LEFT:
                   mouvement = move("left")
                elif event.key == K_RIGHT:
                   mouvement = move("right")
                elif event.key == K_RETURN and victoireoudefaite == 2: # en cas de défaite et d'appuie sur entrer
                   for i in range(5): #on réinitialise le tableau
                       tab[i] = list(cons)
            if event.type == KEYUP:
                if event.key == K_LEFT or K_RIGHT or K_UP or K_DOWN:
                    victoireoudefaite = vic_def(mouvement) # on vérifie la victoire ou défaite 
                    if victoireoudefaite == 1: # si vitoire
                        print("c'est gagné")
                        random_case() #crée une case aléatoire
                        affichage() 
                    elif victoireoudefaite == 2: # si défaite
                        print("c'est perdu")
                        fenetre.blit(image_dict.get("defaite"), (0,0)) # Affiche le menu de défaite
                        pygame.display.flip()
                    elif victoireoudefaite == 0: #si ni victoire ou défaite
                        random_case() #crée une case aléatoire
                        affichage() 



except:
    traceback.print_exc()


finally:
    pygame.quit()
    exit()

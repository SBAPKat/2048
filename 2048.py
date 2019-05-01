
# coding=utf-8
import pygame
import os
import traceback
from random import randrange as randr
from pygame.locals import *

pygame.init()

def exceptonormal():
    """fonction exécutée dans move
    celle-ci permet de convertir les chiffres multiples de 2+1 en multiples de 2
    une fois toutes les cases déplacées"""
    for i in range(5):
        for k in range(5):
            if tab[i][k] in exceptions: # on vérifie si la case parcourue contient un nombre impair
                tab[i][k] = tab[i][k] - 1 #si oui on retire 1
    return


def move(deway):
    """fonction qui gere le deplacement, deway est la variable contenant le sens voulu, les variables i et k sont respectivement les lignes
    et les colones du tableau, afin de verifier si l'on a perdu, on renvoie la variable mouvement qui indique s'il y a au moins une case à bouger"""
    mouvement = 0 # on initialise la variable qui informe si une case a bougé
    if deway == "down" or deway =="right":
        borneinf = 3 # valeur utilisée dans les boucles for qui suivent
        bornesup = -1 # elle varie en fonction de la manière dont on veut parcourir
        # le tableau
        pas = -1
        sens = 1 # Varie en fonction du sens de lecture : tab[i][k] est la case déplacée
        # tab[i+sens][k] ou  tab[i][k+sens] est la case sur laquelle tab[i][k] va se déplacer.
    else:
        borneinf = 1
        bornesup = 5
        pas = 1
        sens = -1
    if deway == "down" or deway == "up":
        for passage in range(4): # Pour qu'une case parcourt tout le tableau, elle doit se déplacer de 4 cases 
            for i in range(borneinf,bornesup,pas): # minimum, maximum, pas, on lit le  tableau  ligne par ligne
                for k in range(5):
                    if tab[i + sens][k] == tab[i][k] and tab[i][k] not in exceptions and tab[i][k] != 0: # si la case adjacente est la case à déplacer sont identiques
                        # et qu'elles n'ont pas deja été fusionées (non impair) 
                        tab[i + sens][k] = 2 * tab[i][k] + 1 
                        # on fait fois deux pour combiner les cases, puis on rajoute 1 afin de ne pas
                        # fusionner deux fois une case lors d'un passage
                        tab[i][k] = 0 #L'ancienne position de la case est donc = à 0
                        mouvement = 1 #un mouvement a été effectué, mouvement est donc vrai
                    if tab[i + sens][k] == 0 and tab[i][k] !=0:
                        tab[i + sens][k] = tab[i][k]
                        tab[i][k] = 0
                        mouvement = 1
        exceptonormal()  # on retire les 1 ajoutés précedemment
        return mouvement
    else:
        for passage in range(4):
            for k in range(borneinf,bornesup,pas): # on lit le tableau colones par colones
                for i in range(5):
                    if tab[i][k + sens] == tab[i][k] and tab[i][k] not in exceptions and tab[i][k] != 0:
                        tab[i][k + sens] = 2 * tab[i][k] + 1  # on fait fois deux pour combiner les cases
                        tab[i][k] = 0
                        mouvement = 1
                    if tab[i][k + sens] == 0 and tab[i][k] !=0:
                        tab[i][k + sens] = tab[i][k]
                        tab[i][k] = 0
                        mouvement =1
        exceptonormal()
        return mouvement

def images_load():
    """Charge les images et les stocke dans un dictionnaire qu'elle renvoie"""
    image_dict_temp = {}  # Dictionnaire vide qui contiendra les images
    for filename in os.listdir("pictures"):  # Parcours tous les fichiers du dossier "pictures"
        if filename.endswith(".png"):  # si le fichier est un .png, entre dans la boucle
            path = os.path.join("pictures", filename) # Récupère le chemin d'accès au fichier et le stocke dans path
            key = filename[:-4]  # Crée une clé pour accéder à l'élément dans le dictionnaire en prenant le nom du
            # fichier et en enlevant l'extension (-4 caractères)
            image_dict_temp[key] = pygame.image.load(path).convert_alpha() # on stocke l'image donnée dans le dictionnaire
    return image_dict_temp

def vic_def(mouvement):
    """Cette fonction va récupérer la variable mouvement qui informe si un mouvement de case a été effectué,
    si aucun mouvement à été effectué et que le tableau est plein dans ce cas c'est la défaite
    si lorsque qu'on compte les cases du tableau on détecte un 2048, c'est la victoire. """
    number_cases = 0 # on initialise la variable qui compte les cases pleines
    for x in range(5): # on parcourt le tableau afin de compter le nombre de cases
        for y in range(5):
            if tab[x][y] != 0:
                number_cases = number_cases + 1
        if tab[x][y] == 2048: # si un 2048 est présent victoire
            return 1 # on retourne donc 1
    if number_cases == 25 and mouvement == 0: # si aucun mouvement n'a été effectué et que le tableau est plein
            return 2 # on renvoie 2
            if tab[x][y] == 2048: # si un 2048 est présent victoire
                return 1 # on retourne donc 1
    if number_cases == 25 and mouvement == 0: # si aucun mouvement n'a été effectué et que le tableau est plein
        return 2 # on renvoie 2
    return 0 # sinon 0

def random_case(score):
    """Place une case (2 ou 4 au hasard avec 2 ayant une probabilité de 0.75 et 4 de 0.25) dans TAB à une position aléatoire"""
    number = randr(0, 4)  # Choisit un nombre au hasard afin de déterminer si un 2 ou un 4 apparait
    number_x, number_y = randr(0, 5), randr(0, 5)  # Choisit les coordonnées dans le tableau au hasard
    if tab[number_x][number_y] == 0:  # Vérifie si la case est vide
        if number == 0:  # if et else servent ici à déterminer 2 ou 4 à partir de la valeur aléatoire
            number = 4
            score = score + 4
        else:
            number = 2
            score = score + 2
    else:
        score = random_case(score)
        return score
    tab[number_x][number_y] = number  # Entre la valeur déterminée au hasard dans une case vide
    return score # Condition pour continuer = Ne pas perdre


def affichage(score):
    """Fonction qui lit le tableau(tab) ,afin d'associer à chaque nombre son image
    correspondante et l'affiche, de plus elle gere le score"""
    fenetre.blit(image_dict.get("interface"), (0, 0))  # Affiche la grille de jeu
    for x in range(0, 5):  # boucle qui parcourt le tableau
        for y in range(0, 5):
            if tab[x][y] != 0:
                dispcoord = coords(x, y)  # Stocke dans la variable dispcoord l'equivalent en coordonnées dans le plan à partir des coordonnées dans le tableau
                key = "case" + str(tab[x][y])  # "Crée le nom de l'objet à afficher
                fenetre.blit(image_dict.get(key), dispcoord)  # Affiche l'objet
    print(score)
    text_score = font.render(str(score), True, (0, 0, 0))
    fenetre.blit(text_score, (762, 77)) # on affiche le score
    pygame.display.flip()  # Rafraichit l'écran
    return



def coords(y, x):
    """Associe les coordonnées dans le plan à partir des coordonnées du tableau"""
    return  (461+71*x, 181+71*y) # 461 et 181 sont les coordonnées de la première case, le delta entre les coordonnées
    # pour la case suivante est de 71, on ajoute donc x et y fois 71 afin d'avoir les coordonnées de la case souhaitée


try:
    ResX = 1280  # Résolution écran horizontale
    ResY = 720  # Résolution écran verticale
    pygame.font.init()
    font = pygame.font.Font('comic.ttf', 40) #on définit la police et la taille
    score = 0 #on initialise le score
    exceptions = [1, 3, 5, 9, 17, 33, 65, 129, 257, 513, 1025, 2049]
    # liste qui contient les exceptions pour les mouvements
    # elle est utilisée dans la fonction move
    cons = [0] * 5  # Création du tableau contenant les cases
    tab = [0] * 5
    for i in range(5):
        tab[i] = list(cons)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "50, 50"
    fenetre = pygame.display.set_mode((ResX, ResY))
    continuer = 1
    pygame.key.set_repeat(400, 30)
    image_dict = images_load()  # Fonction qui charge toutes les images
    # elle est utilisée dans la fonction random_case
    affichage(score)
    for g in range(5): # debug
        print(tab[g])  # debug
    while continuer: # boucle while principale
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                   mouvement = move("down") # on demande de tenter de déplacer les cases vers le bas, si au moins une case bouge mouvement =1
                elif event.key == K_UP:
                   mouvement = move("up")
                elif event.key == K_LEFT:
                   mouvement = move("left")
                elif event.key == K_RIGHT:
                   mouvement = move("right")
                elif event.key == K_RETURN and victoireoudefaite == 2: # en cas de défaite et d'appui sur entrer
                   for i in range(5): # on réinitialise le tableau
                       tab[i] = list(cons)
                       score = 0 # et le score
            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN or event.key == K_RETURN:
                    victoireoudefaite = vic_def(mouvement) # on vérifie la victoire ou défaite
                    if victoireoudefaite == 1: # si victoire
                        print("c'est gagné")
                        score = random_case(score) # créée une case aléatoire
                        affichage(score)
                    elif victoireoudefaite == 2: # si défaite
                        print("c'est perdu")
                        fenetre.blit(image_dict.get("defaite"), (0,0)) # Affiche le menu de défaite
                        pygame.display.flip()
                    elif victoireoudefaite == 0: # si ni victoire ou défaite
                        score = random_case(score) # crée une case aléatoire
                        affichage(score)



except:
    traceback.print_exc()


finally:
    pygame.quit()
    exit()

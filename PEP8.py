
# encoding=utf-8
import pygame
import os
import traceback
from PIL import Image, ImageDraw, ImageFont
from random import randrange as randr
from pygame.locals import *
import time

pygame.init()


def imagegen(case_title):
    case_content = ''
    for character in case_title:
        if character not in 'case':
            case_content = case_content + character
    # ouvre image "default"
    default = Image.open(os.path.join('pictures', 'default.png'))
    # créée une image vide avec channels rouge bleu vert et transparence,
    # de la taille de default, fond transparent
    txt = Image.new('RGBA', default.size, (255, 255, 255, 0))
    # Récupère la police, et le règle sur la taille voulue
    fnt = ImageFont.truetype('comic.ttf', 20)
    d = ImageDraw.Draw(txt)  # Récupère le contexte de dessin de l'image txt
    # Écrit le numéro de la case sur le contexte de dessin, en gris clair
    d.text((0, 20), case_content, font=fnt, fill=(200, 200, 200, 255))
    # Calque l'image txt sur l'image default
    output = Image.alpha_composite(default, txt)
    case_title = os.path.join('pictures', case_title)+'.png'
    # Sauvegarde l'image sous l'arborescence créée précedemment
    output.save(case_title)


def exceptonormal():
    """fonction exécutée dans move
    celle-ci permet de convertir les chiffres multiples de 2+1 en multiples de 2
    une fois toutes les cases déplacées"""
    for x in range(5):
        for y in range(5):
            if tab[x][y] % 2 == 1:  # On vérifie si la case parcourue contient un nombre impair
                tab[x][y] = tab[x][y] - 1  # Si oui on retire 1
    return


def move(deway):
    """fonction qui gere le deplacement, deway est la variable contenant le sens voulu,
    les variables x et y sont respectivementles lignes et les colones du tableau"""
    global number_case  # Pour pouvoir modifier globalement number_case on doit la définir
    # en temps que variable gobale
    if deway == "down" or deway == "right":
        borninf = 3  # Valeur utilisée dans les boucles for qui suivent
        bornsup = -1  # Elle varie en fonction de la manière dont on veut parcourir
        # le tableau
        step = -1
        # Varie en fonction du sens de lecture : tab[x][y] est la case déplacée
        direction = 1
        # tab[x+direction][y] ou  tab[x][y+direction] est la case sur laquelle tab[x][y] va se déplacer.
    else:
        borninf = 1
        bornsup = 5
        step = 1
        direction = -1
    if deway == "down" or deway == "up":
        # Pour qu'une case parcourt tout le tableau, elle doit se déplacer de 4 cases
        for passage in range(4):
            # Minimum, maximum, pas, on lit le  tableau  ligne par ligne
            for x in range(borninf, bornsup, step):
                for y in range(5):
                    # Si la case adjacente et la case
                    # à déplacer sont identiques et qu'elles n'ont pas deja été fusionées (nombre impair)
                    if tab[x + direction][y] == tab[x][y] and tab[x][y] % 2 == 0 and tab[x][y] != 0:
                        tab[x + direction][y] = 2 * tab[x][y] + 1
                        # on fait fois deux pour combiner les cases, puis on rajoute 1 afin de ne pas
                        # fusionner deux fois une case lors d'un passage
                        # L'ancienne position de la case est donc = à 0
                        tab[x][y] = 0
                        number_case -= 1  # Deux cases ont fusioné, on retire une case du compteur
                    # la case adjacente est vide et la case à déplacer ne l'est pas
                    if tab[x + direction][y] == 0 and tab[x][y] != 0:
                        # On place donc la case à déplacer à la place de la case adjacente
                        tab[x + direction][y] = tab[x][y]
                        tab[x][y] = 0  # L'ancienne posotion vaut donc 0
        exceptonormal()  # On retire les 1 ajoutés précedemment
        return
    else:
        for passage in range(4):
            # On lit le tableau colones par colones
            for y in range(borninf, bornsup, step):
                for x in range(5):
                    if tab[x][y + direction] == tab[x][y] and tab[x][y] % 2 == 0 and tab[x][y] != 0:
                        # On fait fois deux pour combiner les cases
                        tab[x][y + direction] = 2 * tab[x][y] + 1
                        tab[x][y] = 0
                        number_case -= 1
                    if tab[x][y + direction] == 0 and tab[x][y] != 0:
                        tab[x][y + direction] = tab[x][y]
                        tab[x][y] = 0
        exceptonormal()
        return


def images_load():
    """Charge les images et les stocke dans un dictionnaire qu'elle renvoie"""
    image_dict_temp = {}  # Dictionnaire vide qui contiendra les images
    # Parcours tous les fichiers du dossier "pictures"
    for filename in os.listdir("pictures"):
        if filename.endswith(".png"):  # Si le fichier est un .png, entre dans la boucle
            # Récupère le chemin d'accès au fichier et le stocke dans path
            path = os.path.join("pictures", filename)
            # Crée une clé pour accéder à l'élément dans le dictionnaire en prenant le nom du
            # fichier et en enlevant l'extension (-4 caractères)
            key = filename[:-4]
            # On stocke l'image donnée dans le dictionnaire
            image_dict_temp[key] = pygame.image.load(path).convert_alpha()
    return image_dict_temp


def defeat():
    """Si le tableau est plein dans ce cas c'est la défaite."""
    if number_case == 25:  # Le tableau est plein
        return 1  # On renvoie 1
    else:
        return 0  # Sinon 0


def random_case():
    """Place une case (2 ou 4 au hasard avec 2 ayant une probabilité de 0.75 et 4 de 0.25)
    dans TAB à une position aléatoire"""
    number = randr(0, 4)
    # Choisit un nombre au hasard afin de déterminer si un 2 ou un 4 apparait
    global number_case  # Indique que l'on veut utiliser la variable globale
    global score
    # Choisit les coordonnées dans le tableau au hasard
    number_x, number_y = randr(0, 5), randr(0, 5)
    if tab[number_x][number_y] == 0:  # Vérifie si la case est vide
        if number == 0:  # if et else servent ici à déterminer 2 ou 4 à partir de la valeur aléatoire
            number = 4
            score = score + 4
            number_case += 1  # On ajoute une case
        else:
            number = 2
            score = score + 2
            number_case += 1
    else:
        random_case()
        return
    # Entre la valeur déterminée au hasard dans une case vide
    tab[number_x][number_y] = number
    return


def display():
    """Fonction qui lit le tableau(tab), afin d'associer à chaque nombre son image
    correspondante et l'affiche, de plus elle gere le score et vérifie la victoire"""
    global score  # On spécifie que l'on utilise les variables globales
    global varvic  # afin qu'on puisse les modidier
    global background  # de manière globale et non de manière locale
    global image_dict
    if varvic == 1:  # Si on a gagné, change le fond d'écran
        background = "background_win"
    # Affiche la grille de jeu avec le bon fond d'écran
    window.blit(image_dict.get(background), (0, 0))
    victoire = 0
    for x in range(0, 5):  # Boucle qui parcourt le tableau
        for y in range(0, 5):
            if tab[x][y] != 0:
                # Stocke dans la variable dispcoord l'equivalent en coordonnées dans le plan
                # à partir des coordonnées dans le tableau
                dispcoord = coords(x, y)
                # "Créé le nom de l'objet à afficher
                key = "case" + str(tab[x][y])
                if key in image_dict:  # si la case existe
                    # Affiche l'objet
                    window.blit(image_dict.get(key), dispcoord)
                else:
                    imagegen(key)  # On génère une image
                    image_dict = images_load()  # on met a jour le dictionnaire
                    # Affiche la case nouvellement crée
                    window.blit(image_dict.get(key), dispcoord)
            if tab[x][y] >= 8:  # Si on détecte un 2048 ou plus
                victoire = 1
    text_score = font.render(str(score), True, (0, 0, 0))
    window.blit(text_score, (762, 77))  # On affiche le score
    pygame.display.flip()  # Rafraichit l'écran
    return victoire


def coords(x, y):
    """Associe les coordonnées dans le plan à partir des coordonnées du tableau"""
    return (461+71*y, 181+71*x)  # 461 et 181 sont les coordonnées de la première case, le delta entre les coordonnées
    # pour la case suivante est de 71, on ajoute donc x et y fois 71 afin d'avoir les coordonnées de la case souhaitée


volume = 1.0  # On initialise la variable volume
ResX = 1280  # Résolution écran horizontale
ResY = 720  # Résolution écran verticale
pygame.font.init()  # Initialisation de font
pygame.mixer.init()  # Initialisation de mixer
# Chargement du fichier mp3 'background'
pygame.mixer.music.load("background.mp3")
# -1 est le nombre de répétitions (ici infini), et 0 correspond au début de la musique
pygame.mixer.music.play(-1, 0)
font = pygame.font.Font('comic.ttf', 40)  # On définit la police et la taille
score = 0  # On initialise le score
pygame.mixer.music.set_volume(volume)  # On définit le volume de base
varvic = 0  # Initialisation pour le premier run de display()
vardefeat = 0  # On initialise la variable de défaite
background = "background"
number_case = 0  # Ainsi que le compteur de case
cons = [0] * 5  # Création du tableau contenant les cases
tab = [0] * 5
for i in range(5):
    tab[i] = list(cons)
os.environ['SDL_VIDEO_WINDOW_POS'] = "50, 50"
window = pygame.display.set_mode((ResX, ResY))
running = 1  # Initialisation de la variable de la permettant d'entrer boucle principale
image_dict = images_load()  # Fonction qui charge toutes les images
# elle est utilisée dans la fonction display
varvic = display()
menu_victory = 0  # Indique si on est sur le menu de la victoire
while running:  # Boucle while principale
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:  # si l'event est un bouton de la souris
            if event.button == 4 and volume < 1:  # roll up
                volume += 0.05  # On augmente le volume
                pygame.mixer.music.set_volume(volume)
            elif event.button == 5 and volume > 0:  # roll down
                volume -= 0.05  # On baisse le volume
                pygame.mixer.music.set_volume(volume)
        if event.type == QUIT:  # Appui sur la croix
            running = 0
        elif event.type == KEYDOWN:  # Si on détecte une frape de clavier
            if event.key == K_DOWN and vardefeat == 0 and menu_victory == 0:  # Flèche du bas
                # On demande de tenter de déplacer les cases vers le bas
                move("down")
            elif event.key == K_UP and vardefeat == 0 and menu_victory == 0:  # Flèche du haut
                move("up")
            elif event.key == K_LEFT and vardefeat == 0 and menu_victory == 0:  # Flèche de gauce
                move("left")
            elif event.key == K_RIGHT and vardefeat == 0 and menu_victory == 0:  # Flèche de droite
                move("right")
            elif event.key == K_RETURN and vardefeat == 1:  # En cas de défaite et d'appui sur entrer
                for i in range(5):  # On réinitialise le tableau
                    tab[i] = list(cons)
                    score = 0  # Et le score
                number_case = 0  # et le nombre de case
                background = "background"  # et le fond d'ecran au cas ou on aurait attend 2048
                varvic = 0  # et les variables défaite/win
                vardefeat = 0
                varvic = display()  # On met a jour l'affichage
            elif event.key == K_RETURN and varvic == 1 and menu_victory == 1:
                varvic = display()  # On met a jour l'affichage
                menu_victory = 0  # Nous ne somme plus sur le menu de victoire
        elif event.type == KEYUP:
            # Si la touche pressée est utilisée par le programme, sauf Entrée, ou ce n'est pris que si on perd, ou si on gagne
            if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                vardefeat = defeat()  # On vérifie si c'est la défaite
                if vardefeat == 1:  # Si défaite
                    # Affiche le menu de défaite
                    window.blit(image_dict.get("defaite"), (0, 0))
                    pygame.display.flip()  # Rafraîchit l'écran
                elif menu_victory == 0:  # on vérifie que l'on a pas appuyer sur entrée
                    # Car sinon cela gnénére une case après le menu de victoire
                    random_case()  # Crée une case aléatoire
                    varvic = display()
                if varvic == 1 and background != "background_win":  # Si victoire et que le fond n'a pas été changé
                    # Affiche le menu de victoire
                    window.blit(image_dict.get("victoire"), (0, 0))
                    pygame.display.flip()  # Rafraîchit l'écran
                    menu_victory = 1  # Nous somme donc sur le menu de la victoire

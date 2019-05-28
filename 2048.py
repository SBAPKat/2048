
# coadingding=utf-8
import pygame
import os
import traceback
from PIL import Image, ImageDraw, ImageFont
from random import randrange as randr
from pygame.locals import *

pygame.init()


def imagegen(case_title):
    case_content = ''
    for character in case_title:
        if character not in 'case':
            case_content = case_content + character
    default = Image.open('pictures/default.png') # ouvre image "default"
    txt = Image.new('RGBA', default.size, (255,255,255,0)) # créée une image vide avec channels rouge bleu vert et transparence, de la taile de default, fond transparent
    fnt = ImageFont.truetype('comic.ttf',20) # Récupère la police, et le règle sur la taille voulue
    d = ImageDraw.Draw(txt) # Récupère le contexte de dessin de l'image txt
    d.text((0,20), case_content, font=fnt, fill=(200,200,200,255)) # ecrit le numéro de la case sur le contexte de dessin, en gris clair
    output = Image.alpha_composite(default, txt) # calque l'image txt sur l'image default
    case_title = "pictures/" + case_title + ".png" # ajoute l'extension et l'arborescence au titre
    output.save(case_title) # sauvegarde l'image sous le titre fait précedemment


def exceptonormal():
    """fonction exécutée dans move
    celle-ci permet de convertir les chiffres multiples de 2+1 en multiples de 2
    une fois toutes les cases déplacées"""
    for x in range(5):
        for y in range(5):
            if tab[x][y] % 2 == 1: # on vérifie si la case parcourue contient un nombre impair
                tab[x][y] = tab[x][y] - 1 #si oui on retire 1
    return


def move(deway):
    """fonction qui gere le deplacement, deway est la variable contenant le sens voulu, les variables x et y sont respectivement
    les lignes et les colones du tableau"""
    global number_case # pour pouvoir modifier globalement number_case on doit définir number_case
    # comme la variable précédement définie globalement
    if deway == "down" or deway =="right":
        borninf = 3 # valeur utilisée dans les boucles for qui suivent
        bornsup = -1 # elle varie en fonction de la manière dont on veut parcourir
        # le tableau
        step = -1
        direction = 1 # Varie en fonction du sens de lecture : tab[x][y] est la case déplacée
        # tab[x+direction][y] ou  tab[x][y+direction] est la case sur laquelle tab[x][y] va se déplacer.
    else:
        borninf = 1
        bornsup = 5
        step = 1
        direction = -1
    if deway == "down" or deway == "up":
        for passage in range(4): # Pour qu'une case parcourt tout le tableau, elle doit se déplacer de 4 cases 
            for x in range(borninf,bornsup,step): # minimum, maximum, pas, on lit le  tableau  ligne par ligne
                for y in range(5):
                    if tab[x + direction][y] == tab[x][y] and tab[x][y] % 2 == 0 and tab[x][y] != 0: # si la case adjacente est la case
                        # à déplacer sont identiques et qu'elles n'ont pas deja été fusionées (nombre impair) 
                        tab[x + direction][y] = 2 * tab[x][y] + 1 
                        # on fait fois deux pour combiner les cases, puis on rajoute 1 afin de ne pas
                        # fusionner deux fois une case lors d'un passage
                        tab[x][y] = 0 #L'ancienne position de la case est donc = à 0
                        number_case -= 1 #deux case on fusionées, on retire une case du compteur
                    if tab[x + direction][y] == 0 and tab[x][y] !=0: # la case adjacente est vide et la case à déplacer ne l'est pas
                        tab[x + direction][y] = tab[x][y] #on place donc la case à déplacer à la place de la case adjacente
                        tab[x][y] = 0 #L'ancienne posotion vaut donc 0
        exceptonormal()  # on retire les 1 ajoutés précedemment
        return
    else:
        for passage in range(4):
            for y in range(borninf,bornsup,step): # on lit le tableau colones par colones
                for x in range(5):
                    if tab[x][y + direction] == tab[x][y] and tab[x][y] % 2 == 0 and tab[x][y] != 0:
                        tab[x][y + direction] = 2 * tab[x][y] + 1  # on fait fois deux pour combiner les cases
                        tab[x][y] = 0
                        number_case -= 1
                    if tab[x][y + direction] == 0 and tab[x][y] !=0:
                        tab[x][y + direction] = tab[x][y]
                        tab[x][y] = 0
        exceptonormal()
        return

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

def defeat():
    """Si le tableau est plein dans ce cas c'est la défaite."""
    if number_case == 25 :# le tableau est plein
        return 1 # on renvoie 1
    else:
        return 0 # sinon 0

def random_case():
    """Place une case (2 ou 4 au hasard avec 2 ayant une probabilité de 0.75 et 4 de 0.25) dans TAB à une position aléatoire"""
    number = randr(0, 4)  # Choisit un nombre au hasard afin de déterminer si un 2 ou un 4 apparait
    global number_case
    global score
    number_x, number_y = randr(0, 5), randr(0, 5)  # Choisit les coordonnées dans le tableau au hasard
    if tab[number_x][number_y] == 0:  # Vérifie si la case est vide
        if number == 0:  # if et else servent ici à déterminer 2 ou 4 à partir de la valeur aléatoire
            number = 4
            score = score + 4
            number_case += 1 # on ajoute une case
        else:
            number = 2
            score = score + 2
            number_case += 1
    else:
        random_case()
        return
    tab[number_x][number_y] = number  # Entre la valeur déterminée au hasard dans une case vide
    return  # Condition pour running = Ne pas perdre


def display():
    """Fonction qui lit le tableau(tab) ,afin d'associer à chaque nombre son image
    correspondante et l'affiche, de plus elle gere le score et vérifie la victoire"""
    global score # on spécifie que l'on utilise les variables gloabale
    global varvic # de manière à ce que lorsque on les modifies
    global interface # ce soit de manière gloabale et non locale
    global image_dict
    if varvic == 1: # si on a gagné, change le fond d'écran
        interface = "interface_win"
    window.blit(image_dict.get(interface), (0, 0))  # Affiche la grille de jeu avec le bon fond d'écran
    victoire = 0
    for x in range(0, 5):  # boucle qui parcourt le tableau
        for y in range(0, 5):
            if tab[x][y] != 0:
                dispcoord = coords(x, y)  # Stocke dans la variable dispcoord l'equivalent en coordonnées dans le plan à partir des coordonnées dans le tableau
                key = "case" + str(tab[x][y])  # "Créé le nom de l'objet à afficher
                if key in image_dict: #si la case existe
                    window.blit(image_dict.get(key), dispcoord)  # Affiche l'objet
                else:
                    imagegen(key) # on génère une image
                    image_dict = images_load() # on met a jour le dictionnaire
                    window.blit(image_dict.get(key), dispcoord)  # Affiche la case nouvellement crée
            if tab[x][y] >= 2048: # si on détecte un 2048 ou plus
               victoire = 1
    text_score = font.render(str(score), True, (0, 0, 0))
    window.blit(text_score, (762, 77)) # on affiche le score
    pygame.display.flip()  # Rafraichit l'écran
    return victoire



def coords(y, x):
    """Associe les coordonnées dans le plan à partir des coordonnées du tableau"""
    return  (461+71*x, 181+71*y) # 461 et 181 sont les coordonnées de la première case, le delta entre les coordonnées
    # pour la case suivante est de 71, on ajoute donc x et y fois 71 afin d'avoir les coordonnées de la case souhaitée


volume = 1.0 # on initialise la variable volume
ResX = 1280  # Résolution écran horizontale
ResY = 720  # Résolution écran verticale
pygame.font.init() # initialisation de font
pygame.mixer.init() # initialisation de mixer
pygame.mixer.music.load("background.mp3") # chargement du fichier mp3 'background'
pygame.mixer.music.play(-1, 0) # -1 est le nombre de répétitions (ici infini), et 0 correspond au début de la musique
font = pygame.font.Font('comic.ttf', 40) # on définit la police et la taille
score = 0 # on initialise le score
pygame.mixer.music.set_volume(volume) # On définit le volume de base
varvic = 0 # initialisation pour le premier run de display()
vardefeat = 0
interface = "interface"
number_case = 0 # ainsi que le compteur de case
cons = [0] * 5  # Création du tableau contenant les cases
tab = [0] * 5
for i in range(5):
    tab[i] = list(cons)
os.environ['SDL_VIDEO_WINDOW_POS'] = "50, 50"
window = pygame.display.set_mode((ResX, ResY))
running = 1
pygame.key.set_repeat(400, 30)
image_dict = images_load()  # Fonction qui charge toutes les images
# elle est utilisée dans la fonction random_case
varvic = display()
while running: # boucle while principale
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4 and volume < 1: #roll up
                volume += 0.05
                pygame.mixer.music.set_volume(volume)
            elif event.button == 5 and volume > 0: #roll down
                volume -= 0.05
                pygame.mixer.music.set_volume(volume)
        if event.type == QUIT:
            running = 0
        elif event.type == KEYDOWN:
            if event.key == K_DOWN and vardefeat == 0:
               move("down") # on demande de tenter de déplacer les cases vers le bas
            elif event.key == K_UP and vardefeat == 0:
               move("up")
            elif event.key == K_LEFT and vardefeat == 0:
               move("left")
            elif event.key == K_RIGHT and vardefeat == 0:
               move("right")
            elif event.key == K_RETURN and vardefeat == 1: # en cas de défaite et d'appui sur entrer
               for i in range(5): # on réinitialise le tableau
                   tab[i] = list(cons)
                   score = 0 # et le score
                   number_case = 0 # et le nombre de case
                   interface = "interface" # et l'interface
                   varvic = 0 # et les variables défaite/win
                   vardefeat=0
                   display()
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN or event.key == K_RETURN and (vardefeat == 1 or (varvic == 1 and vardefeat ==1)or varvic == 1 and interface == "interface"): # si la touche pressée est utilisée par le programme, sauf Entrée, ou ce n'est pris que si on perd, ou si on gagne
                vardefeat = defeat() # on vérifie la victoire ou défaite
                if vardefeat == 1: # si défaite
                    window.blit(image_dict.get("defaite"), (0,0)) # Affiche le menu de défaite
                    pygame.display.flip()
                elif vardefeat == 0: # sinon
                    random_case() # crée une case aléatoire
                    varvic = display()
                if varvic == 1 and interface != "interface_win":
                    window.blit(image_dict.get("victoire"), (0,0)) # Affiche le menu de victoire
                    pygame.display.flip()


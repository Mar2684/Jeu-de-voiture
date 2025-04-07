# Créé par mariu, le 16/12/2023 en Python 3.7
import pickle
import pygame
import random
import time
import sys
from pygame.locals import*
pygame.init()

meilleur_score = 0
try:
    with open('meilleur_score.dat', 'rb') as file:
        meilleur_score = pickle.load(file)
except:
    meilleur_score = 0

x_voiture_police = 10
y_voiture_police = 295

x_voiture = 1280
y_voiture = 25
voiture_sur_écran = False
nmbr_voitures = 0
nmbr_voiture_totale = 0
move_x_voiture = 18
tours = 0
listRandom = [25, 295, 565, 295]

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 50)
text = font.render('Game Over', True, (255,0,0))
textRect = text.get_rect()
textRect.center = (640, 395)

police = pygame.font.Font(None, 30)

fenetre = pygame.display.set_mode((1280, 790), RESIZABLE)
voiture_de_police_initial = pygame.image.load("voiture_de_police.png").convert_alpha()
voiture_de_police = pygame.transform.rotate(voiture_de_police_initial, 90)
voiture_de_police = pygame.transform.scale(voiture_de_police, (360, 200))

voiture_initial = pygame.image.load("voiture.png").convert_alpha()
voiture = pygame.transform.scale(voiture_initial, (360, 200))

#importation de l'arrière_plan :
image_arPlan = list()
for i in range(1, 11):
    image_arPlan += [pygame.image.load(f"fenetre_{i}.png")]
nr_arPlan = 1

def aff_fond():
    global nr_arPlan, image_arPlan
    fenetre.blit(image_arPlan[nr_arPlan - 1],(0,0))
    if nr_arPlan < 10:
        nr_arPlan += 1
    else:
        nr_arPlan = 1


def aff_score():
    global police, nmbr_voiture_totale, meilleur_score, points, af_meilleur_score
    points = police.render(f"Total : {nmbr_voiture_totale}", True, (255, 255, 255))
    af_meilleur_score = police.render(f"Meilleur : {meilleur_score}", True, (255, 255, 255))
    fenetre.blit(points, (1180, 0))
    fenetre.blit(af_meilleur_score, (10, 0))

def move_voiture_police(direction):
    global x_voiture_police, y_voiture_police
    if (direction > 0 and y_voiture_police < 565) or (direction <0 and y_voiture_police > 25):
        y_voiture_police += direction

def move_voiture():
    global voiture_sur_écran, x_voiture, y_voiture, move_x_voiture, nmbr_voitures, nmbr_voiture_totale, tours, listRandom, meilleur_score
    if voiture_sur_écran == False:
        del(listRandom[-1])
        listRandom.append(y_voiture_police)
        y_voiture = random.choice(listRandom)
        x_voiture = 1280
        voiture_sur_écran = True
    x_voiture -= move_x_voiture
    if x_voiture < -360:
        voiture_sur_écran = False
        nmbr_voitures += 1
        nmbr_voiture_totale += 1
        if nmbr_voiture_totale > meilleur_score:
            with open('meilleur_score.dat', 'wb') as file:
                pickle.dump(nmbr_voiture_totale, file)
        try:
            with open('meilleur_score.dat', 'rb') as file:
                meilleur_score = pickle.load(file)
        except:
            meilleur_score = 0
    if nmbr_voitures == 3:
        nmbr_voitures = 0
        move_x_voiture += 2

def collision():
    global x_voiture, y_voiture, x_voiture_police, y_voiture_police, points, af_meilleur_score
    run = True
    if y_voiture == y_voiture_police and x_voiture <= 370:
        pointsRect = points.get_rect()
        pointsRect.center = (640, 450)
        af_meilleur_scoreRect = af_meilleur_score.get_rect( )
        af_meilleur_scoreRect.center = (640, 490)
        while run:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                         run = False
            fenetre.fill((0,0,0))
            fenetre.blit(text, textRect)
            fenetre.blit(points, pointsRect)
            fenetre.blit(af_meilleur_score, af_meilleur_scoreRect)
            pygame.display.flip()
        print(meilleur_score)
        pygame.quit()
        quit()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event. type == KEYDOWN:
            if event.key == K_DOWN:
                move_voiture_police(270)
            if event.key == K_UP:
                move_voiture_police(-270)
    clock.tick(80)
    fenetre.fill((0,0,0))
    aff_fond()
    move_voiture()
    fenetre.blit(voiture_de_police, (x_voiture_police, y_voiture_police))
    fenetre.blit(voiture, (x_voiture, y_voiture))
    aff_score()
    collision()
    pygame.display.flip()
pygame.quit()
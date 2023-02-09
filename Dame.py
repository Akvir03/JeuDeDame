#################################################
#jeu de dame  sept 2022 
#Anne Pacou
#################################################

######################bibliothèques##################################
from numpy import *
import random as rd
from tkinter import *
import time
#####################variables globales d'affichage##################
debutx=60
debuty=50
taille=50

nb_cases=11
class position:#represente la position sur le damier
    i : int
    j : int 

en_cours=False
blanc=True
damier_deplacement=[]
#code pour damier déplacement, 0 déplacement impossible, 1 déplacement possible, 2 déplacement possible avec prise, 
# 3 position de la prise, 5 déplacement avec passage en dame d'un pion, 4 prise + passage en dame
i_depart=0
j_depart=0
doit_prendre=False

mode_joueur:int=0
#vaut 0 si mode deux joueurs, 1 pour joueur blanc contre IA, 2 pour joueur noir contre IA

##########################fonctions moteur de jeu####################################
def init_damier():
    """init_damier : creation du damier vide

    args : none
    return : le damier
    """
    tab =empty((nb_cases,nb_cases), dtype=object)
    for i in range(nb_cases):
        for j in range(nb_cases):
            tab[i,j]='  '
    return tab

def creation_damier():
    """creation_damier : creation du damier avec les pièces
        les blanches sont sur les colonnes de A à D = 10 à 7 (qui deviennent les lignes graphiquement)
        les noires sur J à G = colonnes  1 à 4
        les indices des colonnes sont les bons, la colonne et ligne 0 servant à placer les indices

    args : none
    return : le damier
    """
    tab=init_damier()
    for j in range(1,nb_cases):
        tab[0][j]=' '+chr(66+9-j) #1ère ligne composée de lettre (deviendra la première colonne)
        if j!=10:
            tab[j][0]=' '+str(j)#1ère colonne composée de nombre (devriendra la première ligne)
        else:
            tab[j][0]=str(j) #le 10 prend déjà 2 caractères
        for i in range(1,nb_cases):
            if ((j==1 or j==3) and i%2==0) or ((j==2 or j==4)and i%2==1):
                tab[i][j]='PN'
            if ((j==7 or j==9) and i%2==0) or ((j==8 or j==10)and i%2==1):
                tab[i][j]='PB'
    tab[3,4]="DN"
    tab[6,7]="DB"
    return tab
    
#########################coeur du jeu############################################
def dans_damier(num):
    """vérifie que le numéro  est dans le damier

    Args:
        num (int): la numéro de la ligne

    Returns:
        Bool: True si c'est dans le damier
    """
    if num>=1 and num<=nb_cases-1 :
        return True
    else:
        return False  

def deplace_pion (origine:position, dam ):
    """ deplace_pion: tableau de vérification de la position possible de déplacement

    args:
    origine : indice i et j d'origine de la pièce à déplacer
    dam : le damier d'échec

    return:    le tableau des déplacements possibles
    """

    support=zeros((nb_cases,nb_cases),dtype=int)
    i=origine.i
    j=origine.j
    piece=dam[i,j]
    noir=piece[1]=='N'
    #on vérifie qui joue
    if noir:
        action_j=+1
        lettre='B'
    #traitement propre aux pièces noires
    else :
        action_j=-1
        lettre='N' 
    #pièces blanches
    #on monte ou on descend suivant noir ou blanc, jeu normal
    orientation=[1,-1]
    for tour in orientation:
      #on commence dans l'ordre normal, puis en arrière  
        for action_i in orientation:
            if dans_damier(j +action_j*tour)and dans_damier(i+action_i): 
                #on ne déborde pas le damier à droite ou gauche         
                if dam[i+action_i,j+action_j*tour]=='  'and tour==1:
                    #la case est vide et on va dans le bon sens
                    if (j+action_j==nb_cases-1) or ( j+action_j==1):
                        #on est sur la ligne d'une dame
                        support[i+action_i,j+action_j*tour]=5
                    else: 
                        support[i+action_i,j+action_j*tour]=1
                        
                elif dam[i+action_i,j+action_j*tour][1]==lettre: #il y a un ennemi
                    if dans_damier(i+2*action_i) and dans_damier(j +2*action_j*tour):
                        #on ne déborde pas le damier, en sautant au dessus
                        if dam[i+2*action_i,j+2*action_j*tour]=='  ':
                            #la case d'après est vide
                            support[i+action_i,j+action_j*tour]=3
                            if j +2*action_j <nb_cases-1 and j +2*action_j*tour>1:
                            #pas une dame
                                support[i+2*action_i,j+2*action_j*tour]=2
                            elif tour==1:
                                #on a pris et c'est une dame
                                support[i+2*action_i,j+2*action_j*tour]=4
                            else:
                                #on est dans un cas de retour en arrière classique
                                support[i+2*action_i,j+2*action_j*tour]=2                         
   # print(support)
    return support
   
def passage (dep : position, action : position, dam, support, lettre):
    """ va incrémenter les indices
        
        dep : à partir de l'indice de départ
        action :dans une direction
        dam : pour le damier
        support le tableau support de déplacement
        lettre : la lettre "ennemie"

    return le tableau support :
    """
    i=dep.i+action.i
    j=dep.j+action.j
    fin=False #on est tombé sur une pièce
    while dans_damier(j) and dans_damier(i) and not fin:
        if dam[i,j]=='  ':
            support[i,j]=1
            i=i+action.i
            j=j+action.j
        else:
            fin=True
            #on est tombé sur une pièce, on vérifie que c'est un ennemi
            if dam[i,j][1]==lettre:
                suiv_i=i+action.i
                suiv_j=j+action.j
                #on vérifie que la case suivante est vide
                if dans_damier(suiv_j) and dans_damier(suiv_i):
                    if dam[suiv_i,suiv_j]=='  ':
                        support[i,j]=3
                        support[suiv_i,suiv_j]=2
                est_fini=False
                suiv_i=suiv_i+action.i
                suiv_j=suiv_j+action.j
                #on poursuit nos recherches dans les cases après
                while dans_damier(suiv_j) and dans_damier(suiv_i) and not est_fini:
                    if dam[suiv_i,suiv_j]=='  ':
                        support[suiv_i,suiv_j]=2
                        suiv_i=suiv_i+action.i
                        suiv_j=suiv_j+action.j
                    else:
                        est_fini=True 
    #print(support)
    return support

def deplace_dame (origine:position, dam ):
    """ deplace_dame: tableau de vérification de la position possible de déplacement dame

    args:
    origine : indice i et j d'origine de la pièce à déplacer
    dam : le damier 

    return:
    le tableau des déplacements possibles
"""
    support=zeros((nb_cases,nb_cases),dtype=int)
    piece=dam[origine.i,origine.j]
    noir=piece[1]=='N'
    if noir:
        lettre='B'
  #traitement propre aux pièces noires
    else :
        lettre='N' 
    #pièces blanches
    
    action =position() 
          #horizontal
    position_possible=[[1,1],[-1,1],[1,-1],[-1,-1]]  
    # diagonales
    for valeur in position_possible:
        action.i=valeur[0]
        action.j=valeur[1]
        support=passage(origine,action,dam,support,lettre)
      
    return support

def prise_possible(tab):
    """vérifie qu'une prise est possible sur le tableau support, utilisée lorsqu'on joue une pièce

    Args:
        tab (_type_): le tableau support contenant des nombres entiers

    Returns:
        bool: retourne True si une prise est possible
    """
    for i in range(nb_cases):
        for j in range(nb_cases):
            if tab[i,j]==2 or tab[i,j]==4:
                return True
    return False
        
def verif_prise_piece(damier,est_blanc,lig,col):
    """vérifie si un pion peut prendre, pas toutes les prises, mais une seule...
    Args:
        damier (array): le damier
        est_blanc (boolean): True si blanc
        lig (int): num de ligne
        col (int): num de colonne

    Returns:
        boolean: True si le pion peut prendre
    """
    if est_blanc:
        type_adverse="N"
    else:
        type_adverse="B"
    for i in range(-1,2,2):
        for j in range(-1,2,2):
            if dans_damier(lig+i) and dans_damier(col+j):#l'indice de la case en diagonale est dans le damier
                if damier[lig+i,col+j][1]==type_adverse:#la case contient un adversaire
                    if dans_damier(lig+2*i) and dans_damier(col+2*j):#l'indice de la case après est dans le damier
                        if damier[lig+2*i,col+2*j]=="  ":#la case est vide
                            return True #on peut prendre
    return False

def verif_prise_dame(damier,est_blanc,lig,col):
    """vérifie si une dame peut prendre, pas toutes les prises, mais une seule...
    Args:
        damier (array): le damier
        est_blanc (boolean): True si blanc
        lig (int): num de ligne
        col (int): num de colonne

    Returns:
        boolean: True si la dame peut prendre
    """
    if est_blanc:
        type_adverse="N"
    else:
        type_adverse="B"
    
    liste=[[-1,-1],[-1,1],[1,-1],[1,1]]
    #directions possibles
    for k in liste:
        fini=False
        i=k[0]
        j=k[1]
        while not fini and lig+i>0 and lig+i<nb_cases and col+j>0 and col+j<nb_cases: 
            #print(lig+i)
            #print(col+j)
            #print(damier[lig+i,col+j])
            if damier[lig+i,col+j]=="  ":
                i=i+k[0]
                j=j+k[1]
            #case inoccupée aux côtés de la dame et jusqu'a trouver une pièce
            elif damier[lig+i,col+j][1]==type_adverse:
                #on trouve une pièce adverse
                if dans_damier(lig+i+k[0]) and dans_damier(col+j+k[1]):
                    if damier[lig+i+k[0],col+j+k[1]]=="  ":
                        #on vérifie que derrière il y a une case vide
                        return True
                    else:
                        fini=True #sinon c'est fini pour la rangée
                else:
                    fini=True
            else: #il y a une pièce mais c'est une de sa couleur, c'est fini pour la rangée
                fini=True
        #print(fini)
    return False

def prise_obligatoire(damier,est_blanc):
    """va vérifier que le joueur est obligé de prendre

    Args:
        damier (array): le damier de jeu
        est_blanc (boolean): True si le joueur est le blanc

    Returns:
        boolean: True si la prise estg obligatorie
    """
    if est_blanc:
        type_pion="PB"
        type_dame="DB"
    else:
        type_pion="PN"
        type_dame="DN"
    for i in range(1,nb_cases):
        for j in range(1, nb_cases):
            if damier[i,j]==type_pion:
                #on passe les pièces en revue, et on vérifie si une de celles-là peut prendre, une suffit
                if verif_prise_piece(damier,est_blanc,i,j):
                    return True
            if damier[i,j]==type_dame:
                #même travail avec les dames
                if verif_prise_dame(damier,est_blanc,i,j):
                    return True

    return False

def gain(damier) :
    """vérifie qu'il reste des pions des 2 couleurs

    Args:
        damier (_type_): le damier de jeu

    Returns:
        boolean: True si c'est gagné
    """
    un_blanc=False
    un_noir=True
    for i in range(1,nb_cases):
        for j in range(1,nb_cases) :
            if  damier[i,j][1] =="N"  :
                un_noir=True
            if damier[i,j][1]=='B'  :
                un_blanc=True 
            if un_blanc and un_noir:
                return False
    return True      

#################################################IA###########################################
def est_deplacable(tab):
    """vérifie qu'une pièce peut se déplacer, à partir de son tableau support

    Args:
        tab (array): le tableau support de la pièce

    Returns:
        boolean: True si la pièce peut être déplacée
    """
    for i in range(nb_cases-1,-1,-1):
        for j in range(nb_cases):
            if tab[i,j]==1 :
            #déplacement simple 
                return True
    return False

def devient_dame(tab):
    """vérifie qu'on peut faire une dame, sur le tableau support

    Args:
        tab (array): le damier support de vérification des coups

    Returns:
        boolean: True si on gfait une dame avec ce déplacement
    """
    for i in range(nb_cases):
        for j in range(nb_cases):
            if tab[i,j]==5:
            #dame possible
                return True
    return False         

def possibilite_jeu(dam,blanc):
    """passe en revue les possibilités lors d'un tour de jeu

    Args:
        dam (_type_): le damier de jeu
        noir (bool): true si le joueur est noir

    Returns:
        bool: retourne True si la prise est obligatoire
    """
    prise_trouvee=[]
    deplacement=[]
    dames_a_venir=[]
    if blanc:
        lettre='B'
    else:
        lettre='N'
    for lig in range(nb_cases-1,-1,-1):
        for col in range(nb_cases):
            if dam[lig,col][1]==lettre:
                origine=position()
                origine.i=lig
                origine.j=col
                if dam[lig,col][0]=="D":
                    support=deplace_dame(origine, dam)
                    #création du tableau support de pièce
                else:
                    support=deplace_pion(origine, dam)
                if prise_possible(support):
                    prise_trouvee.append([lig,col])
                    #à cet emplacement se trouve une pièce qui peut prendre
                else :
                    if devient_dame(support):
                        dames_a_venir.append([lig,col])
                        #à cet emplacement se trouve une pièce qui peut devenir une dame
                    if est_deplacable(support):
                        deplacement.append([lig,col])
                        #cette pièce peut se déplacer
    """print("le tableau des prises possibles")
    print(prise_trouvee)
    print("les déplacements possibles")
    print( deplacement)
    print("et les dames à venir")
    print(dames_a_venir)"""
    return prise_trouvee, deplacement, dames_a_venir


def partie_aleatoire(tableau,blanc):
    """permet de créer une partie IA de base en respectant les règles

    Args:
        tableau (array): le damier de départ
        blanc (boolean): est TRUe si on joue pour les blancs

    Returns:
        array: le tableau modifié
    """
    global damier_deplacement
     #print("on entre dans l IA")
        #time.sleep(2)
        #tour de la machine IA
    prise_trouvee, deplacement, dames_a_venir=possibilite_jeu(tableau,blanc)
    if prise_trouvee!=[]:
        choix=prise_trouvee[rd.randint(0,len(prise_trouvee)-1)]
        #une des prises possibles au hasard
        damier_deplacement=zeros((nb_cases,nb_cases),dtype=int)
        contenu=tableau[choix[0],choix[1]]
        case_travail=position()
        case_travail.i=choix[0]
        case_travail.j=choix[1]
        affichage_possible(contenu,tableau,case_travail,False)
        trouve=False
        i=1
        while i<nb_cases and not trouve:
            j=1
            while j<nb_cases and not trouve:
                if damier_deplacement[i,j]==3:
                    #un pion à prendre, le premier
                    tableau[i,j]="  "#on efface le pion adverse
                    trouve=True #on aura fini une fois ce pion traité
                for k in range(-1,2,2):
                    for l in range(-1,2,2):
                        #on cherche la case utilisable autour
                        if dans_damier(i+k) and dans_damier(j+l):
                            if damier_deplacement[i+k,j+l]==4:
                            #la case vide d'arrivée du pion et devient une dame
                                valeur="D"+contenu[1] 
                                tableau[i+k,j+l]=valeur
                            if damier_deplacement[i+k,j+l]==2:
                            #la case vide d'arrivée du pion
                                tableau[i+k,j+l]=contenu #chgt de la cse en le pion
                j=j+1
            i=i+1
                
        tableau[choix[0],choix[1]]="  "
        #on efface la case de départ

    elif dames_a_venir!=[]:
        choix=dames_a_venir[rd.randint(0,len(dames_a_venir)-1)]
        #une des dames possibles au hasard, souvent une seule...
        damier_deplacement=zeros((nb_cases,nb_cases),dtype=int)
        contenu=tableau[choix[0],choix[1]]
        case_travail=position()
        case_travail.i=choix[0]
        case_travail.j=choix[1]
        affichage_possible(contenu,tableau,case_travail,False)
        trouve=False
        i=1
        while i<nb_cases and not trouve:
            j=1
            while j<nb_cases and not trouve:
                if damier_deplacement[i,j]==5:
                    #on cherche l'emplacement de la dame
                    valeur="D"+contenu[1] 
                    tableau[i+k,j+l]=valeur
                    trouve=True #on aura fini une fois ce pion traité
                j=j+1
            i=i+1
        tableau[choix[0],choix[1]]="  "
        #on efface la case de départ
    elif deplacement!=[]:
        choix=deplacement[rd.randint(0,len(deplacement)-1)]
        #un des déplacements au hasard
        damier_deplacement=zeros((nb_cases,nb_cases),dtype=int)
        contenu=tableau[choix[0],choix[1]]
        case_travail=position()
        case_travail.i=choix[0]
        case_travail.j=choix[1]
        affichage_possible(contenu,tableau,case_travail,False)
        #print(choix)
        #print(damier_deplacement)
        trouve=False
        i=1
        while i<nb_cases and not trouve:
            j=1
            while j<nb_cases and not trouve:
                if damier_deplacement[i,j]==1:
                    #on cherche un déplacement de ce pion /dame, le premier
                    tableau[i,j]=contenu
                    print(contenu)
                    trouve=True #on aura fini une fois ce pion traité
                j=j+1
            i=i+1
        tableau[choix[0],choix[1]]='  '
        #on efface la case de départ
    #print(tableau)
    damier_deplacement=zeros((nb_cases,nb_cases),dtype=int)
    return tableau
###################################### représentation et jeu ######################
def dessin_damier():
    """ dessin du quadrillage

    """
    pos=10
    for i in range(1,nb_cases+2):
        cadre.create_line(pos+i*taille,taille,pos+i*taille, taille+taille*nb_cases)
    for i in range(0,nb_cases+1):
        cadre.create_line(pos+taille,taille+i*taille,pos+(nb_cases+1)*taille,taille+i*taille)

def affichage_possible(case,damier,depart,affiche):
    """vérifie les emplacements possibles en fonction des pièces
    case (str): la pièce qu'on veut déplacer
    damier (array): le damier global
    depart (position): point de départ de la pièce
    affiche (boolean) : True si on veut le montrer
    
    """
    global en_cours
    global damier_deplacement

    if case[0]=='P':
        damier_deplacement=deplace_pion(depart,damier)
    elif case[0]=='D':
        #print("dans la file dame")
        damier_deplacement=deplace_dame(depart,damier)
    else :
        pass
    en_cours=True        
    if prise_possible(damier_deplacement):
        for i in range(nb_cases):
            for j in range(nb_cases):
                if (damier_deplacement[i][j]==1) or (damier_deplacement[i,j]==5):
                    damier_deplacement[i,j]=0
    if affiche==True:
        dessin_piece()

#le clic gauche entraine une action sur le tableau visible
def clicGauche(event) :
    """on gère le jeu dès qu'il y a un clic
    """
    pos=10
    global damier
    global blanc
    global en_cours
    #en_cours est à false si c'est la sélection d'une pièce et True si on est en train de la placer
    global damier_deplacement
    global i_depart
    global j_depart
    global doit_prendre
    global mode_joueur
    
    if mode_joueur==0 or (mode_joueur==1 and blanc) or (mode_joueur==2 and not blanc):
        #jeu manuel si c'est un mode normal à deux joueurs, ou au joueur de jouer
        #print("tour du joueur")
        x = event.x
        y = event.y
        """print(x)
        print(y)
        print(blanc)
        print(en_cours)
        #print(damier)
        num_casex= (x-pos)//50-1
        num_casey= (y-pos)//50-1
        print(num_casex)
        print(num_casey)"""
        if en_cours==True :
            #print("on teste la prise")
            doit_prendre=prise_obligatoire(damier, blanc)
            #va permettre un affichage dans le cadre de jeu
        if taille+pos<=x<=nb_cases*(taille+3)+pos and taille+pos<=y<=nb_cases*(taille+3)+pos :
            #on a cliqué dans le damier
            num_casex= (x-pos)//50-1
            num_casey= (y-pos)//50-1
            #print(num_casex)
            #print(num_casey)
            premier=position()
            premier.i=num_casex
            premier.j=num_casey
            if en_cours and premier.i==i_depart and premier.j==j_depart:
                #on reclique sur sa case, la pièce est reposée
                en_cours=False   
                damier_deplacement=zeros((nb_cases,nb_cases),dtype=int) 
                dessin_piece()
            elif blanc and not en_cours:
                #au blanc de jouer et choix d'une pièce
                #print("première récup")
                case=damier[premier.i,premier.j]
            # on récupère le contenu de la case
                if case[1]=='B':
                    #c'est une blanche
                    affichage_possible(case,damier,premier,True)
                    i_depart=premier.i
                    j_depart=premier.j
                    #on conserve les coordonéees du point de départ
            elif not blanc and not en_cours :
                #au noir de jouer et choix d"une pièce
                case=damier[premier.i,premier.j]
                if case[1]=='N':
                    affichage_possible(case,damier,premier,True)
                    i_depart=premier.i
                    j_depart=premier.j
            else :
                #on est en train de déplacer une pièce
                if damier_deplacement[premier.i,premier.j]==1 and not prise_obligatoire(damier,blanc):
                # print("on place une pièce sur un déplacement normal")
                    damier[premier.i,premier.j]=damier[i_depart,j_depart]
                    damier[i_depart,j_depart]='  '
                    en_cours=False
                elif damier_deplacement[premier.i,premier.j]==5 and not prise_obligatoire(damier,blanc):
                    #passage en dame du pion
                    damier[i_depart,j_depart]='  '
                    en_cours=False
                    #le tour du joueur est terminé
                    if blanc:
                        damier[premier.i,premier.j]="DB"  
                    else :
                        damier[premier.i,premier.j]="DN" 
                elif damier_deplacement[premier.i,premier.j]==2 or damier_deplacement[premier.i,premier.j]==4:
                    #on peut prendre
                    case_depart=damier[i_depart,j_depart]
                    damier[i_depart,j_depart]='  '   #on efface la case de départ
                    i=premier.i
                    j=premier.j
                    orientation=[-1,1]
                    pion_pris=position()
                    pion_pris.i=-1
                    pion_pris.j=-1
                    #recherche de la position du pion pris
                    while pion_pris.i==-1:
                        for k in orientation:
                            for l in orientation :
                                if dans_damier(i+k) and dans_damier(j+l):
                                    if damier_deplacement[i+k,j+l]==3:
                                        pion_pris.i=i+k
                                        pion_pris.j=j+l
                            if pion_pris.i==-1:
                                if i-i_depart>0:
                                    i=i-1
                                else:
                                    i=i+1
                                if j-j_depart>0:
                                    j=j-1
                                else:
                                    j=j+1
                        #cas de la dame, il faut chercher la case à prendre, pas juste à côté
                    damier[pion_pris.i,pion_pris.j]='  '#on efface le pion pris
                    if damier_deplacement[premier.i,premier.j]==2 :
                        #reste pion, on l'avance
                        damier[premier.i,premier.j]=case_depart
                        
                    else:
                        #passage en dame du pion
                        if blanc:
                            damier[premier.i,premier.j]="DB"  
                        else :
                            damier[premier.i,premier.j]="DN" 
                        damier_deplacement=zeros((nb_cases,nb_cases),dtype=int)
                    case=damier[premier.i,premier.j]
                    affichage_possible(case,damier,premier,False)
                    if prise_possible(damier_deplacement):
                        i_depart=premier.i
                        j_depart=premier.j
                    else:
                        en_cours=False       
                if not en_cours:
                    #on a placé la pièce, on peut passer au suivant
                    blanc=not blanc
                    doit_prendre=False
                    if gain(damier):
                        cadre.create_text(pos+3*taille, pos+5*taille, text=' Gagné! Vous pouvez quitter le jeu', font="Arial 20",fill='black') 
        #print("test fin")
        #print(damier)
        dessin_piece()    
    if not en_cours and ((mode_joueur==1 and not blanc) or (mode_joueur==2 and blanc)):
        damier=partie_aleatoire(damier,blanc)
        #print(damier)
        blanc=not blanc
        en_cours =False #le sous-progarmme affichage le change par défaut
        dessin_piece()
        #print("on sort de clic gauche")
        
                
def dessin_piece():
    """dessin du damier et des pièces"""
    pos=85
    rayon=20
    dessin_damier()
    global damier
    #print(damier)
    global damier_deplacement
    global en_cours
    global blanc
    global doit_prendre
    if doit_prendre :
        cadre.create_rectangle(debutx+12*taille,250,debutx+18*taille,300,fill="white")
        cadre.create_text(debutx+14*taille, 270, text=' Prise obligée', font="Arial 20",fill='black') 
    else :
        if blanc :#positionnement du cadre blanc "tour des ..."
            cadre.create_rectangle(debutx+12*taille,250,debutx+18*taille,300,fill="white")
            cadre.create_text(debutx+14*taille, 270, text=' Tour des blancs', font="Arial 20",fill='black') 
        else:
            cadre.create_rectangle(debutx+12*taille,250,debutx+18*taille,300,fill="white")
            cadre.create_text(debutx+14*taille, 270, text='Tour des noirs', font="Arial 20",fill='black')
        
            #pour écrire le tour en cours
    cadre.create_text(pos+5*taille, pos+11*taille, text='cliquer sur une de vos pièces, puis sur une des cases proposées', font="Arial 16",fill='black') 
    cadre.create_text(pos+5*taille, pos+12*taille, text='si une case verte est proposée, elle est obligatoire', font="Arial 16",fill='black')   
    cadre.create_text(pos+5*taille, pos+13*taille, text='cliquez sur votre case de départ pour prendre une autre pièce', font="Arial 16",fill='black') 
    for i in range(nb_cases):
        for j in range(nb_cases):
            if en_cours and damier_deplacement[i,j]==1:
                cadre.create_rectangle(debutx+i*taille,debuty+j*taille,debutx+(i+1)*taille,debuty+(j+1)*taille,fill="yellow")
                #cases des déplacements possibles
            elif en_cours and (damier_deplacement[i,j]==2 or damier_deplacement[i,j]==4) :
                cadre.create_rectangle(debutx+i*taille,debuty+j*taille,debutx+(i+1)*taille,debuty+(j+1)*taille,fill="green")
                #cases des déplacements possibles
            elif not en_cours and i!=0 and j!=0 and (i+j)%2 ==0:
                cadre.create_rectangle(debutx+i*taille,debuty+j*taille,debutx+(i+1)*taille,debuty+(j+1)*taille,fill="white")
                #damier cases grises
            elif not en_cours and i!=0 and j!=0 and (i+j)%2 ==1:
                cadre.create_rectangle(debutx+i*taille,debuty+j*taille,debutx+(i+1)*taille,debuty+(j+1)*taille,fill="brown")
                #damier cases blanches
            if damier[i,j][1]=="N":
                couleur='black'
                coul_ligne="white"
            elif damier[i,j][1]=="B":
                couleur='white'
                coul_ligne="black"
            if damier[i,j][0]=="P":
                r=taille//3
                cadre.create_oval(pos+i*taille-r, pos-10+j*taille-r, pos+i*taille+r, pos-10+j*taille+r,fill=couleur)   
            #dessin de la pièce
            elif damier[i,j][0]=="D":
                r=taille//3
                r_petit=taille//6
                cadre.create_oval(pos+i*taille-r, pos-10+j*taille-r, pos+i*taille+r, pos-10+j*taille+r,fill=couleur)
                cadre.create_oval(pos+i*taille-r_petit, pos-10+j*taille-r_petit, pos+i*taille+r_petit, pos-10+j*taille+r_petit,outline=coul_ligne)
            #dessin de la dame
            else:
                #le reste
                cadre.create_text(pos+i*taille, pos+j*taille, text=damier[i][j], font="Arial 16",fill='red')   
###############################################COMMANDES DU MENU######################################  
def fin():
    """fin du programme"""
    fenetre.destroy()  

def jeu2joueurs():
    global mode_joueur
    mode_joueur=0
    fin()

def jeu1blanc():
    global mode_joueur
    mode_joueur=1
    fin()

def jeu1noir():
    global mode_joueur
    mode_joueur=2
    fin()
                
############################################### sauvegarde###########################################
              
def sauvegarde():
    """sauvegarde du damier, une seule sauvegarde possible"""
    global damier
    global mode_joueur
    fichier = open("../sauv.txt", "w")
    fichier.write(mode_joueur)
    fichier.write('\n')
    for i in range(nb_cases):
        for j in range(nb_cases):
            fichier.write(damier[i][j])
        fichier.write('\n')
    fichier.close()

def importation():
    """importation d'un damier sauvegardé"""
    global damier
    global mode_joueur
    fichier = open("../sauv.txt", "r")
    line = fichier.readline()
    mode_joueur=line[0]
    line = fichier.readline()
    i=0
    damier =empty((nb_cases,nb_cases), dtype=object)
    while line:
        if i<nb_cases:
            for j in range(0,nb_cases*2,2):
                damier[i][j//2]=line[j:j+2]
        i+=1
        line = fichier.readline()
    fichier.close()
    dessin_piece()

######################################programme principal  
if __name__=="__main__":
    #création de la fenêtre
    fenetre = Tk()
    fenetre.title('jeu de dames')
    #fenetre.geometry('1200x1200')#taille de la fenêtre globale
    fenetre.config(background = 'skyblue')

    cadre = Canvas(fenetre, width=1500,height=800, bg="light yellow")#création du cadre jaune
    cadre.pack(pady=50, padx=250)#centrage du cadre jaune
    boutonimport=Button(fenetre, text = 'IMPORTER UNE SAUVEGARDE', width = 50,font="Arial 18",background='orange', command = importation)
    boutonjeu2=Button(fenetre, text = 'JOUER A 2 JOUEURS', width = 50,font="Arial 18",background='orange', command =jeu2joueurs )
    boutonjeu1blanc=Button(fenetre, text = 'JOUER LES BLANCS CONTRE IA', width = 50,font="Arial 18",background='orange', command = jeu1blanc)
    boutonjeu1noir=Button(fenetre, text = 'JOUER LES NOIRS CONTRE IA', width = 50,font="Arial 18",background='orange', command = jeu1noir )
    boutonjeu2.place(x = 400, y = 250)
    boutonjeu1blanc.place(x=400,y=300)
    boutonjeu1noir.place(x=400,y=350)
    boutonimport.place(x=400, y=400)
    fenetre.mainloop()
    #print("on rentre dans le prog")
    #création de la fenêtre
    fenetre = Tk()
    fenetre.title('jeu de dames')
    #fenetre.geometry('1200x1200')#taille de la fenêtre globale
    fenetre.config(background = 'skyblue')

    cadre = Canvas(fenetre, width=1500,height=800, bg="light yellow")#création du cadre jaune
    cadre.pack(pady=50, padx=250)#centrage du cadre jaune
    damier=creation_damier()
    
    dessin_piece()

    fenetre.bind('<Button-1>', clicGauche)
    boutonsauv=Button(fenetre, text = 'SAUVEGARDER', width = 30, command = sauvegarde)
    bouton=Button(fenetre, text = 'QUITTER', width = 30, command = fin)
    bouton.place(x = 20, y = 250)
    boutonsauv.place(x=20,y=300)
    
    fenetre.mainloop()


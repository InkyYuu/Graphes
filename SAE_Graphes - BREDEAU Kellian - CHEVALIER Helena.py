import tkinter
# ========================================================================= FONCTIONS ET PROGRAMMES ========================================================================= #

def defauto():
    # Alphabet
    alphabet = input("Saisissez l'alphabet (séparé par des virgules) : ").split(',')

    # Automate
    automate = {'alphabet': alphabet, 'etats': [], 'transitions': [], 'I': [], 'F': []}

    # Etats
    while True:
        etat = input("Saisissez un état (ou 'fin' pour terminer) : ")
        if etat == 'fin':
            break
        elif etat in automate['etats']:
            print("Cet état existe déjà.")
        else:
            automate['etats'].append(etat)

    # Etats initiaux
    while True:
        I = input("Saisissez les états initiaux (séparés par des virgules) : ").split(',')
        if not all(etat in automate['etats'] for etat in I):
            print("Certains états n'existent pas.")
        else:
            automate['I'] = I
            break

    # Etats terminaux
    while True:
        F = input("Saisissez les états terminaux (séparés par des virgules) : ").split(',')
        if not all(etat in automate['etats'] for etat in F):
            print("Certains états n'existent pas.")
        else:
            automate['F'] = F
            break

    # Transition
    while True:
        transition = input("Saisissez une transition sous la forme 'etat1,lettre,etat2' avec les virgules (ou 'fin' pour terminer) : ")
        if transition == 'fin':
            break
        etat1, lettre, etat2 = transition.split(',')
        if etat1 not in automate['etats'] or etat2 not in automate['etats']:
            print("Certains états n'existent pas.")
        elif lettre not in automate['alphabet']:
            print("Cette lettre n'est pas dans l'alphabet.")
        elif (etat1, lettre) in automate['transitions']:
            print("Cette transition existe déjà.")
        else:
            automate['transitions'].append([etat1,lettre,etat2])

    return automate

def pref(u):
    return [u[:i] for i in range(len(u)+1)]

def suf(u):
    return [u[i:] for i in range(len(u)+1)]

def fact(u):
    facteurs = set()
    for i in range(len(u)):
        for j in range(i, len(u)+1):
            facteurs.add(u[i:j])
    return list(facteurs)

def miroir(u):
    return u[::-1]

def concatene(L1, L2):
    concac = set()
    for m1 in L1:
        for m2 in L2:
            concac.add(m1 + m2)
    return list(concac)

def puis(L, n):
    if n == 0:
        return ['']
    elif n == 1:
        return list(set(L))
    else:
        return concatene(L, puis(L, n-1))

def tousmots(A, n):
    if n <= 0:
        return ['']
    else:
        mots = []
        for a in A:
            for mot in tousmots(A, n-1):
                mots.append(a + mot)
        mots.append('')
        return mots

def lirelettre(T, E, a):
    lst = set()
    for e in E:
        for t in T:
            if t[0] == e and t[1] == a:
                lst.add(t[2])
    return list(lst)

def liremot(T, E, mot):
    etats = E
    for lettre in mot:
        etats = lirelettre(T, etats, lettre)
    return etats

def accepte(automate, m):
    A, T, E, I, F = automate["alphabet"], automate["transitions"], automate["etats"], automate["I"], automate["F"]
    for initiaux in I :
        etats_actuels = [initiaux]
        for lettre in m:
            etats_actuels = lirelettre(T, etats_actuels, lettre)
        for etat in etats_actuels:
            if etat in F:
                return True
        return False

def langage_accepte(automate, n):
    L = []
    for m in tousmots(automate['alphabet'], n): 
        if (accepte(auto,m)):
            L.append(m)
    return L

def deterministe(auto):
    if len(auto["I"]) > 1:
        return False
        
    for etat in auto['etats']:
        #On crée un dico d'occurence
        occurences = dict()
        for l in auto['alphabet']:
            occurences [l] = 0
        #On ajoute une occurence à chaque transition avec etat
        for t in auto['transitions']:
            if etat == t[0]:
                occurences[t[1]] += 1
        #Si l'occurence d'une lettre est supérieur à 1 alors pas déterministe
        for x in occurences.values() :
            if x > 1 :
                return False
    return True

def determinise(auto):
    #Si l'automate est déterministe on le retourne
    if deterministe(auto) :
        return auto
    etats = [auto["I"]].copy() 
    transitions = []
    x= 0
    #On parcourt tous les états en démarrant par l'union des initiaux
    while x < len(etats):  
        for e in etats[x]:
            for l in auto['alphabet']:
                lst = lirelettre(auto['transitions'], etats[x], l)
                #On ajoute les états qui permettent la transition
                if (len(lst) > 0):
                    #On l'ajoute si elle n'existe pas déjà
                    if [etats[x],l,lst] not in transitions:
                        transitions.append([etats[x],l,lst])
                    #On ajoute le nouvel union état
                    if lst not in etats:
                        etats.append(lst)
        x+= 1
        #On ajoute plus un et on recommence

    F = []
    F = [e2 for e2 in etats if any(e in e2 for e in auto["F"]) and e2 not in F]
    
    return {
            'alphabet': auto["alphabet"],
            'etats': etats,
            'transitions': transitions,
            "I": [auto["I"]],
            "F": F
            }

def renommage(auto):
    for x in range(len(auto['etats'])):
        for t in auto['transitions'] :
            for c in range(len(t)) :
                if t[c] == auto['etats'][x] :
                    t[c] = x
        for i in range(len(auto['I'])) :
            if auto['I'][i] == auto['etats'][x] :
                auto['I'][i] = x
        for f in range(len(auto['F'])) :
            if auto['F'][f] == auto['etats'][x] :
                auto['F'][f] = x
        auto['etats'][x] = x
    return auto    

def complet(auto):
    occurence = {}
    for e in auto['etats'] :
        occurence[e] = set()
    for t in auto['transitions'] :
        occurence[t[0]].add(t[1])
    for lettres in occurence.values() :
        if len(lettres) != len(auto['alphabet']):
            return False
    return True

def complete(auto):
    occurence = {}
    auto['etats'].append('ε')
    for e in auto['etats'] :
        occurence[e] = set()
    for t in auto['transitions'] :
        occurence[t[0]].add(t[1])
    for etats, lettres in occurence.items() :
        if len(lettres) < len(auto['alphabet']):
            for l in auto['alphabet'] :
                if l not in lettres :
                    auto['transitions'].append([etats, l, 'ε'])
    return auto

def complement(auto):
    auto_complement = complete(renommage(determinise(auto)))
    finaux = []
    for f in auto_complement['etats']:
        if f not in auto_complement['F'] :
            finaux.append(f)
    auto_complement['F'] = finaux
    return auto_complement

def inter(auto1, auto2):
    # Gestion des erreurs on va être sûr que les deux automates sont déterministes
    auto1 = determinise(auto1)
    auto2 = determinise(auto2)
    # Ensuite on récupère les paramètres
    alphabet = auto1["alphabet"] # A voir si d'autres alphabets peuvent se croiser
    #Creations de tous les etats possibles
    etats = []
    for e1 in auto1["etats"]:
        for e2 in auto2["etats"]:
            etats.append((e1, e2))
    #Création de l'état initial
    I = [(auto1["I"][0], auto2["I"][0])]
    #Création de les etats finaux
    F = []
    for a in auto1["F"]:
        for b in auto2["F"]:
            F.append((a, b))
    #Creations des transitions
    transitions = []
    for e1, e2 in etats:
        # Ajout de la transition initiale
        if (e1, e2) == (0, 0):
                for l in alphabet:
                    t1 = [(e1, i) for i in auto1["etats"] if [e1, l, i] in auto1["transitions"]]
                    t2 = [(e2, i) for i in auto2["etats"] if [e2, l, i] in auto2["transitions"]]
                    if t1 and t2:
                        transitions.append([(e1, e2), l, (t1[0][1], t2[0][1])])
        elif any((e1, e2) == t[2] for t in transitions):
                for l in alphabet:
                    t1 = [(e1, i) for i in auto1["etats"] if [e1, l, i] in auto1["transitions"]]
                    t2 = [(e2, i) for i in auto2["etats"] if [e2, l, i] in auto2["transitions"]]
                    if t1 and t2:
                        if [(e1, e2), l, (t1[0][1], t2[0][1])] not in transitions :
                            transitions.append([(e1, e2), l, (t1[0][1], t2[0][1])])
                            if not any((t1[0][1], t2[0][1]) == t[0] for t in transitions) :
                                etats.append((t1[0][1], t2[0][1]))

    #supprimer les etats qui ne sont pas utilisés
    newetats = [transitions[0][0]]
    for t in transitions:
        if t[0] not in newetats:
            newetats.append(t[0])
        if t[2] not in newetats:
            newetats.append(t[2])
    return {'alphabet': alphabet, 
            'etats': newetats, 
            'transitions': transitions, 
            'I': I, 
            'F': F}

def difference(auto1, auto2):
    auto1 = complete(auto1)
    auto2 = complete(auto2)
    # inverse les états finaux de auto2
    auto2_inv = {'alphabet': auto2['alphabet'],
                 'etats': auto2['etats'],
                 'transitions': auto2['transitions'],
                 'I': auto2['I'],
                 'F': [e for e in auto2['etats'] if e not in auto2['F']]}
    # produit de auto1 par l'inverse de auto2
    auto = inter(auto1, auto2_inv)
    # l'ensemble des états finaux est l'ensemble des états de auto1 qui ne sont pas dans auto2
    F = [(a, b) for a in auto1['F'] for b in auto2_inv['F'] if b not in auto2['F'] and (a,b) in auto['etats']]
    auto['F'] = F
    return auto

def prefixe(auto) :
    #Tous les etats sont finaux
    if not est_emondé(auto) :
        return False
    else :
        return {
            "alphabet" : auto["alphabet"],
            "etats" : auto["etats"],
            "transitions" : auto["transitions"],
            "I": auto["I"],
            "F": [e for e in auto["etats"]]
        }

def suffixe(auto) :
    #Tous les etats sont initiaux
    if not est_emondé(auto) :
        return False
    else :
        return {
            "alphabet" : auto["alphabet"],
            "etats" : auto["etats"],
            "transitions" : auto["transitions"],
            "I": [e for e in auto["etats"]],
            "F": auto["F"]
        }

def facteur(auto) :
    #Tous les etats sont finaux et initiaux
    if not est_emondé(auto) :
        return False
    else :
        return {
            "alphabet" : auto["alphabet"],
            "etats" : auto["etats"],
            "transitions" : auto["transitions"],
            "I": [e for e in auto["etats"]],
            "F": [e for e in auto["etats"]]
        }

def auto_miroir(auto) : #pour différencier de miroir(u)
    #On inverse le sens des transitions, les etats finaux deiviennent initiaux et vice versa pour les terminaux
    if not est_emondé(auto) :
        return False
    else :
        return {
            "alphabet" : auto["alphabet"],
            "etats" : auto["etats"],
            "transitions" : [[transition[2], transition[1], transition[0]] for transition in auto["transitions"]],
            "I": auto["F"],
            "F": auto["I"]
        }

def minimise(auto):
    """Etant donné un automate complet et déterministe,
    Renvoie l'automate minimisé"""
    classes = list()
    classes.append(set(auto["F"]))  # on ajoute dans la classe les états finaux
    # on ajoute dans la classe les états non finaux
    classes.append({etat for etat in auto["etats"] if etat not in auto["F"]})
    # on crée les groupes d'états équivalents
    auto["etats"] = [list(s) for s in classes_etats(
        auto, classes, dico_transi(auto))] # transforme en liste les ensembles d'états équivalents

    dico_classe = dico_classes(auto["etats"]) # dictionnaire associant à chaque état, son nouvel état selon sa classe

    finaux = []
    for etat in auto["F"]:
        if dico_classe[etat] not in finaux:
            # pour chaque état final, on récupère son nouvel état et on l'ajoute à la liste des finaux s'il n'y est pas déjà
            finaux.append(dico_classe[etat])
    auto['F'] = finaux # on associe la liste des finaux créée
    # on récupère les états initiaux en accédant à la valeur du dictionnaire associée à la clé de l'état initial de l'automate
    initiaux = dico_classe[auto['I'][0]] 
    auto['I'] = list(initiaux) # on met les états initiaux en liste
    # on minimise les transitions
    auto["transitions"] = chemin_minimise(auto, [], initiaux, dico_classe)
    return auto


def classes_etats(auto, classes, dico_transi):
    """Etant donnés un automate, une liste de classes d'équivalence et un dictionnaire de transitions,
    Renvoie la liste des classes d'équivalence"""
    new_classes = []
    auto_etats = auto["etats"]
    for i in range(len(auto_etats)):
        # pour chaque état, on crée une classe d'équivalence contenant cet état
        classe = set()
        classe.add(auto_etats[i])
        for j in range(len(auto_etats)):
            # on ajoute dans la classe tous les états qui sont dans la même classe d'équivalence
            if (meme_classe(auto_etats[i], auto_etats[j], dico_transi, classes, auto)):
                classe.add(auto_etats[j])
        if classe not in new_classes:
            # on ajoute la classe à la liste des classes d'équivalence si elle n'y est pas déjà
            new_classes.append(classe)

    if classes != new_classes:  # si les classes ont changé, on continue le processus
        return classes_etats(auto, new_classes, dico_transi)
    return classes


def meme_classe(etat1, etat2, dico_transi, classes, auto):
    """Etant donnés deux états, un dictionnaire de transitions, une liste de classes d'équivalence et un automate,
    Renvoie True si les deux états sont dans la même classe d'équivalence, False sinon"""
    for symbole in auto["alphabet"]:  # pour chaque symbole de l'alphabet
        for set in classes:  # pour chaque classe d'équivalence
            # si les deux états ne sont pas dans la même classe d'équivalence, on renvoie False
            if (not (etat1 in set and etat2 in set) and (etat1 in set or etat2 in set)):
                return False
            etat1inset = dico_transi[(etat1, symbole)] in set
            etat2inset = dico_transi[(etat2, symbole)] in set
            if (not (etat1inset and etat2inset) and (etat1inset or etat2inset)):
                return False
    return True


def chemin_minimise(auto, transitions, etats, dico_classes):
    """Etant donnés un automate, une liste de transitions, une liste d'états et un dictionnaire associant à chaque état, son nouvel état,
    Renvoie la liste des transitions minimisées"""
    for symbole in auto["alphabet"]:
        # pour chaque symbole de l'alphabet, on récupère les états possibles
        etatspossibles = lirelettre(auto["transitions"], [etats[0]], symbole)
        if etatspossibles != []:
            # si il y a des états possibles, on récupère la classe de l'état possible
            classepossible = dico_classes[etatspossibles[0]]
            if ([etats, symbole, classepossible] not in transitions):
                # si la transition n'est pas déjà dans la liste des transitions, on l'ajoute
                transitions.append([etats, symbole, classepossible])
                # on continue le processus avec les états possibles
                chemin_minimise(auto, transitions,
                                classepossible, dico_classes)
    return transitions


def dico_classes(etats_minimise):
    """Etant donné une liste de classes d'états,
    Renvoie un dictionnaire associant à chaque état son nouvel état"""
    dico_classes = dict()  # dictionnaire associant à chaque état, son nouvel état
    for i in range(len(etats_minimise)):  # pour chaque groupe d'états dans la classe d'équivalence
        for etat in etats_minimise[i]:  # pour chaque état de ce groupe
            dico_classes[etat] = etats_minimise[i] # on associe l'état à son nouvel état
    return dico_classes


def dico_transi(auto):
    """Etant donné un automate,
    Renovie un dictionnaire associant à chaque transition son état d'arrivée"""
    dico_transi = dict()
    for transition in auto["transitions"]: # pour chaque transition
        # on associe la transition à son état d'arrivée
        # sous la forme (état de départ, symbole) : état d'arrivée
        dico_transi[(transition[0], transition[1])] = transition[2] 
    return dico_transi

def chemin(auto, depart, arrivee, visite=set()):
    # Condition si c'est le meme etat
    if depart == arrivee:
        return True
    # Eviter une boucle infinie
    visite.add(depart)
    # Utilisation récursivité
    for transition in auto["transitions"]:
        if transition[0] == depart and transition[2] not in visite:
            if chemin(auto, transition[2], arrivee, visite):
                return True
    # Si on a parcouru toutes les transitions sans trouver de chemin, il n'y en a pas
    return False

def est_accessible(auto): 
    return all(chemin(auto, i, e) for i in auto['I'] for e in auto['etats'])

def est_co_accessible(auto):
    return all(chemin(auto, e, f) for e in auto['etats'] for f in auto['F'])

def est_emondé(auto):
    print(est_accessible(auto),est_co_accessible(auto))
    if (est_accessible(auto) and est_co_accessible(auto)):
        return True
    return False

# ========================================================================= TESTS ET REPONSES ========================================================================= #

# 1 - Mots, langages et automates...

print('-----   1 - Mots, langages et automates...   -----\n')

print('-----   1.1 - Mots   -----\n')
mot = 'coucou'
print(f'1.1.1 - Prefixes : {pref(mot)}')
print(f'1.1.2 - Suffixes : {suf(mot)}')
print(f'1.1.3 - Facteurs : {fact(mot)}')
print(f'1.1.4 - Miroir : {miroir(mot)}')

print('\n-----   1.2 - Langages   -----\n')
L1 = ['aa','ab','ba','bb']
L2 = ['a','b','']
print(f'1.2.1 - Concaténation : {concatene(L1,L2)}')
print(f'1.2.2 - Puissance : {puis(L1,2)}')
print('1.2.3 - Car il y a un nombre infini de possibilités')
print(f'1.2.4 - Tous les mots : {tousmots(["a","b"],3)}')

print('\n-----   1.3 - Automates   -----\n')
auto ={"alphabet":['a','b'],"etats": [1,2,3,4],
"transitions":[[1,'a',2],[2,'a',2],[2,'b',3],[3,'a',4]],
"I":[1],"F":[4]}
###print(f'1.3.1 - Définition de l\'automate : {defauto()}')
print(f'1.3.2 - Lire la lettre : {lirelettre(auto["transitions"],auto["etats"],"a")}')
print(f'1.3.3 - Lire le mot : {liremot(auto["transitions"],auto["etats"],"aba")}')
print(f'1.3.4 - Mot accepté : {accepte(auto, "aba")}')
print(f'1.3.5 - Langage accepté : {langage_accepte(auto, 5)}')
print('1.3.6 - Car il y a un nombre infini de possibilités')

# 2 - Déterminisation

print('\n-----   2 - Déterminisation   -----\n')
auto0 ={"alphabet":['a','b'],"etats": [0,1,2,3],
"transitions":[[0,'a',1],[1,'a',1],[1,'b',2],[2,'a',3]], "I":[0],"F":[3]}
auto1 ={"alphabet":['a','b'],"etats": [0,1],
"transitions":[[0,'a',0],[0,'b',1],[1,'b',1],[1,'a',1]], "I":[0],"F":[1]}
auto2={"alphabet":['a','b'],"etats": [0,1],
"transitions":[[0,'a',0],[0,'a',1],[1,'b',1],[1,'a',1]], "I":[0],"F":[1]}
print(f'2.1 - Auto0 déterministe : {deterministe(auto0)}')
print(f'2.1 - Auto1 déterministe : {deterministe(auto1)}')
print(f'2.1 - Auto2 déterministe : {deterministe(auto2)}')
print(f'2.2 - Auto2 déterminisé : {determinise(auto2)}')
print(f'2.3 - Auto2 renommé : {renommage(determinise(auto2))}')

# 3 - Complémentation

print('\n-----   3 - Complémentation   -----\n')
auto3 ={"alphabet":['a','b'],"etats": [0,1,2],
"transitions":[[0,'a',1],[0,'a',0],[1,'b',2],[1,'b',1]], "I":[0],"F":[2]}
print(f'3.1 - Auto complet : {complet(auto0)}')
print(f'3.1 - Auto complet : {complet(auto1)}')
print(f'3.2 - Auto completé : {complete(auto0)}')
print(f'3.2 - Auto complement : {complement(auto3)}')

# 4 - Automate produit

print('\n-----   4 - Automate produit   -----\n')
auto4 ={"alphabet":['a','b'],"etats": [0,1,2,],
"transitions":[[0,'a',1],[1,'b',2],[2,'b',2],[2,'a',2]], "I":[0],"F":[2]}
auto5 ={"alphabet":['a','b'],"etats": [0,1,2],
"transitions":[[0,'a',0],[0,'b',1],[1,'a',1],[1,'b',2],[2,'a',2],[2,'b',0]],
"I":[0],"F":[0,1]}

print(f'\n4.1 - Auto produit intersection : {inter(auto4, auto5)}')
print(f'\n4.1 - Auto produit intersection : {renommage(inter(auto4, auto5))}')
print(f'\n4.2 - Auto produit différence : {difference(auto4, auto5)}')
print(f'\n4.2 - Auto produit différence :  {renommage(difference(auto4, auto5))}')

# 5 - Propriétés de fermeture

print('\n-----   5 - Propriétés de fermeture   -----\n')
print(f'5.0 - Vérifier si l\'automate est émondé : {est_emondé(auto1)}')
print(f'5.1 - Auto préfixe : {prefixe(auto1)}')
print(f'5.2 - Auto suffixe : {suffixe(auto1)}')
print(f'5.3 - Auto facteur : {facteur(auto1)}')
print(f'5.4 - Auto miroir : {auto_miroir(auto1)}')

# 6 - Minimisation

print('\n-----   6 - Minimisation   -----\n')
auto6 ={"alphabet":['a','b'],"etats": [0,1,2,3,4,5],
"transitions":[[0,'a',4],[0,'b',3],[1,'a',5],[1,'b',5],[2,'a',5],[2,'b',2],[3,'a',1],[3,'b',0],
[4,'a',1],[4,'b',2],[5,'a',2],[5,'b',5]],
"I":[0],"F":[0,1,2,5]}

print(f'6.1 - Auto minimisé : {minimise(auto6)}')

# 7 - Bonus dessin graphes
print('\n-----   7 - Graphes   -----\n')
def organisation (auto) :
    print(auto)
    graphe = {}
    positions = {}
    j = 200
    i = 0
    for etats in auto["etats"] :
        if 400*(i+1) < 1600 :
            positions[etats] = (400*(i+1), j)
        else :
            i = 0
            j += 300
            positions[etats] = (400*(i+1), j)
        i += 1
    graphe["positions"] = positions
    arcs = []
    for t in auto["transitions"] :
        if arcs != [] :
            récurrence = False
            for verif in arcs :
                if verif[0] == t[0] and verif[2] == t[2] :
                    verif[1] = verif[1] +',' + t[1]
                    récurrence = True
            if récurrence == False :
                arcs.append([t[0],t[1],t[2]])
        else :
            arcs.append([t[0],t[1],t[2]])
    graphe["arcs"] = arcs
    graphe["initiaux"] = auto["I"]
    graphe["terminaux"] = auto["F"]
    print(graphe)
    return graphe


def draw_graphe(canvas, graphe):

    for nom, coordonnes in graphe["positions"].items():
        if nom in graphe["initiaux"] :
            canvas.create_oval ((coordonnes[0]-25, coordonnes[1]-25), (coordonnes[0]+25, coordonnes[1]+25), fill="white", width=2)
            canvas.create_line ((coordonnes[0]-75, coordonnes[1]), (coordonnes[0]-25, coordonnes[1]), arrow="last", arrowshape=(20,20,5), fill="black", width=3)
        elif nom in graphe["terminaux"] :
            canvas.create_oval ((coordonnes[0]-25, coordonnes[1]-25), (coordonnes[0]+25, coordonnes[1]+25), fill="white", width=2)
            canvas.create_oval ((coordonnes[0]-30, coordonnes[1]-30), (coordonnes[0]+30, coordonnes[1]+30), width=2)

        else :
            canvas.create_oval ((coordonnes[0]-25, coordonnes[1]-25), (coordonnes[0]+25, coordonnes[1]+25), fill="white", width=2)
        canvas.create_text (coordonnes[0], coordonnes[1], text= nom,fill= "black", font=("courier", 20), anchor="center", justify= "center")

    for arc in graphe["arcs"] :
        if arc[0] == arc[2] :
            courbe = [graphe["positions"][arc[2]][0], graphe["positions"][arc[0]][1]-50]
            canvas.create_line ((graphe["positions"][arc[0]][0]-25, graphe["positions"][arc[0]][1]), (graphe["positions"][arc[0]][0]-50, graphe["positions"][arc[0]][1]-50), (courbe[0], courbe[1]), smooth= True, fill="black", width=3)
            canvas.create_line ((courbe[0], courbe[1]), (graphe["positions"][arc[0]][0]+50, graphe["positions"][arc[0]][1]-50), (graphe["positions"][arc[2]][0]+25, graphe["positions"][arc[2]][1]), smooth= True,arrow="last", arrowshape=(20,20,5), fill="black", width=3)
            canvas.create_text (courbe[0], courbe[1]-15, text= arc[1] ,fill= "black", font=("courier", 20), anchor="center", justify= "center")
        else :
            courbe = [abs((graphe["positions"][arc[0]][0]+graphe["positions"][arc[2]][0])//2), graphe["positions"][arc[0]][1]+100]
            canvas.create_line ((graphe["positions"][arc[0]][0]+25, graphe["positions"][arc[0]][1]), (courbe[0], courbe[1]), (graphe["positions"][arc[2]][0]-25, graphe["positions"][arc[2]][1]), smooth= True,arrow="last", arrowshape=(20,20,5), fill="black", width=3)
            canvas.create_text (courbe[0], courbe[1]-25, text= arc[1] ,fill= "black", font=("courier", 20), anchor="center", justify= "center")
    


def dessine (auto) :
    root= tkinter.Tk()
    root.title ("Dessin du graphe")
    canvas=tkinter.Canvas(root, width=1800, height=1080, bg="white")
    canvas.pack()
    graphe = organisation(auto)
    draw_graphe(canvas, graphe)
    root.mainloop()

dessine(complete(auto0))

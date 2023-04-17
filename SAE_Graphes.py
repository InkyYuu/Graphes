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
    return None

def difference(auto1, auto2):
    return None

def prefixe(auto) :
    #Tous les etats sont finaux
    return {
        "alphabet" : auto["alphabet"],
        "etats" : auto["etats"],
        "transitions" : auto["transitions"],
        "I": auto["I"],
        "F": [e for e in auto["etats"]]
    }

def suffixe(auto) :
    #Tous les etats sont initiaux
    return {
        "alphabet" : auto["alphabet"],
        "etats" : auto["etats"],
        "transitions" : auto["transitions"],
        "I": [e for e in auto["etats"]],
        "F": auto["F"]
    }

def facteurs(auto) :
    #Tous les etats sont finaux et terminaux
    return {
        "alphabet" : auto["alphabet"],
        "etats" : auto["etats"],
        "transitions" : auto["transitions"],
        "I": [e for e in auto["etats"]],
        "F": [e for e in auto["etats"]]
    }

def auto_miroir(auto) : #pour différencier de miroir(u)
    #On inverse le sens des transitions, les etats finaux deiviennent initiaux et vice versa pour les terminaux
    return {
        "alphabet" : auto["alphabet"],
        "etats" : auto["etats"],
        "transitions" : [[transition[2], transition[1], transition[0]] for transition in auto["transitions"]],
        "I": auto["F"],
        "F": auto["I"]
    }

def minimise(auto):
    return None
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
print(f'4.1 - Auto produit intersection : {inter(auto0, auto1)}')
print(f'4.2 - Auto produit différence : {difference(auto0, auto1)}')

# 5 - Propriétés de fermeture

print('\n-----   5 - Propriétés de fermeture   -----\n')
print(f'5.1 - Auto préfixe : {prefixe(auto1)}')
print(f'5.2 - Auto suffixe : {suffixe(auto1)}')
print(f'5.3 - Auto facteur : {complete(auto1)}')
print(f'5.4 - Auto miroir : {auto_miroir(auto1)}')

# 6 - Minimisation

print('\n-----   6 - Minimisation   -----\n')
auto6 ={"alphabet":['a','b'],"etats": [0,1,2,3,4,5],
"transitions":[[0,'a',4],[0,'b',3],[1,'a',5],[1,'b',5],[2,'a',5],[2,'b',2],[3,'a',1],[3,'b',0],
[4,'a',1],[4,'b',2],[5,'a',2],[5,'b',5]],
"I":[0],"F":[0,1,2,5]}
print(f'6.1 - Auto minimisé : {minimise(auto6)}')

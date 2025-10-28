import heapq

class Actor:
    def __init__(self, nm_id, name):
        self.nm_id = nm_id
        self.name = name
        self.films = []  #liste med Film-objektene


class Film:
    def __init__(self, tt_id, title, rating):
        self.tt_id = tt_id
        self.title = title
        self.rating = rating
        self.actors = []  # liste med Actor-objektene


#Lese filmer fra fil
def les_filmer(filnavn):
    films = {}
    with open(filnavn, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 3:
                continue  # hopper over tomme eller ugyldige linjer
            tt_id = parts[0]
            title = parts[1]
            rating_str = parts[2].split()[0] #Fordi rating og antall stemmer ble lagret sammen? - så la på split for å løse det
            rating = float(rating_str)
            films[tt_id] = Film(tt_id, title, rating)
    return films


#Lese skuespillere fra fil
def les_skuespillere(filnavn, films):

    actors = {}
    with open(filnavn, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            nm_id = parts[0]
            name = parts[1]
            tt_ids = parts[2:]
            
            actor = Actor(nm_id, name)
            actors[nm_id] = actor

            #Legge til filmer til skuespiller og omvendt
            for tt in tt_ids:
                if tt in films: #Hvis ikke skal vi ignorere den filmen
                    film = films[tt]
                    actor.films.append(film)
                    film.actors.append(actor)
    return actors



films = les_filmer("movies.tsv")
actors = les_skuespillere("actors.tsv", films)

edges = []  # hver kant = (Actor1, Actor2, Film, rating)

#Nabo ordbok
neighbors = {}  # nm_id = liste av naboer/ [(annen_nm_id1, film1, rating1), (annen_nm_id2, film2, rating2)]

for film in films.values():
    n = len(film.actors)
    for i in range(n):
        for j in range(i + 1, n):
            a1 = film.actors[i]
            a2 = film.actors[j]
            edges.append((a1, a2, film, film.rating))

            #Legge til i naboer ordbok
            if a1.nm_id not in neighbors:
                neighbors[a1.nm_id] = []
            if a2.nm_id not in neighbors:
                neighbors[a2.nm_id] = []
            neighbors[a1.nm_id].append((a2.nm_id, film, film.rating))
            neighbors[a2.nm_id].append((a1.nm_id, film, film.rating))

#også legge til skuespillere som ikke har naboer
for nm_id in actors.keys():
    if nm_id not in neighbors:
        neighbors[nm_id] = []

#Antall noder og kanter - Oppgave 1
print("\nOppgave 1")
print("Antall skuespillere (noder):", len(actors))
print("Antall kanter (filmer som forbinder skuespillere):", len(edges))


#Komponenter - Oppgave 2
print("\nOppgave 2")
def BFSVisit(neighbors, visited, start_nm_id):
    antall_i_komponent = 1

    visited.add(start_nm_id)
    kø = [start_nm_id]

    while kø:
        u = kø.pop(0)
        for nabo in neighbors.get(u):
            nabo_id = nabo[0]
            if nabo_id not in visited:
                visited.add(nabo_id)
                kø.append(nabo_id)
                antall_i_komponent += 1
    return antall_i_komponent

def BFSFull(neighbors):
    visited = set()
    komponenter = {}

    for nm_id in neighbors.keys():
        if nm_id not in visited:
            størrelse = BFSVisit(neighbors, visited, nm_id)
            if størrelse in komponenter:
                komponenter[størrelse] += 1
            else:
                komponenter[størrelse] = 1

    return komponenter

komponenter = BFSFull(neighbors)
print("\nKomponenter i grafen:")
for størrelse in sorted(komponenter.keys(), reverse = True):
    print("There are "+ str(komponenter[størrelse])+" components of size " +str(størrelse))


#Oppgave 3 - Finne beste vei mellom to skuespillere. Bruker BFSVisit her også
print("\nOppgave 3 - Korteste sti mellom skuespillere")
def korteste_sti(neighbors, start_nm_id, slutt_nm_id):
    kø = [start_nm_id]
    visited = set()
    visited.add(start_nm_id)
    forelder = {start_nm_id: None}

    while len(kø) > 0:
        u = kø.pop(0)
        if u == slutt_nm_id:
            break  # hvis vi finner riktige noden

        for nabo in neighbors.get(u):
            nabo_id = nabo[0]
            film = nabo[1]
            rating = nabo[2]

            if nabo_id not in visited:
                visited.add(nabo_id)
                forelder[nabo_id] = (u, film, rating)
                kø.append(nabo_id)

    if slutt_nm_id not in forelder:
        return None
    
    sti = []
    currentActor = slutt_nm_id
    while forelder[currentActor] is not None:
        prevActor, film, rating = forelder[currentActor]
        sti.append((prevActor, currentActor, film, rating))
        currentActor = prevActor

    # snu rekkefølgen (fordi vi startet bakerst)
    sti.reverse()
    return sti


def skriv_ut_korteste_sti(neighbors, actors, fra_id, til_id):
    print("\n")
    sti = korteste_sti(neighbors, fra_id, til_id)

    if sti is None or len(sti)== 0:    
        print("Ingen forbindelse mellom " + actors[fra_id].name + " og " + actors[til_id].name)
    else:
        print("Fra: " + actors[fra_id].name)
        for actor1, actor2, film, rating in sti:
            print("--> Film: " + film.title + " (" + str(rating) + ") --> Skuespiller: " + actors[actor2].name)


skriv_ut_korteste_sti(neighbors, actors, "nm2255973", "nm0000460")  
skriv_ut_korteste_sti(neighbors, actors, "nm0424060", "nm8076281")  
skriv_ut_korteste_sti(neighbors, actors, "nm4689420", "nm0000365")  
skriv_ut_korteste_sti(neighbors, actors, "nm0000288", "nm2143282")  
skriv_ut_korteste_sti(neighbors, actors, "nm0637259", "nm0931324")  



#Oppgave 4 - Chilleste veien mellom to skuespillere. Bruk av Dijkstra
print("\n")
print("\nChilleste veier mellom skuespillere: ")
def chilleste_sti(neighbors, start_nm_id, slutt_nm_id):
    dist = dict()
    forelder = {start_nm_id: None}
    kø = []
    visited = set()

    for nm_id in neighbors:
        dist[nm_id] = (float('inf'))
        
    dist[start_nm_id] = 0
    heapq.heappush(kø, (0, start_nm_id))

    while kø:

        #Gjorde det først slik men det gjorde at koden brukte veldig lang tid på å kjøre, brukte derfor heller heapq
        #min_index = 0
        #min_dist = kø[0][0]
        #for i in range(1, len(kø)):#Finne indeksen til minste verdien i køen
        #    if kø[i][0] < min_dist:
        #        min_dist = kø[i][0]
        #        min_index = i

        #u_dist, u = kø.pop(min_index) 

        u_dist, u = heapq.heappop(kø)


        if u == slutt_nm_id:
            break  # hvis vi finner riktige noden

        if u in visited:
            continue

        visited.add(u)

        for nabo in neighbors.get(u):
            nabo_id = nabo[0]
            film = nabo[1]
            rating = nabo[2]

            vekt = 10 - rating

            c = u_dist + vekt
            if c < dist[nabo_id]:
                dist[nabo_id] = c
                heapq.heappush(kø, (c, nabo_id))
                forelder[nabo_id] = (u,film,rating)

    if slutt_nm_id not in forelder:
        return None

    sti = []
    currentActor = slutt_nm_id
    while forelder[currentActor] is not None:
        prevActor, film, rating = forelder[currentActor]
        sti.append((prevActor, currentActor, film, rating))
        currentActor = prevActor

    sti.reverse()

    total_vekt = dist[slutt_nm_id]
    return sti, total_vekt


def skriv_ut_chilleste_sti(neighbors, actors, fra_id, til_id):
    print("\n")
    sti, total_vekt = chilleste_sti(neighbors, fra_id, til_id)

    if sti is None or len(sti) == 0:
        print("Ingen forbindelse mellom " + actors[fra_id].name + " og " + actors[til_id].name)
    else:
        print("Fra: " + actors[fra_id].name)
        for actor1, actor2, film, rating in sti:
            print("--> Film: " + film.title + " (" + str(rating) + ") --> Skuespiller: " + actors[actor2].name)
        print("Total vekt: "+str(round(total_vekt,1)))

skriv_ut_chilleste_sti(neighbors, actors, "nm2255973", "nm0000460")
skriv_ut_chilleste_sti(neighbors, actors, "nm0424060", "nm8076281") 
skriv_ut_chilleste_sti(neighbors, actors, "nm4689420", "nm0000365") 
skriv_ut_chilleste_sti(neighbors, actors, "nm0000288", "nm2143282")  
skriv_ut_chilleste_sti(neighbors, actors, "nm0637259", "nm0931324")  





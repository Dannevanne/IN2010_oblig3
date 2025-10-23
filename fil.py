#Er et par ting som må rettes opp, men tror jeg er inne på noe
from collections import defaultdict

class Graf:

    def __init__(self):
        self.skuespillere = {}
        self.filmer = {}
        self.skuespillere_i_film = defaultdict(list)
        self.graf = defaultdict(list)

    def hent_film(self, filnavn):
        with open(filnavn,"r") as file:
            for line in file:
                parts = line.strip().split("\t")
                tt_id, title, rating = parts[0], parts[1], parts[2]
                self.filmer[tt_id] = float(rating)

    def hent_skuespillere(self,filnavn):
        with open(filnavn,"r") as file:
            for line in file:
                parts = line.strip().split("\t")
                nmId, name, tt_id = parts[0], parts[1], parts[2:]
                self.skuespillere[nmId] = tt_id

    def film_til_skuespillere(self):
        for skuespiller in self.skuespillere:
            filmer_spilt_i = self.skuespillere[skuespiller]
            for tt_id in filmer_spilt_i:
                if tt_id in self.filmer:
                    self.skuespillere_i_film[tt_id].append(skuespiller)

    def bygg_graf(self):
        for tt_id, skuespillere in self.skuespillere_i_film.items():
            rating = self.filmer[tt_id]
            for i in range(len(skuespillere)):
                for j in range(i+1, len(skuespillere)):
                    self.graf[skuespillere[i]].append((skuespillere[j], tt_id, rating))
                    self.graf[skuespillere[j]].append((skuespillere[i], tt_id, rating))

    def ant_noder_og_kanter(self):
        ant_noder = 0
        ant_kanter = 0
        for node in self.graf:
            ant_noder += 1
            for kanter in self.graf[node]:
                ant_kanter += 1
        
        return ant_noder, ant_kanter

def main():
    graf = Graf()

    graf.hent_film("marvel_movies.tsv")
    graf.hent_skuespillere("marvel_actors.tsv")
    graf.film_til_skuespillere()
    graf.bygg_graf()
    print(graf.ant_noder_og_kanter())


if __name__ == "__main__":
    main()

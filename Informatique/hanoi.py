def deplacer_disque(source, destination):
    print(f'Déplacer le disque de {source} à {destination}')

def hanoi(n):
    def resoudre_hanoi(n, tour_source, tour_destination, tour_intermediaire):
        if n==0:
            return
        resoudre_hanoi(n-1, tour_source, tour_intermediaire, tour_destination)
        deplacer_disque(tour_source, tour_destination)
        resoudre_hanoi(n-1, tour_intermediaire, tour_destination, tour_source)
    resoudre_hanoi(n,'A', 'C', 'B' )

hanoi(6)
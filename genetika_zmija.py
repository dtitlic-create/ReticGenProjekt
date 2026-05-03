# iterator za sve kombinacije
import itertools
# brojac
from collections import Counter

from genska_lista import  KODOMINANTNI_GENI, SUPER_GENI

def izracun_gena(geni_oca, geni_majke):
    # Dodavanje normala ako imamo jedan gen roditelja
    svi_geni = list(set(geni_oca + geni_majke))
    parovi_otac = []
    parovi_majka = []
    for g in svi_geni:
        if g in geni_oca:
            parovi_otac.append([g, "Normal"])
        else:
            parovi_otac.append(["Normal","Normal"])
    for g in svi_geni:
        if g in geni_majke:
            parovi_majka.append([g, "Normal"])
        else:
            parovi_majka.append(["Normal","Normal"])

# Ukrstavanje majke i oca

    rezultat_ukrstavanja = []
    for i in range(len(svi_geni)):
        kombinacije = list(itertools.product(parovi_otac[i], parovi_majka[i]))
        rezultat_ukrstavanja.append(kombinacije)
    # o1,o2 i m1,m2 = o1m1, o1,m2, o2,m1, o2,m2
    offspring = list(itertools.product(*rezultat_ukrstavanja))

    # ciscenje liste
    offspring_zavrsen = []
    for beba in offspring:
        offspring_filtriran = []
        for clan in beba:
                if clan[0] != "Normal" and clan[0] == clan[1]:
                    gen = clan[0]
                    # Provjera za super gene
                    if gen in SUPER_GENI:
                        offspring_filtriran.append(SUPER_GENI[gen])
                    elif gen in KODOMINANTNI_GENI:
                        offspring_filtriran.append("Super " + gen)
                    else:
                        offspring_filtriran.append(gen)
                else:
                    if clan[0] != "Normal":
                        offspring_filtriran.append(clan[0])
                    if clan[1] != "Normal":
                        offspring_filtriran.append(clan[1])

        if not offspring_filtriran:
            ime_bebe = "Normal"
        else:
            offspring_filtriran.sort()
            ime_bebe=" ".join(offspring_filtriran)

        offspring_zavrsen.append(ime_bebe)
    # Brojac
    brojac = Counter(offspring_zavrsen)
    postotci = {}
    ukupno = len(offspring_zavrsen)
    for ime, kolicina in brojac.items():
        rezultat = (kolicina/ukupno) * 100
        postotci[ime] = rezultat
    return postotci

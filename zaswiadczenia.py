"""Lista osób uprawnionych do zaświadczenia (obecność na co najmniej 6 z 8 spotkań).

Uruchomienie:  python zaswiadczenia.py
Wejście:       dane/uczestnicy.csv
Wyniki:        wynik/uprawnieni.csv, wynik/nieuprawnieni.csv

Przyjęte decyzje przy niejednoznacznych danych (zatwierdzone przez zamawiającego):
- Wiersze z tym samym e-mailem to jedna osoba; obecności łączymy (obecna, jeśli
  którykolwiek wiersz mówi „obecna”).
- „x” oznacza obecność, „-” nieobecność; pusta komórka to nieobecność.
- Brak lub błędny e-mail nie odbiera prawa do zaświadczenia — osoba trafia na listę
  z uwagą o danych do uzupełnienia.
"""

import csv
import re
import sys
from pathlib import Path

PROG = 6
LICZBA_SPOTKAN = 8
PLIK_WEJSCIOWY = Path("dane/uczestnicy.csv")
KATALOG_WYNIKOW = Path("wynik")

OBECNY = {"tak", "1", "x", "obecny", "obecna"}
NIEOBECNY = {"nie", "0", "-", "nieobecny", "nieobecna", ""}

# Skróty i warianty nazw jednostek → nazwa kanoniczna (porównanie bez wielkości liter).
JEDNOSTKI = {
    "zi": "Zakład Informatyki",
    "zak. informatyki": "Zakład Informatyki",
    "zakład informatyki": "Zakład Informatyki",
    "dział rekrutacji": "Dział Rekrutacji",
}

WZOR_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$")


def popraw_imie_nazwisko(tekst):
    """„Woźniak, Paweł” → „Paweł Woźniak”; usuwa zbędne spacje."""
    tekst = " ".join(tekst.split())
    if "," in tekst:
        nazwisko, imie = (czesc.strip() for czesc in tekst.split(",", 1))
        tekst = f"{imie} {nazwisko}"
    return tekst


def popraw_jednostke(tekst):
    tekst = " ".join(tekst.split())
    return JEDNOSTKI.get(tekst.lower(), tekst)


def odczytaj_obecnosc(wartosc, nr_wiersza, kolumna):
    w = wartosc.strip().lower()
    if w in OBECNY:
        return True
    if w in NIEOBECNY:
        return False
    sys.exit(f"Błąd: nieznany zapis obecności „{wartosc}” (wiersz {nr_wiersza}, kolumna {kolumna}). "
             "Dopisz go do słownika OBECNY albo NIEOBECNY.")


def wczytaj_osoby():
    """Zwraca listę osób po scaleniu duplikatów (klucz: e-mail, a gdy go brak — imię i nazwisko)."""
    osoby = {}
    with PLIK_WEJSCIOWY.open(encoding="utf-8-sig", newline="") as plik:
        czytnik = csv.DictReader(plik, delimiter=";")
        for wiersz in czytnik:
            nr = czytnik.line_num  # numer linii w pliku (DictReader pomija puste linie)
            if not any((v or "").strip() for v in wiersz.values()):
                continue  # pusty wiersz

            imie_nazwisko = popraw_imie_nazwisko(wiersz["imie_nazwisko"])
            email = wiersz["email"].strip().lower()
            obecnosci = [odczytaj_obecnosc(wiersz[f"S{i}"], nr, f"S{i}")
                         for i in range(1, LICZBA_SPOTKAN + 1)]

            klucz = email or "brak-emaila:" + imie_nazwisko.lower()
            if klucz in osoby:
                osoba = osoby[klucz]
                osoba["obecnosci"] = [a or b for a, b in zip(osoba["obecnosci"], obecnosci)]
                osoba["wiersze"].append(nr)
                # Zostaw wariant zapisu z polskimi znakami (np. „Wiśniewska”, nie „Wisniewska”).
                if not imie_nazwisko.isascii() and osoba["imie_nazwisko"].isascii():
                    osoba["imie_nazwisko"] = imie_nazwisko
            else:
                osoby[klucz] = {
                    "imie_nazwisko": imie_nazwisko,
                    "email": email,
                    "jednostka": popraw_jednostke(wiersz["jednostka"]),
                    "obecnosci": obecnosci,
                    "wiersze": [nr],
                }
    return list(osoby.values())


def uwagi(osoba):
    lista = []
    if not osoba["email"]:
        lista.append("brak adresu e-mail — do uzupełnienia")
    elif not WZOR_EMAIL.match(osoba["email"]):
        lista.append(f"błędny adres e-mail ({osoba['email']}) — do poprawienia")
    if len(osoba["wiersze"]) > 1:
        nry = ", ".join(map(str, osoba["wiersze"]))
        lista.append(f"osoba zapisana kilka razy (wiersze {nry}) — obecności połączono")
    return "; ".join(lista)


def zapisz(sciezka, naglowek, wiersze):
    # utf-8-sig, żeby Excel poprawnie pokazał polskie znaki.
    with sciezka.open("w", encoding="utf-8-sig", newline="") as plik:
        zapis = csv.writer(plik, delimiter=";")
        zapis.writerow(naglowek)
        zapis.writerows(wiersze)


def main():
    osoby = sorted(wczytaj_osoby(), key=lambda o: o["imie_nazwisko"].split()[-1])
    uprawnieni, nieuprawnieni = [], []
    for osoba in osoby:
        liczba = sum(osoba["obecnosci"])
        if liczba >= PROG:
            uprawnieni.append([osoba["imie_nazwisko"], osoba["email"], osoba["jednostka"],
                               liczba, uwagi(osoba)])
        else:
            przyczyna = f"za mało obecności ({liczba} z {LICZBA_SPOTKAN}, wymagane {PROG})"
            nieuprawnieni.append([osoba["imie_nazwisko"], osoba["email"], osoba["jednostka"],
                                  liczba, przyczyna])

    KATALOG_WYNIKOW.mkdir(exist_ok=True)
    zapisz(KATALOG_WYNIKOW / "uprawnieni.csv",
           ["imie_nazwisko", "email", "jednostka", "obecnosci", "uwagi"], uprawnieni)
    zapisz(KATALOG_WYNIKOW / "nieuprawnieni.csv",
           ["imie_nazwisko", "email", "jednostka", "obecnosci", "przyczyna"], nieuprawnieni)

    print(f"Uprawnieni do zaświadczenia: {len(uprawnieni)} z {len(osoby)} osób")
    for w in uprawnieni:
        print(f"  ✔ {w[0]:<22} {w[3]}/8  {w[4]}")
    print(f"Bez zaświadczenia: {len(nieuprawnieni)}")
    for w in nieuprawnieni:
        print(f"  ✘ {w[0]:<22} {w[4]}")
    print(f"Wyniki zapisano w katalogu {KATALOG_WYNIKOW}/")


if __name__ == "__main__":
    main()

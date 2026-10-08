"""Lista osób uprawnionych do zaświadczenia (obecność na co najmniej 6 z 8 spotkań).

Uruchomienie:  python zaswiadczenia.py
Wejście:       dane/uczestnicy.csv
Wyniki:        wynik/uprawnieni.csv, wynik/nieuprawnieni.csv,
               wynik/raport_dla_dziekanatu.md

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
from datetime import date
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


def poprawki_wiersza(wiersz, nr):
    """Opisuje po ludzku, co w danym wierszu poprawiono lub założono przy liczeniu."""
    lista = []
    surowe_nazwisko = wiersz["imie_nazwisko"]
    if "," in surowe_nazwisko:
        lista.append(f"wiersz {nr}: nazwisko zapisane jako „{surowe_nazwisko.strip()}” — odwrócono kolejność")
    surowa_jednostka = wiersz["jednostka"].strip()
    if surowa_jednostka != popraw_jednostke(surowa_jednostka):
        lista.append(f"wiersz {nr}: jednostka zapisana jako „{surowa_jednostka}” — "
                     f"przyjęto „{popraw_jednostke(surowa_jednostka)}”")
    zapisy = [wiersz[f"S{i}"].strip().lower() for i in range(1, LICZBA_SPOTKAN + 1)]
    if "x" in zapisy:
        lista.append(f"wiersz {nr}: obecność oznaczona „x”/„-” — „x” policzono jako obecność")
    puste = [f"S{i}" for i, z in enumerate(zapisy, start=1) if z == ""]
    if puste:
        lista.append(f"wiersz {nr}: puste pola obecności ({', '.join(puste)}) — policzono jako nieobecność")
    return lista


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
                osoba = osoby[klucz] = {
                    "imie_nazwisko": imie_nazwisko,
                    "email": email,
                    "jednostka": popraw_jednostke(wiersz["jednostka"]),
                    "obecnosci": obecnosci,
                    "wiersze": [nr],
                    "poprawki": [],
                }
            osoba["poprawki"] += poprawki_wiersza(wiersz, nr)
    return list(osoby.values())


def problem_z_emailem(osoba):
    if not osoba["email"]:
        return "brak adresu e-mail — do uzupełnienia"
    if not WZOR_EMAIL.match(osoba["email"]):
        return f"błędny adres e-mail ({osoba['email']}) — do poprawienia"
    return ""


def uwagi(osoba):
    lista = [problem_z_emailem(osoba)] if problem_z_emailem(osoba) else []
    if len(osoba["wiersze"]) > 1:
        nry = ", ".join(map(str, osoba["wiersze"]))
        lista.append(f"osoba zapisana kilka razy (wiersze {nry}) — obecności połączono")
    return "; ".join(lista)


def nieobecnosci(osoba):
    return ", ".join(f"S{i}" for i, ob in enumerate(osoba["obecnosci"], start=1) if not ob)


def zapisz(sciezka, naglowek, wiersze):
    # utf-8-sig, żeby Excel poprawnie pokazał polskie znaki.
    with sciezka.open("w", encoding="utf-8-sig", newline="") as plik:
        zapis = csv.writer(plik, delimiter=";")
        zapis.writerow(naglowek)
        zapis.writerows(wiersze)


def zapisz_raport(sciezka, uprawnieni, nieuprawnieni):
    wszyscy = uprawnieni + nieuprawnieni
    liczba_wpisow = sum(len(o["wiersze"]) for o in wszyscy)
    do_wyjasnienia = [o for o in uprawnieni if problem_z_emailem(o)]
    duplikaty = [o for o in wszyscy if len(o["wiersze"]) > 1]

    r = []
    r.append("# Zaświadczenia ukończenia cyklu spotkań — raport dla dziekanatu")
    r.append("")
    r.append(f"Data sporządzenia: {date.today():%d.%m.%Y}  ")
    r.append(f"Źródło: lista obecności `{PLIK_WEJSCIOWY.name}` ({liczba_wpisow} wpisów)  ")
    r.append(f"Reguła: zaświadczenie przysługuje osobie obecnej na **co najmniej {PROG} "
             f"z {LICZBA_SPOTKAN}** spotkań (S1–S{LICZBA_SPOTKAN}).")
    r.append("")
    r.append("## Podsumowanie")
    r.append("")
    r.append(f"- Liczba uczestników: **{len(wszyscy)}**")
    if duplikaty:
        r.append(f"  (wpisów na liście jest {liczba_wpisow}, bo {len(duplikaty)} "
                 f"{'osoba jest zapisana' if len(duplikaty) == 1 else 'osoby są zapisane'} więcej niż raz)")
    r.append(f"- Zaświadczenie przysługuje: **{len(uprawnieni)}**")
    r.append(f"- Zaświadczenie nie przysługuje: **{len(nieuprawnieni)}**")
    if do_wyjasnienia:
        r.append(f"- W tym do wyjaśnienia przed wysłaniem: **{len(do_wyjasnienia)}** "
                 "(brak lub błędny adres e-mail — patrz niżej)")
    r.append("")

    r.append("## Osoby, którym przysługuje zaświadczenie")
    r.append("")
    r.append("| Lp. | Imię i nazwisko | Jednostka | Obecności | Uwagi |")
    r.append("|---:|---|---|:---:|---|")
    for lp, o in enumerate(uprawnieni, start=1):
        r.append(f"| {lp} | {o['imie_nazwisko']} | {o['jednostka']} | "
                 f"{sum(o['obecnosci'])}/{LICZBA_SPOTKAN} | {uwagi(o)} |")
    r.append("")

    r.append("## Osoby, którym zaświadczenie nie przysługuje")
    r.append("")
    if nieuprawnieni:
        r.append("| Lp. | Imię i nazwisko | Jednostka | Obecności | Nieobecności | Przyczyna |")
        r.append("|---:|---|---|:---:|---|---|")
        for lp, o in enumerate(nieuprawnieni, start=1):
            liczba = sum(o["obecnosci"])
            brakuje = PROG - liczba
            r.append(f"| {lp} | {o['imie_nazwisko']} | {o['jednostka']} | {liczba}/{LICZBA_SPOTKAN} | "
                     f"{nieobecnosci(o)} | za mało obecności — brakuje {brakuje} "
                     f"{'spotkania' if brakuje == 1 else 'spotkań'} do progu |")
        r.append("")
        r.append("Żadnej osoby nie wykluczono z powodu braków w danych ani zdublowanego wpisu — "
                 "jedyną przyczyną odmowy jest liczba obecności.")
    else:
        r.append("Brak.")
    r.append("")

    if do_wyjasnienia:
        r.append("## Do wyjaśnienia przed wysłaniem zaświadczeń")
        r.append("")
        r.append("Te osoby spełniają warunek obecności, ale ich dane kontaktowe są niekompletne:")
        r.append("")
        for o in do_wyjasnienia:
            r.append(f"- **{o['imie_nazwisko']}** ({o['jednostka']}) — {problem_z_emailem(o)}")
        r.append("")

    r.append("## Jak liczono obecność — przyjęte założenia")
    r.append("")
    r.append("Lista była prowadzona ręcznie przez różne osoby, więc zapis nie był jednolity. "
             "Przyjęto następujące zasady:")
    r.append("")
    r.append("- Obecność zapisywano na różne sposoby (TAK/NIE, tak/nie, 1/0, x/-, obecny/nieobecny) — "
             "wszystkie potraktowano jednakowo; „x” oznacza obecność.")
    r.append("- Puste pole obecności liczono jako nieobecność.")
    r.append("- Ta sama osoba zapisana kilka razy (ten sam adres e-mail) to jedna osoba — "
             "spotkanie liczy się jako obecność, jeśli którykolwiek wpis ją odnotował.")
    r.append("- Brak lub błędny adres e-mail nie odbiera prawa do zaświadczenia.")
    r.append("- Ujednolicono zapis nazw jednostek i kolejność „imię nazwisko”.")
    r.append("")
    z_poprawkami = [o for o in wszyscy if o["poprawki"] or len(o["wiersze"]) > 1]
    if z_poprawkami:
        r.append("Szczegóły poprawek (numery wierszy odnoszą się do pliku źródłowego):")
        r.append("")
        for o in sorted(z_poprawkami, key=lambda o: o["wiersze"][0]):
            opisy = list(o["poprawki"])
            if len(o["wiersze"]) > 1:
                opisy.insert(0, f"wpisy w wierszach {', '.join(map(str, o['wiersze']))} połączono "
                                f"(łącznie {sum(o['obecnosci'])}/{LICZBA_SPOTKAN} obecności)")
            r.append(f"- **{o['imie_nazwisko']}**: " + "; ".join(opisy))
        r.append("")

    sciezka.write_text("\n".join(r), encoding="utf-8")


def main():
    osoby = sorted(wczytaj_osoby(), key=lambda o: o["imie_nazwisko"].split()[-1])
    uprawnieni = [o for o in osoby if sum(o["obecnosci"]) >= PROG]
    nieuprawnieni = [o for o in osoby if sum(o["obecnosci"]) < PROG]

    KATALOG_WYNIKOW.mkdir(exist_ok=True)
    zapisz(KATALOG_WYNIKOW / "uprawnieni.csv",
           ["imie_nazwisko", "email", "jednostka", "obecnosci", "uwagi"],
           [[o["imie_nazwisko"], o["email"], o["jednostka"], sum(o["obecnosci"]), uwagi(o)]
            for o in uprawnieni])
    zapisz(KATALOG_WYNIKOW / "nieuprawnieni.csv",
           ["imie_nazwisko", "email", "jednostka", "obecnosci", "przyczyna"],
           [[o["imie_nazwisko"], o["email"], o["jednostka"], sum(o["obecnosci"]),
             f"za mało obecności ({sum(o['obecnosci'])} z {LICZBA_SPOTKAN}, wymagane {PROG})"]
            for o in nieuprawnieni])
    zapisz_raport(KATALOG_WYNIKOW / "raport_dla_dziekanatu.md", uprawnieni, nieuprawnieni)

    print(f"Uprawnieni do zaświadczenia: {len(uprawnieni)} z {len(osoby)} osób")
    for o in uprawnieni:
        print(f"  ✔ {o['imie_nazwisko']:<22} {sum(o['obecnosci'])}/8  {uwagi(o)}")
    print(f"Bez zaświadczenia: {len(nieuprawnieni)}")
    for o in nieuprawnieni:
        print(f"  ✘ {o['imie_nazwisko']:<22} za mało obecności ({sum(o['obecnosci'])} z 8)")
    print(f"Wyniki zapisano w katalogu {KATALOG_WYNIKOW}/ (raport: raport_dla_dziekanatu.md)")


if __name__ == "__main__":
    main()

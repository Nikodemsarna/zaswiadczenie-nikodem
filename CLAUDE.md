# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projekt

Ćwiczenie warsztatowe „Zaświadczenia” (sesja 2 kursu „Od promptu do produktu”). Cel: jednym poleceniem
wygenerować listę osób uprawnionych do zaświadczenia o ukończeniu cyklu ośmiu spotkań oraz wyjaśnić,
komu i dlaczego zaświadczenie się nie należy. Treści, komunikaty, raporty i opisy commitów — po polsku.

To osobne repozytorium git. `CLAUDE.md` z katalogu nadrzędnego (aplikacja „Zeszyt ćwiczeń UX”, Node,
`public/`, `engine.js`) **nie dotyczy tego projektu** — ignoruj jego polecenia i architekturę.

## Stan repozytorium

Na starcie nie ma jeszcze kodu ani wybranej technologii — repozytorium zawiera tylko dane i materiały
warsztatowe. Środowisko (`.devcontainer/`, Codespaces) zapewnia Python 3.12 i Node.js LTS; brak zależności,
lintera, testów i kroku budowania, dopóki ich nie dodamy.

- `dane/uczestnicy.csv` — lista obecności (wejście). Separator `;`, UTF-8, kolumny
  `imie_nazwisko;email;jednostka;S1..S8`. Format opisany w `dane/OPIS_DANYCH.md`.
- `README.md`, `INSTRUKCJA_UCZESTNIKA.md`, `KARTA_PRACY.md` — opis zadania i faz warsztatu (F0–F5
  plus rozszerzenia). `KARTA_PRACY.md` określa, czego oczekuje się na każdym etapie.
- `CODESPACE.md`, `.devcontainer/` — alternatywne środowisko w przeglądarce.

## Reguła biznesowa

Zaświadczenie przysługuje osobie obecnej na **co najmniej 6 z 8** spotkań.

## Ważne przy pracy z danymi

- Plik CSV był prowadzony ręcznie przez różne osoby i **celowo nie jest wyczyszczony** — to część zadania.
  Przed napisaniem kodu przeanalizuj jakość danych i przedstaw listę problemów; nie zakładaj, że format
  jest jednolity.
- Tożsamość osoby ustalaj po adresie e-mail, nie po imieniu i nazwisku.
- Przypadki niejednoznaczne (gdzie nie ma jednej poprawnej odpowiedzi) to decyzje biznesowe, nie
  techniczne — zgłoś je użytkownikowi i zapytaj, zamiast rozstrzygać po cichu. Przyjęte decyzje
  odnotuj w raporcie.
- Nie modyfikuj `dane/uczestnicy.csv` — czyszczenie odbywa się w kodzie.
- Oczekiwane wyniki: lista uprawnionych oraz raport osób nieuprawnionych z przyczyną
  (za mało obecności / brak danych / duplikat), zrozumiały dla dziekanatu.

## Git

- `.gitignore` wyklucza katalog `wynik/` oraz `DLA_PROWADZACEGO.md` (materiał prowadzącego — nie publikować).
- `.gitattributes` wymusza końce linii LF (inaczej `setup.sh` nie zadziała w Codespace).
